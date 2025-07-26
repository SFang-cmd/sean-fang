#!/usr/bin/env python3
"""
Script to create nested folder structure for SAT Knowledge based on the SAT_STRUCTURE.
"""

import os
import json
from pathlib import Path

# Base directory
base_dir = Path("/Users/sean/Documents/code/hackathons/odscGoogle2025/sean-fang/satKnowledge")

# SAT Structure from the provided dictionary
sat_structure = {
  "math": {
    "name": "Math",
    "description": "Mathematical reasoning and problem-solving",
    "domains": [
      {
        "id": "algebra",
        "name": "Algebra",
        "description": "Linear equations, functions, and systems",
        "skills": [
          {
            "id": "linear-equations-one-var",
            "name": "Linear Equations in One Variable"
          },
          {
            "id": "linear-functions",
            "name": "Linear Functions"
          },
          {
            "id": "linear-equations-two-var",
            "name": "Linear Equations in Two Variables"
          },
          {
            "id": "systems-linear-equations",
            "name": "Systems of Two Linear Equations in Two Variables"
          },
          {
            "id": "linear-inequalities",
            "name": "Linear Inequalities in One or Two Variables"
          }
        ]
      },
      {
        "id": "advanced-math",
        "name": "Advanced Math",
        "description": "Nonlinear functions and complex equations",
        "skills": [
          {
            "id": "nonlinear-functions",
            "name": "Nonlinear Functions"
          },
          {
            "id": "nonlinear-equations-systems",
            "name": "Nonlinear Equations in One Variable & Systems of Equations in Two Variables"
          },
          {
            "id": "equivalent-expressions",
            "name": "Equivalent Expressions"
          }
        ]
      },
      {
        "id": "problem-solving-data-analysis",
        "name": "Problem-Solving & Data Analysis",
        "description": "Statistics, probability, and data interpretation",
        "skills": [
          {
            "id": "ratios-rates-proportions",
            "name": "Ratios, Rates, Proportional Relationships, & Units"
          },
          {
            "id": "percentages",
            "name": "Percentages"
          },
          {
            "id": "one-variable-data",
            "name": "One-Variable Data: Distributions & Measures of Center & Spread"
          },
          {
            "id": "two-variable-data",
            "name": "Two-Variable Data: Models & Scatterplots"
          },
          {
            "id": "probability-conditional",
            "name": "Probability & Conditional Probability"
          },
          {
            "id": "inference-statistics",
            "name": "Inference from Sample Statistics & Margin of Error"
          },
          {
            "id": "statistical-claims",
            "name": "Evaluating Statistical Claims: Observational Studies & Experiments"
          }
        ]
      },
      {
        "id": "geometry-trigonometry",
        "name": "Geometry & Trigonometry",
        "description": "Spatial reasoning and trigonometric relationships",
        "skills": [
          {
            "id": "area-volume",
            "name": "Area & Volume"
          },
          {
            "id": "lines-angles-triangles",
            "name": "Lines, Angles, & Triangles"
          },
          {
            "id": "right-triangles-trigonometry",
            "name": "Right Triangles & Trigonometry"
          },
          {
            "id": "circles",
            "name": "Circles"
          }
        ]
      }
    ]
  },
  "english": {
    "name": "English",
    "description": "Reading comprehension and language conventions",
    "domains": [
      {
        "id": "information-ideas",
        "name": "Information & Ideas",
        "description": "Reading comprehension and analysis",
        "skills": [
          {
            "id": "central-ideas-details",
            "name": "Central Ideas & Details"
          },
          {
            "id": "inferences",
            "name": "Inferences"
          },
          {
            "id": "command-evidence",
            "name": "Command of Evidence"
          }
        ]
      },
      {
        "id": "craft-structure",
        "name": "Craft & Structure",
        "description": "Text analysis and rhetorical skills",
        "skills": [
          {
            "id": "words-in-context",
            "name": "Words in Context"
          },
          {
            "id": "text-structure-purpose",
            "name": "Text Structure & Purpose"
          },
          {
            "id": "cross-text-connections",
            "name": "Cross-Text Connections"
          }
        ]
      },
      {
        "id": "expression-ideas",
        "name": "Expression of Ideas",
        "description": "Writing and rhetorical effectiveness",
        "skills": [
          {
            "id": "rhetorical-synthesis",
            "name": "Rhetorical Synthesis"
          },
          {
            "id": "transitions",
            "name": "Transitions"
          }
        ]
      },
      {
        "id": "standard-english-conventions",
        "name": "Standard English Conventions",
        "description": "Grammar, usage, and mechanics",
        "skills": [
          {
            "id": "boundaries",
            "name": "Boundaries"
          },
          {
            "id": "form-structure-sense",
            "name": "Form, Structure, and Sense"
          }
        ]
      }
    ]
  }
}

