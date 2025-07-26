"""
Knowledge Retriever Module for SAT Knowledge Base

This module handles searching, retrieving, and processing content from the
structured SAT knowledge base stored in markdown files.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

class KnowledgeRetriever:
    """
    Knowledge retriever that can search through the SAT knowledge base
    and return relevant content for questions.
    """
    
    def __init__(self, knowledge_base_path: str = "../satKnowledge"):
        """
        Initialize the knowledge retriever.
        
        Args:
            knowledge_base_path (str): Path to the SAT knowledge base directory
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_index = {}
        self._build_knowledge_index()
    
    def _build_knowledge_index(self):
        """Build an index of all knowledge base content for faster searching."""
        try:
            self.knowledge_index = {
                "math": self._index_subject("math"),
                "english": self._index_subject("english")
            }
        except Exception as e:
            print(f"Error building knowledge index: {e}")
            self.knowledge_index = {"math": {}, "english": {}}
    
    def _index_subject(self, subject: str) -> Dict[str, Any]:
        """
        Index all content for a specific subject (math or english).
        
        Args:
            subject (str): The subject to index ('math' or 'english')
            
        Returns:
            Dict[str, Any]: Indexed content for the subject
        """
        subject_path = self.knowledge_base_path / subject
        if not subject_path.exists():
            return {}
        
        subject_index = {
            "overview": None,
            "study_notes": None,
            "topics": {}
        }
        
        # Index main subject files
        overview_file = subject_path / f"{subject}-overview.md"
        if overview_file.exists():
            subject_index["overview"] = self._read_markdown_file(overview_file)
        
        study_notes_file = subject_path / f"{subject}-study-notes.md"
        if study_notes_file.exists():
            subject_index["study_notes"] = self._read_markdown_file(study_notes_file)
        
        # Index all topics and subtopics
        for topic_dir in subject_path.iterdir():
            if topic_dir.is_dir():
                topic_name = topic_dir.name
                subject_index["topics"][topic_name] = self._index_topic(topic_dir, topic_name)
        
        return subject_index
    
    def _index_topic(self, topic_path: Path, topic_name: str) -> Dict[str, Any]:
        """
        Index a specific topic directory.
        
        Args:
            topic_path (Path): Path to the topic directory
            topic_name (str): Name of the topic
            
        Returns:
            Dict[str, Any]: Indexed content for the topic
        """
        topic_index = {
            "overview": None,
            "study_notes": None,
            "metadata": None,
            "subtopics": {}
        }
        
        # Index main topic files
        for file in topic_path.iterdir():
            if file.is_file():
                if file.name.endswith("-overview.md"):
                    topic_index["overview"] = self._read_markdown_file(file)
                elif file.name.endswith("-study-notes.md"):
                    topic_index["study_notes"] = self._read_markdown_file(file)
                elif file.name == "metadata.json":
                    topic_index["metadata"] = self._read_json_file(file)
            elif file.is_dir():
                # This is a subtopic
                subtopic_name = file.name
                topic_index["subtopics"][subtopic_name] = self._index_subtopic(file, subtopic_name)
        
        return topic_index
    
    def _index_subtopic(self, subtopic_path: Path, subtopic_name: str) -> Dict[str, Any]:
        """
        Index a specific subtopic directory.
        
        Args:
            subtopic_path (Path): Path to the subtopic directory
            subtopic_name (str): Name of the subtopic
            
        Returns:
            Dict[str, Any]: Indexed content for the subtopic
        """
        subtopic_index = {
            "overview": None,
            "study_notes": None,
            "metadata": None
        }
        
        for file in subtopic_path.iterdir():
            if file.is_file():
                if file.name.endswith("-overview.md"):
                    subtopic_index["overview"] = self._read_markdown_file(file)
                elif file.name.endswith("-study-notes.md"):
                    subtopic_index["study_notes"] = self._read_markdown_file(file)
                elif file.name == "metadata.json":
                    subtopic_index["metadata"] = self._read_json_file(file)
        
        return subtopic_index
    
    def _read_markdown_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Read and parse a markdown file.
        
        Args:
            file_path (Path): Path to the markdown file
            
        Returns:
            Dict[str, Any]: Parsed markdown content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "file_path": str(file_path),
                "content": content,
                "word_count": len(content.split()),
                "sections": self._extract_sections(content)
            }
        except Exception as e:
            print(f"Error reading markdown file {file_path}: {e}")
            return {"file_path": str(file_path), "content": "", "word_count": 0, "sections": []}
    
    def _read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Read and parse a JSON file.
        
        Args:
            file_path (Path): Path to the JSON file
            
        Returns:
            Dict[str, Any]: Parsed JSON content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return {}
    
    def _extract_sections(self, markdown_content: str) -> List[Dict[str, str]]:
        """
        Extract sections from markdown content based on headers.
        
        Args:
            markdown_content (str): The markdown content
            
        Returns:
            List[Dict[str, str]]: List of sections with headers and content
        """
        sections = []
        lines = markdown_content.split('\n')
        current_section = {"header": "", "content": ""}
        
        for line in lines:
            if line.startswith('#'):
                # New section found
                if current_section["content"].strip():
                    sections.append(current_section.copy())
                current_section = {
                    "header": line.strip(),
                    "content": ""
                }
            else:
                current_section["content"] += line + "\n"
        
        # Add the last section
        if current_section["content"].strip():
            sections.append(current_section)
        
        return sections
    
    def search_knowledge_base(self, query: str, subject_filter: str = "all", max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for relevant content.
        
        Args:
            query (str): The search query
            subject_filter (str): Filter by subject ('math', 'english', or 'all')
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of relevant knowledge base entries
        """
        results = []
        query_lower = query.lower()
        
        # Determine which subjects to search
        subjects_to_search = []
        if subject_filter == "all":
            subjects_to_search = ["math", "english"]
        elif subject_filter in ["math", "english"]:
            subjects_to_search = [subject_filter]
        
        for subject in subjects_to_search:
            if subject in self.knowledge_index:
                subject_results = self._search_subject(query_lower, subject, self.knowledge_index[subject])
                results.extend(subject_results)
        
        # Sort results by relevance score and return top results
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return results[:max_results]
    
    def _search_subject(self, query: str, subject: str, subject_index: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search within a specific subject.
        
        Args:
            query (str): The search query (lowercase)
            subject (str): The subject being searched
            subject_index (Dict[str, Any]): The subject's index
            
        Returns:
            List[Dict[str, Any]]: List of relevant results from this subject
        """
        results = []
        
        # Search main subject files
        if subject_index.get("overview"):
            score = self._calculate_relevance_score(query, subject_index["overview"]["content"])
            if score > 0:
                results.append({
                    "subject": subject,
                    "type": "overview",
                    "title": f"{subject.capitalize()} Overview",
                    "content": subject_index["overview"]["content"],
                    "file_path": subject_index["overview"]["file_path"],
                    "relevance_score": score
                })
        
        if subject_index.get("study_notes"):
            score = self._calculate_relevance_score(query, subject_index["study_notes"]["content"])
            if score > 0:
                results.append({
                    "subject": subject,
                    "type": "study_notes",
                    "title": f"{subject.capitalize()} Study Notes",
                    "content": subject_index["study_notes"]["content"],
                    "file_path": subject_index["study_notes"]["file_path"],
                    "relevance_score": score
                })
        
        # Search topics and subtopics
        for topic_name, topic_data in subject_index.get("topics", {}).items():
            topic_results = self._search_topic(query, subject, topic_name, topic_data)
            results.extend(topic_results)
        
        return results
    
    def _search_topic(self, query: str, subject: str, topic_name: str, topic_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search within a specific topic.
        
        Args:
            query (str): The search query (lowercase)
            subject (str): The subject name
            topic_name (str): The topic name
            topic_data (Dict[str, Any]): The topic's indexed data
            
        Returns:
            List[Dict[str, Any]]: List of relevant results from this topic
        """
        results = []
        
        # Search topic files
        if topic_data.get("overview"):
            score = self._calculate_relevance_score(query, topic_data["overview"]["content"])
            if score > 0:
                results.append({
                    "subject": subject,
                    "topic": topic_name,
                    "type": "topic_overview",
                    "title": f"{topic_name.replace('-', ' ').title()} Overview",
                    "content": topic_data["overview"]["content"],
                    "file_path": topic_data["overview"]["file_path"],
                    "relevance_score": score
                })
        
        if topic_data.get("study_notes"):
            score = self._calculate_relevance_score(query, topic_data["study_notes"]["content"])
            if score > 0:
                results.append({
                    "subject": subject,
                    "topic": topic_name,
                    "type": "topic_notes",
                    "title": f"{topic_name.replace('-', ' ').title()} Study Notes",
                    "content": topic_data["study_notes"]["content"],
                    "file_path": topic_data["study_notes"]["file_path"],
                    "relevance_score": score
                })
        
        # Search subtopics
        for subtopic_name, subtopic_data in topic_data.get("subtopics", {}).items():
            subtopic_results = self._search_subtopic(query, subject, topic_name, subtopic_name, subtopic_data)
            results.extend(subtopic_results)
        
        return results
    
    def _search_subtopic(self, query: str, subject: str, topic_name: str, subtopic_name: str, subtopic_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search within a specific subtopic.
        
        Args:
            query (str): The search query (lowercase)
            subject (str): The subject name
            topic_name (str): The topic name
            subtopic_name (str): The subtopic name
            subtopic_data (Dict[str, Any]): The subtopic's indexed data
            
        Returns:
            List[Dict[str, Any]]: List of relevant results from this subtopic
        """
        results = []
        
        if subtopic_data.get("overview"):
            score = self._calculate_relevance_score(query, subtopic_data["overview"]["content"])
            if score > 0:
                results.append({
                    "subject": subject,
                    "topic": topic_name,
                    "subtopic": subtopic_name,
                    "type": "subtopic_overview",
                    "title": f"{subtopic_name.replace('-', ' ').title()} Overview",
                    "content": subtopic_data["overview"]["content"],
                    "file_path": subtopic_data["overview"]["file_path"],
                    "relevance_score": score
                })
        
        if subtopic_data.get("study_notes"):
            score = self._calculate_relevance_score(query, subtopic_data["study_notes"]["content"])
            if score > 0:
                results.append({
                    "subject": subject,
                    "topic": topic_name,
                    "subtopic": subtopic_name,
                    "type": "subtopic_notes",
                    "title": f"{subtopic_name.replace('-', ' ').title()} Study Notes",
                    "content": subtopic_data["study_notes"]["content"],
                    "file_path": subtopic_data["study_notes"]["file_path"],
                    "relevance_score": score
                })
        
        return results
    
    def _calculate_relevance_score(self, query: str, content: str) -> float:
        """
        Calculate a simple relevance score for content based on query.
        
        Args:
            query (str): The search query (lowercase)
            content (str): The content to score
            
        Returns:
            float: Relevance score (higher is more relevant)
        """
        if not content:
            return 0.0
        
        content_lower = content.lower()
        query_words = query.split()
        
        score = 0.0
        total_words = len(content.split())
        
        # Count exact query matches (higher weight)
        exact_matches = content_lower.count(query)
        score += exact_matches * 10
        
        # Count individual word matches
        for word in query_words:
            if len(word) > 2:  # Ignore very short words
                word_matches = content_lower.count(word)
                score += word_matches * 2
        
        # Normalize by content length to favor more focused content
        if total_words > 0:
            score = score / (total_words / 100)  # Normalize per 100 words
        
        return score
    
    def get_topic_content(self, subject: str, topic: str, subtopic: str = None) -> Optional[Dict[str, Any]]:
        """
        Get specific content for a topic or subtopic.
        
        Args:
            subject (str): The subject ('math' or 'english')
            topic (str): The topic name
            subtopic (str, optional): The subtopic name
            
        Returns:
            Optional[Dict[str, Any]]: The requested content or None if not found
        """
        try:
            if subject not in self.knowledge_index:
                return None
            
            subject_data = self.knowledge_index[subject]
            if topic not in subject_data.get("topics", {}):
                return None
            
            topic_data = subject_data["topics"][topic]
            
            if subtopic:
                if subtopic not in topic_data.get("subtopics", {}):
                    return None
                return topic_data["subtopics"][subtopic]
            else:
                return topic_data
                
        except Exception as e:
            print(f"Error getting topic content: {e}")
            return None
    
    def get_all_topics(self, subject: str = "all") -> Dict[str, List[str]]:
        """
        Get a list of all available topics.
        
        Args:
            subject (str): Filter by subject ('math', 'english', or 'all')
            
        Returns:
            Dict[str, List[str]]: Dictionary mapping subjects to their topics
        """
        topics = {}
        
        subjects_to_check = []
        if subject == "all":
            subjects_to_check = ["math", "english"]
        elif subject in ["math", "english"]:
            subjects_to_check = [subject]
        
        for subj in subjects_to_check:
            if subj in self.knowledge_index:
                topics[subj] = list(self.knowledge_index[subj].get("topics", {}).keys())
        
        return topics