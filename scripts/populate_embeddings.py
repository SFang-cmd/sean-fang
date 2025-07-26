#!/usr/bin/env python3
"""
SAT Knowledge Base Embedding Population Script

This script scans all SAT knowledge files and creates embeddings for them
in ChromaDB using the Gemini embedding model.
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
import sys

# Add project root to Python path to allow importing from src
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.rag_system import SATKnowledgeRAG

# Load environment variables
load_dotenv()

def main():
    """Main function to populate embeddings"""
    print("🚀 SAT Knowledge Base Embedding Population Script")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("💡 Please set your Gemini API key in the .env file")
        return
    
    # Configuration
    knowledge_base_path = "satKnowledge"
    collection_name = "sat_knowledge"
    
    print(f"📁 Knowledge Base Path: {knowledge_base_path}")
    print(f"🗄️  Collection Name: {collection_name}")
    print(f"🤖 Using Gemini API for embeddings")
    print()
    
    # Check if knowledge base exists
    if not Path(knowledge_base_path).exists():
        print(f"❌ Error: Knowledge base directory '{knowledge_base_path}' not found")
        return
    
    # Count files first
    print("📊 Scanning knowledge base...")
    total_files = 0
    for subject in ['math', 'english']:
        subject_path = Path(knowledge_base_path) / subject
        if subject_path.exists():
            file_count = len(list(subject_path.glob('**/*.md')))
            print(f"   {subject.title()}: {file_count} markdown files")
            total_files += file_count
    
    print(f"📈 Total files to process: {total_files}")
    print()
    
    if total_files == 0:
        print("⚠️  No markdown files found in knowledge base")
        return
    
    # Confirm before proceeding
    response = input("🤔 Do you want to proceed with embedding generation? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("👋 Operation cancelled")
        return
    
    print("\n🔄 Initializing RAG system...")
    start_time = time.time()
    
    try:
        # Initialize the RAG system (this will automatically build the index)
        rag_system = SATKnowledgeRAG(
            api_key=api_key,
            knowledge_base_path=knowledge_base_path,
            collection_name=collection_name
        )
        
        # Get statistics
        stats = rag_system.get_stats()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n✅ Embedding generation completed!")
        print("=" * 60)
        print(f"⏱️  Total time: {duration:.2f} seconds")
        print(f"📊 Documents in collection: {stats.get('total_documents', 'Unknown')}")
        print(f"🔧 Embedding model: {stats.get('embedding_model', 'Unknown')}")
        print()
        
        # Test the system
        print("🧪 Testing the embedding system...")
        test_queries = [
            "linear equations",
            "command of evidence",
            "trigonometry",
            "central ideas"
        ]
        
        for query in test_queries:
            results = rag_system.search(query, max_results=2)
            print(f"   Query: '{query}' → {len(results)} results found")
        
        print("\n🎉 System is ready for use!")
        print("💡 You can now use the knowledge_editor.py to edit files")
        print("💡 The main SAT application will have access to semantic search")
        
    except Exception as e:
        print(f"\n❌ Error during embedding generation: {e}")
        print("💡 Please check your API key and network connection")
        return

def show_help():
    """Show help information"""
    print("SAT Knowledge Base Embedding Population Script")
    print()
    print("This script creates embeddings for all SAT knowledge files using Gemini.")
    print()
    print("Prerequisites:")
    print("1. Set GEMINI_API_KEY in your .env file")
    print("2. Ensure satKnowledge/ directory exists with markdown files")
    print("3. Install required dependencies (google-genai, chromadb)")
    print()
    print("Usage:")
    print("  python populate_embeddings.py")
    print("  python populate_embeddings.py --help")
    print()
    print("The script will:")
    print("• Scan all .md files in satKnowledge/")
    print("• Generate embeddings using Gemini text-embedding-004")
    print("• Store embeddings in ChromaDB (./chroma_db/)")
    print("• Provide progress updates and final statistics")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        show_help()
    else:
        main()