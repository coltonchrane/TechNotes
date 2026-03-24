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

    if not issue_title:
        print("Error: ISSUE_TITLE environment variable not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a technical documentation assistant. I have a GitHub issue that needs to be converted into a markdown note for my 'TechNotes' repository.

Please analyze the following issue:
Title: {issue_title}
Body: {issue_body}
Author: {issue_author}
Issue Number: {issue_number}
Date: {issue_date}

Generate a JSON object with the following fields:
1. "category": A suggested directory name for this note (e.g., 'Networking', 'Docker', 'Linux', 'Database'). Choose an existing one if it fits, or suggest a new logical one.
2. "filename": A slugified filename ending in '.md' (e.g., 'ssh_setup.md').
3. "content": The formatted markdown content.
   - It MUST start with YAML frontmatter containing 'title', 'date', 'author', and 'issue' (link: https://github.com/coltonchrane/TechNotes/issues/{issue_number}).
   - The body of the note should be nicely formatted, fixing any obvious typos, structuring the information logically with headers, code blocks, etc. If the issue body is short, just use it as is but nicely formatted.

Return ONLY the raw JSON object. Do not wrap it in markdown code blocks like ```json ... ```.

Example Output format:
{{
  "category": "Networking",
  "filename": "ssh_setup.md",
  "content": "---\ntitle: SSH Setup\\ndate: 2026-03-23\\nauthor: user1\\nissue: https://github.com/coltonchrane/TechNotes/issues/123\\n---\\n\\nHere is the body..."
}}
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
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

        # Create directory if it doesn't exist
        os.makedirs(category, exist_ok=True)
        
        file_path = os.path.join(category, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Successfully generated note at {file_path}")

        # --- README.md Update Logic ---
        readme_path = "README.md"
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()

            # Extract title from frontmatter, handling optional quotes
            title_match = re.search(r"^title:\s*[\"']?(.*?)[\"']?$", content, re.MULTILINE)
            note_title = title_match.group(1).strip() if title_match else filename.replace(".md", "").replace("_", " ").title()

            # URL encode category and filename for links
            encoded_category = category.replace(" ", "%20")
            encoded_filename = filename.replace(" ", "%20")
            
            note_link = f"- [{note_title}](./{encoded_category}/{encoded_filename})"
            
            # Prevent duplicate links
            if note_link in readme_content:
                print(f"Note link already exists in {readme_path}. Skipping README update.")
            else:
                # Check if category section exists
                category_header = f"### [{category}](./{encoded_category})"
                
                if category_header in readme_content:
                    # Category exists, find the section and append the note
                    # We'll look for the next header or end of file
                    lines = readme_content.split("\n")
                    new_lines = []
                    in_category = False
                    added = False
                    
                    for line in lines:
                        new_lines.append(line)
                        if category_header in line:
                            in_category = True
                        elif in_category and (line.startswith("### ") or line.startswith("## ")):
                            # Reached next section, insert before this line if not added
                            if not added:
                                # Remove the last line (the current header) and insert note, then put header back
                                new_lines.insert(-1, note_link)
                                new_lines.insert(-1, "") # add a newline before the next section
                                added = True
                            in_category = False
                    
                    if in_category and not added:
                        # Reached end of file while in the correct category
                        new_lines.append(note_link)
                        added = True
                    
                    final_content = "\n".join(new_lines)
                else:
                    # Category doesn't exist, create a new section under ## Contents
                    contents_marker = "## 📖 Contents"
                    if contents_marker in readme_content:
                        insertion_point = readme_content.find(contents_marker) + len(contents_marker)
                        new_section = f"\n\n### [{category}](./{encoded_category})\n{note_link}"
                        final_content = readme_content[:insertion_point] + new_section + readme_content[insertion_point:]
                    else:
                        # Fallback to appending at the end
                        final_content = readme_content + f"\n\n### [{category}](./{encoded_category})\n{note_link}"

                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(final_content)
                print(f"Successfully updated {readme_path}")
        # -----------------------------
        
    except Exception as e:
        print(f"Error calling Gemini API or parsing response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
