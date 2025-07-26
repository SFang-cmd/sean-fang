# SAT Agentic AI Tutor - System Architecture

## High-Level System Overview

The SAT Agentic AI Tutor is built on a modular architecture that separates concerns between planning, execution, memory, and knowledge management. The system demonstrates a complete agentic workflow with sophisticated RAG capabilities.

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                         │
├─────────────────────────┬───────────────────────────────────────┤
│   Main SAT Tutor App    │      Knowledge Editor App            │
│   (src/main.py)         │      (src/knowledge_editor.py)       │
│                         │                                       │
│  ┌─ Problem Solver ─┐   │  ┌─ Browse Files ─┐                  │
│  │                  │   │  │                │                  │
│  └─ Knowledge Q&A ──┘   │  └─ Edit & Save ──┘                  │
└─────────────────────────┴───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT CORE                                │
├─────────────────┬─────────────────┬─────────────────────────────┤
│    PLANNER      │    EXECUTOR     │         MEMORY              │
│  (planner.py)   │  (executor.py)  │       (memory.py)           │
│                 │                 │                             │
│ ┌─ReAct Loop──┐ │ ┌─Tool System─┐ │ ┌─Session State─┐           │
│ │ • Thought   │ │ │ • search_   │ │ │ • Conversation│           │
│ │ • Action    │ │ │   knowledge │ │ │   History     │           │
│ │ • Observation│ │ │ • calculate │ │ │ • Context     │           │
│ │ • Reflection│ │ │ • get_context│ │ │ • Preferences │           │
│ └─────────────┘ │ └─────────────┘ │ └───────────────┘           │
└─────────────────┴─────────────────┴─────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  KNOWLEDGE SYSTEM                              │
├─────────────────────────┬───────────────────────────────────────┤
│      RAG SYSTEM         │      KNOWLEDGE RETRIEVER             │
│    (rag_system.py)      │    (knowledge_retriever.py)          │
│                         │                                       │
│ ┌─ChromaDB Vector DB─┐  │ ┌─File-based Access─┐                │
│ │ • 78 SAT files     │  │ │ • Hierarchical    │                │
│ │ • Gemini embeddings│  │ │   Navigation      │                │
│ │ • Semantic search  │  │ │ • Topic indexing  │                │
│ │ • Similarity query │  │ │ • Direct file read│                │
│ └────────────────────┘  │ └───────────────────┘                │
└─────────────────────────┴───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL APIS                               │
├─────────────────────────┬───────────────────────────────────────┤
│     GEMINI API          │         KNOWLEDGE BASE               │
│                         │                                       │
│ ┌─Gemini 2.0 Flash───┐  │ ┌─78 Markdown Files─┐                │
│ │ • Planning         │  │ │ • Math (48 files) │                │
│ │ • Response gen     │  │ │ • English (30)    │                │
│ │ • Tool calling     │  │ │ • Overview + Notes│                │
│ └────────────────────┘  │ │ • Hierarchical    │                │
│                         │ └───────────────────┘                │
│ ┌─text-embedding-004─┐  │                                       │
│ │ • Vector generation│  │                                       │
│ │ • Semantic search  │  │                                       │
│ └────────────────────┘  │                                       │
└─────────────────────────┴───────────────────────────────────────┘
```

## Core Components

### 1. User Interface Layer

#### Main SAT Tutor Application (`src/main.py`)
- **Two-tab Streamlit interface**
- **Tab 1: Problem Solver** - Step-by-step SAT problem solutions
- **Tab 2: Knowledge Q&A** - Dual functionality for general concepts and specific problem analysis
- **Session management** - Persistent conversation history
- **Real-time interaction** - Immediate feedback and explanations

#### Knowledge Editor Application (`src/knowledge_editor.py`)
- **File browser** - Navigate SAT knowledge hierarchy
- **Markdown editor** - Rich text editing with live preview
- **Auto-save** - Automatic embedding updates on file changes
- **Search interface** - Find and filter knowledge files
- **Statistics dashboard** - Track knowledge base status

### 2. Agent Core

#### Planner (`src/planner.py`)
**Architecture Pattern**: ReAct (Reasoning + Acting)

```
User Query → Planner Analysis → Step-by-Step Plan
     │              │                    │
     │              ▼                    ▼
     │        Problem Type         Action Sequence
     │        Identification       [Think, Act, Observe]
     │              │                    │
     └──────────────┴────────────────────┘
                    │
                    ▼
            Structured JSON Plan
