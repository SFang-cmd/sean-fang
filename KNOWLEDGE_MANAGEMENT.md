# SAT Knowledge Management System

A complete system for managing SAT knowledge files with ChromaDB embeddings and a Streamlit editor interface.

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up your Gemini API key
cp example.env .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Populate Embeddings Database

First time setup - generate embeddings for all knowledge files:

```bash
python populate_embeddings.py
```

This will:
- Scan all `.md` files in `satKnowledge/`
- Generate embeddings using Gemini
- Store in ChromaDB (`./chroma_db/`)
- Provide progress updates

### 3. Launch Knowledge Editor

```bash
streamlit run knowledge_editor.py
```

This opens a web interface where you can:
- Browse all knowledge files by subject/domain/skill
- Edit markdown content with live preview
- Save changes with automatic embedding updates
- View file statistics and metadata

## 📁 File Structure

```
satKnowledge/
├── math/
│   ├── math-overview.md
│   ├── math-study-notes.md
│   ├── algebra/
│   │   ├── algebra-overview.md
│   │   ├── algebra-study-notes.md
│   │   ├── linear-equations-one-var/
│   │   │   ├── linear-equations-one-var-overview.md
│   │   │   └── linear-equations-one-var-study-notes.md
│   │   └── ...
│   └── ...
└── english/
    └── ...
```

**Naming Convention:** `{topic}-overview.md` and `{topic}-study-notes.md`

## 🛠️ Management Tools

### Check System Status
```bash
python manage_embeddings.py status
```

### Rebuild All Embeddings
```bash
python manage_embeddings.py rebuild
```

### Test Search Functionality
```bash
python manage_embeddings.py test
```

### Interactive Search
```bash
python manage_embeddings.py search
```

## 🔧 System Components

### 1. Knowledge Retriever (`src/knowledge_retriever.py`)
- Indexes all knowledge files
- Provides text-based search
- Handles hierarchical file structure

### 2. RAG System (`src/rag_system.py`)
- Creates semantic embeddings using Gemini
- Stores in ChromaDB for fast similarity search
- Supports subject filtering

### 3. Knowledge Editor (`knowledge_editor.py`)
- Streamlit web interface
- File browser with filtering
- Markdown editor with preview
- Automatic embedding updates

### 4. Management Scripts
- `populate_embeddings.py` - Initial setup
- `manage_embeddings.py` - Maintenance utilities

## 🔍 Usage Examples

### Programmatic Access

```python
from src.rag_system import SATKnowledgeRAG
import os

# Initialize
api_key = os.getenv("GEMINI_API_KEY")
rag = SATKnowledgeRAG(api_key, "satKnowledge")

# Search
results = rag.search("linear equations", subject_filter="math", max_results=5)
for result in results:
    print(f"Title: {result['title']}")
    print(f"Score: {result['similarity_score']:.3f}")
    print(f"Content: {result['content'][:100]}...")
```

### Integration with Main App

```python
# In your main SAT application
from src.rag_system import SATKnowledgeRAG

# Initialize once
rag_system = SATKnowledgeRAG(api_key, "satKnowledge")

# Use for context retrieval
def get_relevant_context(question, subject="all"):
    return rag_system.get_relevant_context(question, subject_filter=subject)
```

## 📊 Features

### Knowledge Editor Features
- 📁 **File Browser** - Hierarchical navigation by subject/domain/skill
- 🔍 **Search & Filter** - Find files by subject, type, or content
- ✏️ **Rich Editor** - Markdown editing with syntax highlighting
- 👁️ **Live Preview** - See rendered markdown in real-time
- 💾 **Auto-save** - Automatic embedding updates on save
- 📊 **Statistics** - File counts, modification dates, sizes

### Search Features
- 🔍 **Semantic Search** - Find content by meaning, not just keywords
- 🎯 **Subject Filtering** - Limit search to math or english
- 📈 **Relevance Scoring** - Results ranked by similarity
- ⚡ **Fast Retrieval** - ChromaDB for efficient vector search

### Management Features
- 🔄 **Bulk Processing** - Process all files at once
- 📊 **Status Monitoring** - Check system health and statistics
- 🧪 **Testing Tools** - Verify search functionality
- 🔧 **Maintenance** - Rebuild index, clear cache

## 🔧 Troubleshooting

### Common Issues

**No embeddings found:**
```bash
python manage_embeddings.py status
python populate_embeddings.py
```

**Search not working:**
```bash
python manage_embeddings.py test
```

**Files not loading in editor:**
- Check file permissions
- Verify knowledge base path
- Ensure files follow naming convention

**API errors:**
- Verify GEMINI_API_KEY in .env
- Check internet connection
- Monitor API rate limits

### Performance Tips

- **Initial embedding generation** takes 5-10 minutes for full knowledge base
- **Individual file updates** take 1-2 seconds
- **Search queries** return results in <100ms
- **File editing** is real-time with instant preview

## 🔐 Security Notes

- API keys are stored in `.env` (not committed to git)
- ChromaDB data is stored locally
- No external data transmission except Gemini API calls
- All file operations respect system permissions

## 📈 Monitoring

The system provides comprehensive statistics:
- Total files in knowledge base
- Number of embedded documents
- Search performance metrics
- File modification tracking
- API usage monitoring

Use `manage_embeddings.py status` for real-time system health checks.