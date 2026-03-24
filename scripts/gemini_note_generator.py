#!/usr/bin/env python3
import os
import sys
import json
import re
from google import genai
from datetime import datetime

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    issue_title = os.environ.get("ISSUE_TITLE", "")
    issue_body = os.environ.get("ISSUE_BODY", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "")
    issue_author = os.environ.get("ISSUE_AUTHOR", "")
    issue_date = datetime.now().strftime("%Y-%m-%d")

    model_name = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")

    if not issue_title:
        print("Error: ISSUE_TITLE environment variable not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a technical documentation assistant. I have a GitHub issue that needs to be converted into a detailed markdown note for my 'TechNotes' repository.

Please analyze the following issue:
Title: {issue_title}
Body: {issue_body}
Author: {issue_author}
Issue Number: {issue_number}
Date: {issue_date}

Your goal is to transform this issue into a comprehensive, well-structured technical guide.

Generate a JSON object with the following fields:
1. "category": A suggested directory name for this note (e.g., 'Networking', 'Docker', 'Linux', 'Database'). Choose an existing one if it fits, or suggest a new logical one.
2. "filename": A slugified filename ending in '.md' (e.g., 'ssh_setup.md').
3. "content": The formatted markdown content.
   - It MUST start with an H1 title (e.g., '# My Guide Title').
   - Include a brief introduction (1-2 sentences) explaining the purpose of the guide.
   - Use numbered H2 headers for main sections (e.g., '## 1. Installation', '## 2. Configuration').
   - Use H3 headers for sub-sections.
   - Provide detailed explanations, code blocks with language identifiers (bash, yaml, python, etc.), and practical examples.
   - Fix typos and improve the flow of the original issue text.
   - At the very end of the document, add a horizontal rule (---) followed by a small section:
     "**Source:** [GitHub Issue #{issue_number}](https://github.com/coltonchrane/TechNotes/issues/{issue_number}) | **Contributor:** @{issue_author}"

Return ONLY the raw JSON object. Do not wrap it in markdown code blocks like ```json ... ```.

Example Output format:
{{
  "category": "Networking",
  "filename": "ssh_setup.md",
  "content": "# SSH Server Setup\\n\\nThis guide covers...\\n\\n## 1. Installation\\n```bash\\nsudo apt install...```\\n\\n---\\n**Source:** [GitHub Issue #123]... | **Contributor:** @user1"
}}
"""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        text = response.text.strip()
        
        # In case the model still outputs markdown blocks, strip them
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        data = json.loads(text.strip())
        
        category = data.get("category", "Drafts")
        filename = data.get("filename", "note.md")
        content = data.get("content", "")

        # Extract title from H1 header
        title_match = re.search(r"^#\s*(.*?)$", content, re.MULTILINE)
        note_title = title_match.group(1).strip() if title_match else filename.replace(".md", "").replace("_", " ").title()

        # Prepend Jekyll front matter
        front_matter = f"---\nlayout: default\ntitle: {note_title}\n---\n\n"
        final_content = front_matter + content

        # Create directory if it doesn't exist
        os.makedirs(category, exist_ok=True)
        
        file_path = os.path.join(category, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        print(f"Successfully generated note at {file_path}")

        # --- index.md Table of Contents Update Logic ---
        index_path = "index.md"
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                index_content = f.read()

            # URL encode category and filename for links
            encoded_category = category.replace(" ", "%20")
            encoded_filename = filename.replace(" ", "%20")
            
            note_link = f"- [{note_title}](./{encoded_category}/{encoded_filename})"
            
            # Prevent duplicate links
            if note_link in index_content:
                print(f"Note link already exists in {index_path}. Skipping update.")
            else:
                # Check if category section exists
                category_header = f"### [{category}](./{encoded_category})"
                
                if category_header in index_content:
                    # Category exists, find the section and append the note
                    lines = index_content.split("\n")
                    new_lines = []
                    in_category = False
                    added = False
                    
                    for line in lines:
                        if category_header in line:
                            in_category = True
                            new_lines.append(line)
                            continue
                        
                        if in_category and (line.startswith("### ") or line.startswith("## ") or line.startswith("---")):
                            # Reached next section, insert before this line
                            if not added:
                                new_lines.append(note_link)
                                new_lines.append("") # add a newline before the next section
                                added = True
                            in_category = False
                        
                        new_lines.append(line)
                    
                    if in_category and not added:
                        # Reached end of file (or end of content area) while in the correct category
                        new_lines.append(note_link)
                        added = True
                    
                    updated_index_content = "\n".join(new_lines)
                else:
                    # Category doesn't exist, create a new section under ## 📖 Table of Contents
                    toc_marker = "## 📖 Table of Contents"
                    if toc_marker in index_content:
                        insertion_point = index_content.find(toc_marker) + len(toc_marker)
                        new_section = f"\n\n### [{category}](./{encoded_category})\n{note_link}"
                        updated_index_content = index_content[:insertion_point] + new_section + index_content[insertion_point:]
                    else:
                        # Fallback to appending before Features
                        features_marker = "## 🚀 Features"
                        if features_marker in index_content:
                            insertion_point = index_content.find(features_marker)
                            new_section = f"### [{category}](./{encoded_category})\n{note_link}\n\n"
                            updated_index_content = index_content[:insertion_point] + new_section + index_content[insertion_point:]
                        else:
                            updated_index_content = index_content + f"\n\n### [{category}](./{encoded_category})\n{note_link}"

                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(updated_index_content)
                print(f"Successfully updated {index_path}")
            
            # --- Category index.md Update Logic ---
            category_index_path = os.path.join(category, "index.md")
            if os.path.exists(category_index_path):
                with open(category_index_path, "r", encoding="utf-8") as f:
                    cat_index_content = f.read()
                
                cat_note_link = f"- [{note_title}](./{encoded_filename})"
                
                if cat_note_link not in cat_index_content:
                    # Find a good place to insert - before the "Back to Home" link
                    back_link_marker = "[Back to Home]"
                    if back_link_marker in cat_index_content:
                        insertion_point = cat_index_content.find(back_link_marker)
                        updated_cat_content = cat_index_content[:insertion_point] + cat_note_link + "\n\n" + cat_index_content[insertion_point:]
                    else:
                        updated_cat_content = cat_index_content + f"\n{cat_note_link}"
                    
                    with open(category_index_path, "w", encoding="utf-8") as f:
                        f.write(updated_cat_content)
                    print(f"Successfully updated {category_index_path}")
            # -----------------------------
        # -----------------------------
        
    except Exception as e:
        print(f"Error calling Gemini API or parsing response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
