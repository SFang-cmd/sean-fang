#!/usr/bin/env python3
"""
Script to rename all knowledge base files to a consistent naming pattern.

Converts:
- "Command of EvidenceOverview.md" -> "command-evidenceOverview.md"
- "Linear Equations in One VariableStudyNotes.md" -> "linear-equations-one-varStudyNotes.md"
"""

import os
import re
from pathlib import Path

def convert_to_kebab_case(text):
    """Convert text to kebab-case format."""
    # Remove special characters and replace with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Convert to lowercase and replace spaces with hyphens
    text = text.strip().lower().replace(' ', '-')
    return text

def rename_files_in_directory(directory):
    """Rename all markdown files in a directory to follow consistent naming."""
    directory = Path(directory)
    renamed_count = 0
    
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix == '.md':
            filename = file_path.name
            
            # Skip if already in correct format (ends with -overview.md or -study-notes.md)
            if filename.endswith('-overview.md') or filename.endswith('-study-notes.md'):
                continue
            
            # Extract the base name and determine new suffix pattern
            if filename.endswith('Overview.md'):
                base_name = filename.replace('Overview.md', '').strip()
                new_suffix = '-overview.md'
            elif filename.endswith('StudyNotes.md'):
                base_name = filename.replace('StudyNotes.md', '').strip()
                new_suffix = '-study-notes.md'
            else:
                # Skip files that don't match our pattern
                continue
            
            # Convert base name to kebab-case
            kebab_name = convert_to_kebab_case(base_name)
            new_filename = f"{kebab_name}{new_suffix}"
            
            # Rename the file
            new_path = directory / new_filename
            if new_path != file_path:  # Only rename if different
                print(f"Renaming: {filename} -> {new_filename}")
                file_path.rename(new_path)
                renamed_count += 1
    
    return renamed_count

def main():
    """Main function to rename all knowledge base files."""
    knowledge_base_path = Path("../satKnowledge")
    
    if not knowledge_base_path.exists():
        print(f"Knowledge base path not found: {knowledge_base_path}")
        return
    
    total_renamed = 0
    
    print("Renaming knowledge base files to consistent pattern...")
    print("=" * 60)
    
    # Walk through all directories in the knowledge base
    for root, dirs, files in os.walk(knowledge_base_path):
        root_path = Path(root)
        renamed_count = rename_files_in_directory(root_path)
        if renamed_count > 0:
            print(f"Directory: {root_path}")
            print(f"Renamed {renamed_count} files")
            print("-" * 40)
        total_renamed += renamed_count
    
    print(f"\nTotal files renamed: {total_renamed}")
    print("Renaming complete!")

if __name__ == "__main__":
    main()