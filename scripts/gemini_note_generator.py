#!/usr/bin/env python3
import os
import sys
import json
import re
import google.generativeai as genai
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

    genai.configure(api_key=api_key)
    
    # We will use the latest gemini-1.5-flash model
    model = genai.GenerativeModel('gemini-1.5-flash')

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
        response = model.generate_content(prompt)
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
        
    except Exception as e:
        print(f"Error calling Gemini API or parsing response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
