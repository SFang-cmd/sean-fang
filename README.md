# SAT Step-by-Step Agentic AI Tutor

An intelligent SAT tutoring system that combines agentic AI with comprehensive knowledge management. This system provides step-by-step solutions to SAT problems while maintaining a sophisticated knowledge base with semantic search capabilities.

## 🎯 Overview

This project demonstrates an **Agentic AI architecture** that:
- **Plans** multi-step solutions to SAT problems using Gemini AI
- **Executes** solutions with specialized tools and knowledge retrieval
- **Remembers** conversation context and learning progress
- **Manages** a comprehensive SAT knowledge base with ChromaDB embeddings

### Key Features

- **🧠 Intelligent Problem Solving**: Step-by-step SAT question solutions using agentic planning
- **📚 Knowledge Management**: Semantic search across 78+ SAT study files
- **✏️ Interactive Editor**: Web-based interface for editing and updating knowledge content
- **🔍 RAG System**: Retrieval-Augmented Generation with Gemini embeddings
- **💬 Dual Interface**: Problem solver + Knowledge Q&A in one application

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

5. **Initialize knowledge embeddings** (one-time setup)
```bash
python scripts/populate_embeddings.py
```

### Running the Applications

#### Main SAT Tutor Application
```bash
streamlit run src/main.py
```

#### Knowledge Editor (separate app)
```bash
streamlit run src/knowledge_editor.py
```

#### Management Tools
```bash
# Check system status
python scripts/manage_embeddings.py status

# Test search functionality  
python scripts/manage_embeddings.py test

# Rebuild embeddings
python scripts/manage_embeddings.py rebuild
```

## 🏗️ Architecture

### Core Components

```
src/
├── main.py              # Main Streamlit application (2-tab interface)
├── planner.py           # Agentic planning module (ReAct pattern)
├── executor.py          # Tool execution and coordination
├── memory.py            # Conversation memory and persistence
├── rag_system.py        # ChromaDB + Gemini embeddings
├── knowledge_retriever.py # File-based knowledge access
└── knowledge_editor.py  # Streamlit knowledge management app
```

### Agentic Workflow

1. **User Input** → SAT question or knowledge query
2. **Planning** → Gemini AI creates step-by-step solution plan
3. **Tool Execution** → Retrieves relevant knowledge, performs calculations
4. **Memory Integration** → Stores context and tracks learning progress
5. **Response Generation** → Comprehensive answer with explanations

### Gemini Integration

- **Planning**: Gemini 2.0 Flash for intelligent task decomposition
- **Embeddings**: text-embedding-004 for semantic search
- **Knowledge Retrieval**: RAG system with ChromaDB vector storage
- **Response Generation**: Context-aware tutoring responses

## 📊 Knowledge Base

- **78 Structured Files**: Complete SAT curriculum coverage
- **Hierarchical Organization**: Subject → Domain → Skills
- **Dual Content Types**: Overview + Study Notes for each topic
- **Semantic Search**: Find relevant content by meaning, not keywords

### Subjects Covered

**Mathematics**:
- Algebra (Linear equations, functions, systems)
- Advanced Math (Nonlinear functions, equivalent expressions)  
- Problem-Solving & Data Analysis (Statistics, probability)
- Geometry & Trigonometry (Area, volume, triangles)

**English**:
- Information & Ideas (Central ideas, evidence, inferences)
- Craft & Structure (Text analysis, vocabulary)
- Expression of Ideas (Rhetorical synthesis, transitions)
- Standard English Conventions (Grammar, mechanics)

## 🛠️ Usage Examples

### Problem Solving
```
Input: "Solve for x: 3x + 7 = 22"
Output: Step-by-step solution with explanations and verification
```

### Knowledge Queries
```
Input: "How do I identify supporting evidence in reading passages?"
Output: Comprehensive guidance with strategies and examples
```

### Knowledge Editing
```
1. Browse knowledge files by subject/topic
2. Edit content with live markdown preview
3. Save changes with automatic embedding updates
```

## 📋 Dependencies

### Core Requirements
```
streamlit>=1.28.0
google-genai>=0.3.0
chromadb>=0.4.0
python-dotenv>=1.0.0
pathlib
json
datetime
hashlib
```

### Development Tools
```
python>=3.9
pip
virtualenv
```

## 🧪 Testing

```bash
# Test knowledge retrieval
python -c "from src.knowledge_retriever import KnowledgeRetriever; kr = KnowledgeRetriever(); print(len(kr.get_all_topics()))"

# Test embeddings system
python scripts/manage_embeddings.py test

# Test main application (manual)
streamlit run src/main.py
```

## 📈 Performance

- **Knowledge Base**: 78 files indexed with semantic search
- **Response Time**: < 3 seconds for most queries
- **Embedding Quality**: Gemini text-embedding-004 (768 dimensions)
- **Memory Usage**: Persistent conversation history
- **Scalability**: ChromaDB supports large-scale knowledge expansion

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini API** for advanced language model capabilities
- **ChromaDB** for efficient vector storage and similarity search
- **Streamlit** for rapid web application development
- **SAT Knowledge Base** curated for comprehensive test preparation

---

**Built for the Agentic AI Hackathon** - Demonstrating intelligent tutoring through agentic planning, tool use, and knowledge management.


