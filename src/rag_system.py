"""
RAG (Retrieval-Augmented Generation) System for SAT Knowledge Base

This module implements a semantic search system using embeddings to find
relevant content from the SAT knowledge base for better question answering.
"""

import os
import json
import chromadb
from pathlib import Path
from typing import List, Dict, Any, Optional
from google import genai
import uuid
import time

class SATKnowledgeRAG:
    """
    RAG system for SAT knowledge base using ChromaDB and sentence transformers.
    """
    
    def __init__(self, api_key: str, knowledge_base_path: str = "../satKnowledge", collection_name: str = "sat_knowledge"):
        """
        Initialize the RAG system.
        
        Args:
            api_key (str): Gemini API key for embeddings
            knowledge_base_path (str): Path to the SAT knowledge base directory
            collection_name (str): Name for the ChromaDB collection
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.collection_name = collection_name
        
        # Initialize Gemini client for embeddings
        print("Initializing Gemini client for embeddings...")
        self.client = genai.Client(api_key=api_key)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection(name=collection_name)
            print(f"Loaded existing collection '{collection_name}'")
        except:
            print(f"Creating new collection '{collection_name}'")
            self.collection = self.chroma_client.create_collection(name=collection_name)
            self._build_knowledge_index()
    
    def _build_knowledge_index(self):
        """Build the vector index from all knowledge base content."""
        print("Building knowledge index...")
        
        documents = []
        metadatas = []
        ids = []
        
        # Process both math and english subjects
        for subject in ["math", "english"]:
            subject_path = self.knowledge_base_path / subject
            if subject_path.exists():
                self._process_subject_directory(subject, subject_path, documents, metadatas, ids)
        
        if documents:
            print(f"Adding {len(documents)} documents to the index...")
            # Generate embeddings using Gemini
            embeddings = self._generate_embeddings(documents)
            
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings,
                ids=ids
            )
            print("Knowledge index built successfully!")
        else:
            print("No documents found to index.")
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Gemini.
        
        Args:
            texts (List[str]): List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        embeddings = []
        print(f"Generating embeddings for {len(texts)} documents...")
        
        for i, text in enumerate(texts):
            try:
                # Use Gemini's embedding model
                result = self.client.models.embed_content(
                    model='text-embedding-004',
                    contents=text
                )
                embeddings.append(result.embeddings[0].values)
                
                # Add small delay to avoid rate limiting
                if i > 0 and i % 10 == 0:
                    print(f"Generated embeddings for {i}/{len(texts)} documents...")
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"Error generating embedding for document {i}: {e}")
                # Use a zero vector as fallback
                embeddings.append([0.0] * 768)  # Assuming 768-dimensional embeddings
        
        return embeddings
    
    def _generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a single query using Gemini.
        
        Args:
            query (str): Query text to embed
            
        Returns:
            List[float]: Embedding vector
        """
        try:
            result = self.client.models.embed_content(
                model='text-embedding-004',
                contents=query
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return [0.0] * 768
    
    def _process_subject_directory(self, subject: str, subject_path: Path, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Process a subject directory and extract content."""
        
        # Process main subject files with new naming pattern
        overview_file = subject_path / f"{subject}-overview.md"
        if overview_file.exists():
            content = self._read_markdown_file(overview_file)
            if content.strip():
                documents.append(content)
                metadatas.append({
                    "subject": subject,
                    "type": "subject_overview",
                    "title": f"{subject.capitalize()} Overview",
                    "file_path": str(overview_file)
                })
                ids.append(str(uuid.uuid4()))
        
        study_notes_file = subject_path / f"{subject}-study-notes.md"
        if study_notes_file.exists():
            content = self._read_markdown_file(study_notes_file)
            if content.strip():
                documents.append(content)
                metadatas.append({
                    "subject": subject,
                    "type": "subject_notes",
                    "title": f"{subject.capitalize()} Study Notes",
                    "file_path": str(study_notes_file)
                })
                ids.append(str(uuid.uuid4()))
        
        # Process topic directories
        for topic_dir in subject_path.iterdir():
            if topic_dir.is_dir():
                self._process_topic_directory(subject, topic_dir.name, topic_dir, documents, metadatas, ids)
    
    def _process_topic_directory(self, subject: str, topic_name: str, topic_path: Path, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Process a topic directory and extract content."""
        
        # Process topic files with new naming pattern
        for file in topic_path.iterdir():
            if file.is_file() and file.suffix == '.md':
                content = self._read_markdown_file(file)
                if content.strip():
                    if file.name.endswith('-overview.md'):
                        doc_type = "topic_overview"
                        title = f"{topic_name.replace('-', ' ').title()} Overview"
                    elif file.name.endswith('-study-notes.md'):
                        doc_type = "topic_notes"
                        title = f"{topic_name.replace('-', ' ').title()} Study Notes"
                    else:
                        doc_type = "topic_content"
                        title = f"{topic_name.replace('-', ' ').title()} - {file.stem}"
                    
                    documents.append(content)
                    metadatas.append({
                        "subject": subject,
                        "topic": topic_name,
                        "type": doc_type,
                        "title": title,
                        "file_path": str(file)
                    })
                    ids.append(str(uuid.uuid4()))
            
            elif file.is_dir():
                # This is a subtopic directory
                self._process_subtopic_directory(subject, topic_name, file.name, file, documents, metadatas, ids)
    
    def _process_subtopic_directory(self, subject: str, topic_name: str, subtopic_name: str, subtopic_path: Path, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Process a subtopic directory and extract content."""
        
        for file in subtopic_path.iterdir():
            if file.is_file() and file.suffix == '.md':
                content = self._read_markdown_file(file)
                if content.strip():
                    if file.name.endswith('-overview.md'):
                        doc_type = "subtopic_overview"
                        title = f"{subtopic_name.replace('-', ' ').title()} Overview"
                    elif file.name.endswith('-study-notes.md'):
                        doc_type = "subtopic_notes"
                        title = f"{subtopic_name.replace('-', ' ').title()} Study Notes"
                    else:
                        doc_type = "subtopic_content"
                        title = f"{subtopic_name.replace('-', ' ').title()} - {file.stem}"
                    
                    documents.append(content)
                    metadatas.append({
                        "subject": subject,
                        "topic": topic_name,
                        "subtopic": subtopic_name,
                        "type": doc_type,
                        "title": title,
                        "file_path": str(file)
                    })
                    ids.append(str(uuid.uuid4()))
    
    def _read_markdown_file(self, file_path: Path) -> str:
        """Read and return the content of a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def search(self, query: str, subject_filter: str = "all", max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search the knowledge base using semantic similarity.
        
        Args:
            query (str): The search query
            subject_filter (str): Filter by subject ('math', 'english', or 'all')
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of relevant knowledge base entries with similarity scores
        """
        try:
            # Create where clause for subject filtering
            where_clause = None
            if subject_filter in ["math", "english"]:
                where_clause = {"subject": subject_filter}
            
            # Generate query embedding using Gemini
            query_embedding = self._generate_query_embedding(query)
            
            # Perform semantic search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=max_results,
                where=where_clause
            )
            
            # Format results
            formatted_results = []
            if results['documents'][0]:  # Check if we have results
                for i in range(len(results['documents'][0])):
                    formatted_result = {
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "similarity_score": 1 - results['distances'][0][i],  # Convert distance to similarity
                        "title": results['metadatas'][0][i].get('title', 'Unknown'),
                        "subject": results['metadatas'][0][i].get('subject', 'Unknown'),
                        "type": results['metadatas'][0][i].get('type', 'Unknown'),
                        "file_path": results['metadatas'][0][i].get('file_path', 'Unknown')
                    }
                    formatted_results.append(formatted_result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def get_relevant_context(self, query: str, subject_filter: str = "all", max_context_length: int = 2000) -> str:
        """
        Get relevant context for a query, formatted for use in prompts.
        
        Args:
            query (str): The search query
            subject_filter (str): Filter by subject
            max_context_length (int): Maximum length of context to return
            
        Returns:
            str: Formatted context string
        """
        results = self.search(query, subject_filter, max_results=3)
        
        if not results:
            return "No relevant information found in the knowledge base."
        
        context_parts = []
        current_length = 0
        
        for result in results:
            source_info = f"Source: {result['title']} ({result['subject']}, {result['type']})"
            content = result['content']
            
            # Truncate content if it would exceed max length
            available_length = max_context_length - current_length - len(source_info) - 10  # Buffer
            if available_length > 100:  # Only include if we have reasonable space
                if len(content) > available_length:
                    content = content[:available_length] + "..."
                
                context_parts.append(f"{source_info}\n{content}")
                current_length += len(source_info) + len(content) + 10
            
            if current_length >= max_context_length:
                break
        
        return "\n\n---\n\n".join(context_parts)
    
    def rebuild_index(self):
        """Rebuild the entire knowledge index (useful when content is updated)."""
        print("Rebuilding knowledge index...")
        
        # Delete existing collection
        try:
            self.chroma_client.delete_collection(name=self.collection_name)
        except:
            pass
        
        # Create new collection and rebuild index
        self.collection = self.chroma_client.create_collection(name=self.collection_name)
        self._build_knowledge_index()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection_name,
                "embedding_model": "text-embedding-004 (Gemini)"
            }
        except Exception as e:
            return {"error": str(e)}

# Utility function for easy integration
def create_rag_system(api_key: str) -> SATKnowledgeRAG:
    """Create and return a SAT Knowledge RAG system."""
    return SATKnowledgeRAG(api_key=api_key)