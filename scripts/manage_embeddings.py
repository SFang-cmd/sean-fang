#!/usr/bin/env python3
"""
SAT Knowledge Base Embedding Management Script

Utility script to check status, rebuild, and manage the embedding database.
"""

import os
import sys
import time
from pathlib import Path

# Add parent directory to Python path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.rag_system import SATKnowledgeRAG

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def check_status():
    """Check the status of the embedding system"""
    print("🔍 Checking embedding system status...")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✅ Gemini API key: Configured")
    else:
        print("❌ Gemini API key: Not found")
        return
    
    # Check knowledge base
    knowledge_base_path = "satKnowledge"
    if Path(knowledge_base_path).exists():
        print(f"✅ Knowledge base: Found at {knowledge_base_path}")
    else:
        print(f"❌ Knowledge base: Not found at {knowledge_base_path}")
        return
    
    # Check ChromaDB
    chroma_path = Path("chroma_db")
    if chroma_path.exists():
        print("✅ ChromaDB: Database directory exists")
    else:
        print("❌ ChromaDB: Database directory not found")
    
    # Initialize RAG system and get stats
    try:
        rag_system = SATKnowledgeRAG(api_key, knowledge_base_path)
        stats = rag_system.get_stats()
        
        print(f"✅ RAG System: Initialized successfully")
        print(f"📊 Total documents: {stats.get('total_documents', 0)}")
        print(f"🔧 Embedding model: {stats.get('embedding_model', 'Unknown')}")
        print(f"🗂️  Collection: {stats.get('collection_name', 'Unknown')}")
        
        # Count actual files
        total_files = 0
        for subject in ['math', 'english']:
            subject_path = Path(knowledge_base_path) / subject
            if subject_path.exists():
                file_count = len(list(subject_path.glob('**/*.md')))
                total_files += file_count
        
        print(f"📁 Markdown files in knowledge base: {total_files}")
        
        # Check if all files are embedded
        embedded_count = stats.get('total_documents', 0)
        if embedded_count >= total_files:
            print("✅ All files appear to be embedded")
        else:
            print(f"⚠️  Missing embeddings: {total_files - embedded_count} files")
            
    except Exception as e:
        print(f"❌ RAG System: Error - {e}")

def rebuild_index():
    """Rebuild the entire embedding index"""
    print("🔄 Rebuilding embedding index...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return
    
    knowledge_base_path = "satKnowledge"
    
    response = input("⚠️  This will delete and recreate all embeddings. Continue? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("👋 Operation cancelled")
        return
    
    try:
        print("🚀 Initializing RAG system...")
        rag_system = SATKnowledgeRAG(api_key, knowledge_base_path)
        
        print("🗑️  Rebuilding index...")
        start_time = time.time()
        rag_system.rebuild_index()
        end_time = time.time()
        
        stats = rag_system.get_stats()
        print(f"✅ Rebuild completed in {end_time - start_time:.2f} seconds")
        print(f"📊 Total documents: {stats.get('total_documents', 0)}")
        
    except Exception as e:
        print(f"❌ Error during rebuild: {e}")

def test_search():
    """Test the search functionality"""
    print("🧪 Testing search functionality...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return
    
    try:
        rag_system = SATKnowledgeRAG(api_key, "satKnowledge")
        
        test_queries = [
            ("linear equations", "math"),
            ("command of evidence", "english"),
            ("trigonometry", "math"),
            ("central ideas", "english"),
            ("probability", "math"),
            ("text structure", "english")
        ]
        
        print("🔍 Running test queries...")
        print("-" * 60)
        
        for query, subject in test_queries:
            results = rag_system.search(query, subject_filter=subject, max_results=2)
            print(f"Query: '{query}' (Subject: {subject})")
            print(f"  Results found: {len(results)}")
            
            for i, result in enumerate(results[:2]):
                score = result.get('similarity_score', 0)
                title = result.get('title', 'Unknown')
                print(f"    {i+1}. {title} (Score: {score:.3f})")
            print()
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")

def interactive_search():
    """Interactive search mode"""
    print("🔍 Interactive Search Mode")
    print("Type 'quit' to exit")
    print("-" * 30)
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return
    
    try:
        rag_system = SATKnowledgeRAG(api_key, "satKnowledge")
        
        while True:
            query = input("\n🔍 Enter search query: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            subject = input("📚 Subject filter (math/english/all): ").strip() or "all"
            
            results = rag_system.search(query, subject_filter=subject, max_results=5)
            
            if results:
                print(f"\n📊 Found {len(results)} results:")
                for i, result in enumerate(results):
                    score = result.get('similarity_score', 0)
                    title = result.get('title', 'Unknown')
                    subject = result.get('subject', 'Unknown')
                    print(f"  {i+1}. {title} ({subject}) - Score: {score:.3f}")
            else:
                print("❌ No results found")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def show_help():
    """Show help information"""
    print("SAT Knowledge Base Embedding Management")
    print("=" * 40)
    print()
    print("Commands:")
    print("  status     - Check system status and statistics")
    print("  rebuild    - Rebuild the entire embedding index")
    print("  test       - Run search tests")
    print("  search     - Interactive search mode")
    print("  help       - Show this help message")
    print()
    print("Examples:")
    print("  python manage_embeddings.py status")
    print("  python manage_embeddings.py rebuild")
    print("  python manage_embeddings.py test")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        check_status()
    elif command == "rebuild":
        rebuild_index()
    elif command == "test":
        test_search()
    elif command == "search":
        interactive_search()
    elif command in ["help", "--help", "-h"]:
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Use 'help' to see available commands")

if __name__ == "__main__":
    main()