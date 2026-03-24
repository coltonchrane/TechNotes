#!/usr/bin/env python3
import os
import sys
import json
from google import genai

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

    model_name = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")

    client = genai.Client(api_key=api_key)

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
            
        print(f"Successfully updated note at {file_path}")
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