# Function to create markdown files for a given folder
def create_markdown_files(folder_path, topic_name):
    """
    Create StudyNotes and Overview markdown files for the given folder
    
    Args:
        folder_path (Path): Path to the folder
        topic_name (str): Name of the topic for the files
    """
    # Create StudyNotes markdown file
    study_notes_path = folder_path / f"{topic_name}StudyNotes.md"
    with open(study_notes_path, "w") as f:
        f.write(f"# {topic_name} Study Notes\n\n")
        f.write(f"## Key Concepts\n\n")
        f.write(f"- \n\n")
        f.write(f"## Formulas and Rules\n\n")
        f.write(f"- \n\n")
        f.write(f"## Common Mistakes to Avoid\n\n")
        f.write(f"- \n\n")
        f.write(f"## Practice Tips\n\n")
        f.write(f"- \n\n")
    
    # Create Overview markdown file
    overview_path = folder_path / f"{topic_name}Overview.md"
    with open(overview_path, "w") as f:
        f.write(f"# {topic_name} Overview\n\n")
        f.write(f"## Introduction\n\n")
        f.write(f"This section covers key concepts in {topic_name}.\n\n")
        f.write(f"## Subtopics\n\n")
        f.write(f"- \n\n")
        f.write(f"## Resources\n\n")
        f.write(f"- \n\n")

# Create domain and skill folders along with markdown files
created_folders = []
created_files = []

for subject_id, subject_data in sat_structure.items():
    subject_path = base_dir / subject_id
    
    # Ensure the subject folder exists
    subject_path.mkdir(exist_ok=True)
    
    # Create markdown files for the subject
    create_markdown_files(subject_path, subject_data["name"])
    created_files.append(str(subject_path / f"{subject_data['name']}StudyNotes.md"))
    created_files.append(str(subject_path / f"{subject_data['name']}Overview.md"))
    
    # Create a metadata file for the subject
    with open(subject_path / "metadata.json", "w") as f:
        json.dump({
            "id": subject_id,
            "name": subject_data["name"],
            "description": subject_data["description"]
        }, f, indent=2)
    
    # Create domain folders
    for domain in subject_data["domains"]:
        domain_path = subject_path / domain["id"]
        domain_path.mkdir(exist_ok=True)
        created_folders.append(str(domain_path))
        
        # Create markdown files for the domain
        create_markdown_files(domain_path, domain["name"])
        created_files.append(str(domain_path / f"{domain['name']}StudyNotes.md"))
        created_files.append(str(domain_path / f"{domain['name']}Overview.md"))
        
        # Create a metadata file for the domain
        with open(domain_path / "metadata.json", "w") as f:
            json.dump({
                "id": domain["id"],
                "name": domain["name"],
                "description": domain["description"]
            }, f, indent=2)
        
        # Create skill folders
        for skill in domain["skills"]:
            skill_path = domain_path / skill["id"]
            skill_path.mkdir(exist_ok=True)
            created_folders.append(str(skill_path))
            
            # Create markdown files for the skill
            create_markdown_files(skill_path, skill["name"])
            created_files.append(str(skill_path / f"{skill['name']}StudyNotes.md"))
            created_files.append(str(skill_path / f"{skill['name']}Overview.md"))
            
            # Create a metadata file for the skill
            with open(skill_path / "metadata.json", "w") as f:
                json.dump({
                    "id": skill["id"],
                    "name": skill["name"]
                }, f, indent=2)

print(f"Created {len(created_folders)} folders:")
for folder in created_folders[:5]:  # Show only first 5 folders
    print(f"  - {folder}")
if len(created_folders) > 5:
    print(f"  - ... and {len(created_folders) - 5} more")

print(f"\nCreated {len(created_files)} markdown files:")
for file in created_files[:5]:  # Show only first 5 files
    print(f"  - {file}")
if len(created_files) > 5:
    print(f"  - ... and {len(created_files) - 5} more")
