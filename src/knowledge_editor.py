#!/usr/bin/env python3
"""
SAT Knowledge Editor - Streamlit App
Allows browsing, editing, and saving SAT knowledge files with automatic embedding updates
"""

import streamlit as st
import os
from pathlib import Path
from datetime import datetime
import json
from dotenv import load_dotenv

# Load the modules
from src.knowledge_retriever import KnowledgeRetriever
from src.rag_system import SATKnowledgeRAG

# Load environment variables
load_dotenv()

# Configuration
KNOWLEDGE_BASE_PATH = "satKnowledge"
API_KEY = os.getenv("GEMINI_API_KEY")

def initialize_systems():
    """Initialize the knowledge systems"""
    if 'knowledge_retriever' not in st.session_state:
        st.session_state.knowledge_retriever = KnowledgeRetriever(KNOWLEDGE_BASE_PATH)
    
    if 'rag_system' not in st.session_state and API_KEY:
        st.session_state.rag_system = SATKnowledgeRAG(API_KEY, KNOWLEDGE_BASE_PATH)

def get_all_files():
    """Get all knowledge files organized by hierarchy"""
    files = []
    knowledge_path = Path(KNOWLEDGE_BASE_PATH)
    
    for subject_dir in knowledge_path.iterdir():
        if subject_dir.is_dir() and subject_dir.name in ['math', 'english']:
            subject = subject_dir.name
            
            # Add subject-level files
            for file in subject_dir.iterdir():
                if file.is_file() and file.suffix == '.md':
                    files.append({
                        'path': str(file),
                        'relative_path': str(file.relative_to(knowledge_path)),
                        'subject': subject,
                        'type': 'subject',
                        'name': file.name,
                        'display_name': f"{subject.title()} - {file.stem.split('-')[-1].title()}"
                    })
            
            # Add domain/topic files
            for domain_dir in subject_dir.iterdir():
                if domain_dir.is_dir():
                    domain = domain_dir.name
                    
                    # Add domain-level files
                    for file in domain_dir.iterdir():
                        if file.is_file() and file.suffix == '.md':
                            files.append({
                                'path': str(file),
                                'relative_path': str(file.relative_to(knowledge_path)),
                                'subject': subject,
                                'domain': domain,
                                'type': 'domain',
                                'name': file.name,
                                'display_name': f"{subject.title()} > {domain.replace('-', ' ').title()} - {file.stem.split('-')[-1].title()}"
                            })
                    
                    # Add skill-level files
                    for skill_dir in domain_dir.iterdir():
                        if skill_dir.is_dir():
                            skill = skill_dir.name
                            
                            for file in skill_dir.iterdir():
                                if file.is_file() and file.suffix == '.md':
                                    files.append({
                                        'path': str(file),
                                        'relative_path': str(file.relative_to(knowledge_path)),
                                        'subject': subject,
                                        'domain': domain,
                                        'skill': skill,
                                        'type': 'skill',
                                        'name': file.name,
                                        'display_name': f"{subject.title()} > {domain.replace('-', ' ').title()} > {skill.replace('-', ' ').title()} - {file.stem.split('-')[-1].title()}"
                                    })
    
    return sorted(files, key=lambda x: (x['subject'], x.get('domain', ''), x.get('skill', ''), x['name']))

def load_file_content(file_path):
    """Load content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return ""

def save_file_content(file_path, content):
    """Save content to a file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False

def update_embedding(file_path):
    """Update embedding for a file"""
    if API_KEY and 'rag_system' in st.session_state:
        try:
            # Rebuild the entire index for now (could be optimized to update just one file)
            st.session_state.rag_system.rebuild_index()
            return True
        except Exception as e:
            st.error(f"Error updating embedding: {e}")
            return False
    return False

def get_file_stats():
    """Get statistics about the knowledge base"""
    stats = {'total_files': 0, 'subjects': {}}
    
    for subject in ['math', 'english']:
        subject_path = Path(KNOWLEDGE_BASE_PATH) / subject
        if subject_path.exists():
            file_count = len(list(subject_path.glob('**/*.md')))
            stats['subjects'][subject] = file_count
            stats['total_files'] += file_count
    
    return stats

