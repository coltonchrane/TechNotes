#!/usr/bin/env python3
import os
import sys
import json
import re
from google import genai

def extract_title(content):
    # Extract title from front matter or H1
    front_matter_match = re.search(r"^title:\s*(.*?)$", content, re.MULTILINE)
    if front_matter_match:
        return front_matter_match.group(1).strip()
    
    h1_match = re.search(r"^#\s*(.*?)$", content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    return None

def update_index_entry(old_title, new_title, file_path):
    # Update only the root index.md. Category index.md files no longer contain note links.
    category_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    
    # Category dir is already slugified on disk
    encoded_category = category_dir
    encoded_filename = filename.replace(" ", "%20")

    targets = [
        ("index.md", f"./{encoded_category}/{encoded_filename}"), # Root index
    ]

    for target_path, link_path in targets:
        if not os.path.exists(target_path):
            continue

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex to find the entry: - [ANYTHING](link_path)
        pattern = rf"- \[.*?\]\({re.escape(link_path)}\)"
        replacement = f"- [{new_title}]({link_path})"
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated link title in {target_path} from '{old_title}' to '{new_title}'")
        else:
            print(f"No existing link found for {link_path} in {target_path}")

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    file_path = os.environ.get("FILE_PATH")
    comment_body = os.environ.get("COMMENT_BODY")

    if not file_path or not comment_body:
        print("Error: FILE_PATH or COMMENT_BODY environment variables not set.")
        sys.exit(1)

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        current_content = f.read()

    old_title = extract_title(current_content)
    
    model_name = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")
    client = genai.Client(api_key=api_key)

    is_index = file_path == "index.md"
    
    if is_index:
        prompt = f"""
You are a technical documentation assistant. I need to update the repository's index file based on feedback.

Current Index Content:
---
{current_content}
---

User Feedback:
"{comment_body}"

Please update the index file.
- PRESERVE the existing Jekyll front matter.
- Preserve the overall structure (Table of Contents, Features, etc.).
- Ensure links to notes remain valid.
- Return ONLY the updated markdown content. No conversational filler or code blocks.
"""
    else:
        prompt = f"""
You are a technical documentation assistant. I have a technical note that needs refinement based on a user's feedback.

Current Content:
---
{current_content}
---

User Feedback:
"{comment_body}"

Please update the technical note based on the feedback.
- PRESERVE the existing Jekyll front matter (the block between --- at the very top).
- Preserve the existing H1 title and the "Source/Contributor" section at the bottom unless the feedback explicitly asks to change them.
- Ensure main sections remain numbered (## 1., ## 2., etc.) as per the repository style.
- Improve the formatting, clarity, or depth of the content as requested.
- Return ONLY the raw markdown content. No conversational filler or markdown code blocks.
"""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        updated_content = response.text.strip()
        
        # Clean up any potential markdown code block markers
        if updated_content.startswith("```markdown"):
            updated_content = updated_content[11:]
        elif updated_content.startswith("```"):
            updated_content = updated_content[3:]
        if updated_content.endswith("```"):
            updated_content = updated_content[:-3]
        
        updated_content = updated_content.strip()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
            
        print(f"Successfully updated {file_path}")
        
        # If it was a note, check if the title changed and update index.md
        if not is_index:
            new_title = extract_title(updated_content)
            if new_title and new_title != old_title:
                update_index_entry(old_title, new_title, file_path)
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