```

**Key Functions**:
- **Problem Classification**: Math vs English, complexity assessment
- **Task Decomposition**: Break complex problems into actionable steps
- **Strategy Selection**: Choose appropriate solution methods
- **Context Integration**: Incorporate relevant knowledge base content

#### Executor (`src/executor.py`)
**Tool Integration System**

```
Plan Step → Tool Selection → API Call → Result Processing
    │            │             │            │
    ▼            ▼             ▼            ▼
  Action      Available     Gemini/       Formatted
  Type        Tools         ChromaDB      Response
              
Tools Available:
• search_knowledge() - RAG semantic search
• get_context() - Retrieve specific knowledge
• calculate() - Math expression evaluation
• format_solution() - Step-by-step formatting
```

**Key Features**:
- **Dynamic tool selection** based on problem type
- **Error handling** with graceful fallbacks
- **Result aggregation** from multiple tool calls
- **Context-aware responses** using retrieved knowledge

#### Memory (`src/memory.py`)
**Persistent Session Management**

```
Conversation Flow:
┌─User Input─┐ → ┌─Session State─┐ → ┌─Memory Store─┐
│            │   │               │   │             │
│ • Question │   │ • Context     │   │ • JSON Files│
│ • Feedback │   │ • History     │   │ • Conv. Log │
│ • Prefs    │   │ • User Prefs  │   │ • Progress  │
└────────────┘   └───────────────┘   └─────────────┘
```

**Memory Types**:
- **Working Memory**: Current conversation context
- **Session Memory**: Per-session conversation history  
- **Long-term Memory**: User preferences and learning progress
- **Knowledge Cache**: Frequently accessed content

### 3. Knowledge System

#### RAG System (`src/rag_system.py`)
**Retrieval-Augmented Generation Architecture**

```
Query → Embedding → Vector Search → Context Retrieval → Response
  │         │            │              │               │
  ▼         ▼            ▼              ▼               ▼
Text    Gemini     ChromaDB        Ranked         Enhanced
Input   API        Vector DB       Results        Generation

Embedding Pipeline:
Text → text-embedding-004 → 768-dim vector → ChromaDB storage
```

**Key Features**:
- **Semantic Search**: Find relevant content by meaning
- **Multi-subject Filtering**: Subject-specific queries (Math/English)
- **Similarity Ranking**: Results ranked by relevance score
- **Chunk Management**: Optimal text segmentation for embedding

#### Knowledge Retriever (`src/knowledge_retriever.py`)
**File-based Knowledge Access**

```
Knowledge Hierarchy:
┌─Subject─┐ → ┌─Domain─┐ → ┌─Skill─┐ → ┌─Files─┐
│ Math    │   │Algebra │   │Linear │   │Overview│
│ English │   │Geometry│   │Eqs    │   │Notes   │
└─────────┘   └────────┘   └───────┘   └────────┘

File Structure:
satKnowledge/
├── math/
│   ├── algebra/
│   │   ├── linear-equations-one-var/
│   │   │   ├── overview.md
│   │   │   └── study-notes.md
│   │   └── ...
│   └── ...
└── english/
    └── ...
```

### 4. External APIs and Data

#### Gemini API Integration
**Multi-model Approach**

```
┌─Gemini 2.0 Flash─┐     ┌─text-embedding-004─┐
│                  │     │                     │
│ • Planning       │     │ • Vector generation │
│ • Tool calling   │     │ • Semantic search   │
│ • Response gen   │     │ • Content embedding │
│ • Reasoning      │     │ • Query embedding   │
└──────────────────┘     └─────────────────────┘
          │                         │
          ▼                         ▼
    Text Generation              Vector Database
    & Planning                   & Similarity