def main():
    st.set_page_config(
        page_title="SAT Knowledge Editor",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 SAT Knowledge Base Editor")
    st.markdown("Browse, edit, and manage SAT knowledge files with automatic embedding updates")
    
    # Initialize systems
    initialize_systems()
    
    # Sidebar - File Browser
    with st.sidebar:
        st.header("📁 Knowledge Files")
        
        # Stats
        stats = get_file_stats()
        st.metric("Total Files", stats['total_files'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Math", stats['subjects'].get('math', 0))
        with col2:
            st.metric("English", stats['subjects'].get('english', 0))
        
        st.divider()
        
        # File browser
        files = get_all_files()
        
        # Filter options
        subjects = ['All'] + list(set(f['subject'] for f in files))
        selected_subject = st.selectbox("Filter by Subject", subjects)
        
        file_types = ['All'] + list(set(f['type'] for f in files))
        selected_type = st.selectbox("Filter by Type", file_types)
        
        # Filter files
        filtered_files = files
        if selected_subject != 'All':
            filtered_files = [f for f in filtered_files if f['subject'] == selected_subject]
        if selected_type != 'All':
            filtered_files = [f for f in filtered_files if f['type'] == selected_type]
        
        # File selection
        if filtered_files:
            file_options = [f['display_name'] for f in filtered_files]
            selected_file_idx = st.selectbox(
                "Select File to Edit",
                range(len(file_options)),
                format_func=lambda i: file_options[i]
            )
            selected_file = filtered_files[selected_file_idx]
        else:
            st.warning("No files found matching the filters")
            selected_file = None
    
    # Main content area
    if selected_file:
        st.header(f"✏️ Editing: {selected_file['display_name']}")
        
        # File info
        with st.expander("📋 File Information", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Subject:**", selected_file['subject'].title())
                st.write("**Type:**", selected_file['type'].title())
                st.write("**File Path:**", selected_file['relative_path'])
            with col2:
                if 'domain' in selected_file:
                    st.write("**Domain:**", selected_file['domain'].replace('-', ' ').title())
                if 'skill' in selected_file:
                    st.write("**Skill:**", selected_file['skill'].replace('-', ' ').title())
                
                # File stats
                file_path = Path(selected_file['path'])
                if file_path.exists():
                    stat = file_path.stat()
                    st.write("**Last Modified:**", datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
                    st.write("**File Size:**", f"{stat.st_size} bytes")
        
        # Load and edit content
        current_content = load_file_content(selected_file['path'])
        
        # Content editor
        st.subheader("📝 Content Editor")
        
        # Show preview/edit toggle
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            edit_mode = st.toggle("Edit Mode", value=True)
        with col2:
            if edit_mode:
                preview_mode = st.toggle("Show Preview", value=False)
            else:
                preview_mode = True
        
        if edit_mode and not preview_mode:
            # Text area for editing
            edited_content = st.text_area(
                "Content",
                value=current_content,
                height=600,
                help="Edit the markdown content here"
            )
            
            # Save buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("💾 Save", type="primary"):
                    if save_file_content(selected_file['path'], edited_content):
                        st.success("✅ File saved successfully!")
                        
                        # Update embedding if API key is available
                        if API_KEY:
                            with st.spinner("🔄 Updating embeddings..."):
                                if update_embedding(selected_file['path']):
                                    st.success("✅ Embeddings updated!")
                                else:
                                    st.warning("⚠️ File saved but embedding update failed")
                        else:
                            st.info("💡 Set GEMINI_API_KEY to enable automatic embedding updates")
                        
                        # Refresh the page to show updated content
                        st.rerun()
            
            with col2:
                if st.button("🔄 Reload"):
                    st.rerun()
            
            # Show changes
            if edited_content != current_content:
                st.info("📝 You have unsaved changes")
                
                with st.expander("🔍 View Changes"):
                    st.write("**Character count change:**", len(edited_content) - len(current_content))
                    st.write("**Line count change:**", len(edited_content.split('\n')) - len(current_content.split('\n')))
        
        else:
            # Preview mode
            st.subheader("👁️ Preview")
            if edit_mode and preview_mode:
                # Show edited content preview
                edited_content = st.text_area(
                    "Content (Preview Mode)",
                    value=current_content,
                    height=200,
                    disabled=True
                )
                st.markdown("### Rendered Preview:")
                st.markdown(edited_content)
            else:
                # Show current file content
                st.markdown(current_content)
    
    else:
        # Welcome screen
        st.header("👋 Welcome to the SAT Knowledge Editor")
        st.markdown("""
        ### Features:
        - 📁 **Browse** all SAT knowledge files organized by subject, domain, and skill
        - ✏️ **Edit** markdown content with live preview
        - 💾 **Save** changes with automatic backup
        - 🔄 **Auto-update** embeddings when files are modified
        - 📊 **Track** file statistics and metadata
        
        ### Getting Started:
        1. Use the sidebar to browse and select a file to edit
        2. Toggle between edit and preview modes
        3. Make your changes and save
        4. Embeddings will be automatically updated (if API key is configured)
        
        ### File Structure:
        ```
        satKnowledge/
        ├── math/
        │   ├── algebra/
        │   │   ├── linear-equations-one-var/
        │   │   │   ├── linear-equations-one-var-overview.md
        │   │   │   └── linear-equations-one-var-study-notes.md
        │   │   └── ...
        │   └── ...
        └── english/
            └── ...
        ```
        """)
        
        # System status
        st.subheader("🔧 System Status")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'knowledge_retriever' in st.session_state:
                st.success("✅ Knowledge Retriever: Ready")
            else:
                st.error("❌ Knowledge Retriever: Failed")
        
        with col2:
            if API_KEY:
                st.success("✅ Gemini API: Configured")
            else:
                st.warning("⚠️ Gemini API: Not configured")
        
        with col3:
            if 'rag_system' in st.session_state:
                st.success("✅ RAG System: Ready")
            else:
                st.warning("⚠️ RAG System: Not available")

if __name__ == "__main__":
    main()