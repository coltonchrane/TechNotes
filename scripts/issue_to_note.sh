#!/bin/bash
# scripts/issue_to_note.sh
# Converts a GitHub Issue to a Markdown file in the repository.

ISSUE_TITLE="$1"
ISSUE_BODY="$2"
ISSUE_NUMBER="$3"
ISSUE_AUTHOR="$4"
ISSUE_DATE=$(date +"%Y-%m-%d")

# 1. Extract category from title: "[Category] Title"
CATEGORY=$(echo "$ISSUE_TITLE" | sed -n 's/\[\(.*\)\] .*/\1/p')
CLEAN_TITLE=$(echo "$ISSUE_TITLE" | sed 's/\[.*\] //')

# If no category found, default to "Inbound"
if [ -z "$CATEGORY" ]; then
    CATEGORY="Inbound"
fi

# Slugify category (replace spaces with underscores)
SLUG_CATEGORY=$(echo "$CATEGORY" | tr ' ' '_')

# 2. Slugify the clean title
SLUG=$(echo "$CLEAN_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' | tr ' ' '_')
FILENAME="${SLUG}.md"

# 3. Create the directory if it doesn't exist
mkdir -p "$SLUG_CATEGORY"

# Construct the note content with metadata
cat <<EOF > "${SLUG_CATEGORY}/${FILENAME}"
---
layout: default
title: ${CLEAN_TITLE}
date: ${ISSUE_DATE}
author: ${ISSUE_AUTHOR}
issue: https://github.com/coltonchrane/TechNotes/issues/${ISSUE_NUMBER}
---

${ISSUE_BODY}
EOF

echo "Created ${SLUG_CATEGORY}/${FILENAME}"

# 5. Update index.md
INDEX_FILE="index.md"
if [ -f "$INDEX_FILE" ]; then
    NOTE_LINK="- [${CLEAN_TITLE}](./${SLUG_CATEGORY}/${FILENAME})"
    
    # Check if category header exists (with original category as display name)
    CATEGORY_HEADER="### [${CATEGORY}](./${SLUG_CATEGORY})"
    
    if grep -qF "$CATEGORY_HEADER" "$INDEX_FILE"; then
        # Category exists, append note link after the header
        sed -i "/$(echo "$CATEGORY_HEADER" | sed 's/[][\.*^$/]/\\&/g')/a ${NOTE_LINK}" "$INDEX_FILE"
        echo "Updated ${INDEX_FILE} with new note link in existing category."
    else
        # Category doesn't exist, append new category and link after Table of Contents
        TOC_MARKER="## 📖 Table of Contents"
        if grep -qF "$TOC_MARKER" "$INDEX_FILE"; then
            sed -i "/$TOC_MARKER/a \\\\n### [${CATEGORY}](./${SLUG_CATEGORY})\\n${NOTE_LINK}" "$INDEX_FILE"
            echo "Updated ${INDEX_FILE} with new category and note link."
        else
            echo -e "\n\n### [${CATEGORY}](./${SLUG_CATEGORY})\n${NOTE_LINK}" >> "$INDEX_FILE"
            echo "Appended new category and note link to end of ${INDEX_FILE}."
        fi
    fi
fi