```

#### Knowledge Base Design
**78 Structured SAT Files**

```
Content Organization:
Subject (2) → Domain (8) → Skill (24) → File Type (2) = 78 total files

Math Domains:
• Algebra (5 skills)
• Advanced Math (3 skills)  
• Problem-Solving & Data Analysis (7 skills)
• Geometry & Trigonometry (4 skills)

English Domains:
• Information & Ideas (3 skills)
• Craft & Structure (3 skills)
• Expression of Ideas (2 skills)
• Standard English Conventions (2 skills)

File Types per Skill:
• {skill}-overview.md - Concepts and strategies
• {skill}-study-notes.md - Detailed examples and practice
```

## Data Flow Architecture

### Primary Workflow: Problem Solving

```
1. User Input: "Solve for x: 3x + 7 = 22"
   │
   ▼
2. Planner: Analyze → Classify as Linear Equation → Create solution plan
   │
   ▼
3. Executor: search_knowledge("linear equations") → get_context() → calculate()
   │
   ▼
4. Memory: Store conversation → Update context → Track progress
   │
   ▼
5. Response: Step-by-step solution with explanations and verification
```

### Secondary Workflow: Knowledge Q&A

```
1. User Input: "How do I identify supporting evidence?"
   │
   ▼
2. RAG System: Generate embedding → Search ChromaDB → Rank results
   │
   ▼
3. Context Assembly: Retrieve relevant sections → Format for prompt
   │
   ▼
4. Generation: Gemini creates comprehensive answer using context
   │
   ▼
5. Response: Detailed guidance with strategies and examples
```

### Knowledge Management Workflow

```
1. Editor: Browse files → Select file → Edit content
   │
   ▼
2. Save: Update file → Generate new embedding → Update ChromaDB
   │
   ▼
3. Sync: Refresh knowledge retriever → Update search index
   │
   ▼
4. Validation: Test search → Verify embedding quality
```

## Scalability and Performance

### Vector Database Optimization
- **ChromaDB**: Persistent storage with HNSW indexing
- **Embedding Dimension**: 768 (Gemini text-embedding-004)
- **Search Performance**: Sub-second semantic queries
- **Storage Efficiency**: Compressed vectors with metadata

### Caching Strategy
- **Embedding Cache**: Pre-computed vectors for all knowledge files
- **Session Cache**: Conversation context and retrieved content
- **Query Cache**: Frequently accessed knowledge chunks
- **Model Cache**: Gemini API response caching for repeated queries

### Error Handling and Resilience
- **API Fallbacks**: Graceful degradation when Gemini API unavailable
- **Retry Logic**: Exponential backoff for transient failures
- **Data Validation**: Input sanitization and output verification
- **Logging**: Comprehensive error tracking and debugging

## Security and Privacy

### API Key Management
- **Environment Variables**: Secure API key storage
- **No Logging**: API keys never logged or stored in plaintext
- **Session Isolation**: Per-user session data separation

### Data Privacy
- **Local Storage**: Knowledge base and embeddings stored locally
- **No Personal Data**: System doesn't collect or store personal information
- **Memory Cleanup**: Session data cleared after timeout

## Future Extensions

### Potential Enhancements
1. **Multi-modal Support**: Image upload for SAT question screenshots
2. **Adaptive Learning**: Personalized difficulty adjustment
3. **Progress Tracking**: Long-term learning analytics
4. **Collaborative Features**: Shared knowledge base contributions
5. **Mobile Interface**: React Native app development

### Scaling Considerations
1. **Distributed ChromaDB**: Multi-node vector database
2. **API Load Balancing**: Multiple Gemini API keys
3. **Content Delivery**: CDN for knowledge base assets
4. **Database Optimization**: Advanced indexing strategies
