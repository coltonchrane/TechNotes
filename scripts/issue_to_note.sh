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

# 2. Slugify the clean title
SLUG=$(echo "$CLEAN_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' | tr ' ' '_')
FILENAME="${SLUG}.md"

# 3. Create the directory if it doesn't exist
mkdir -p "$CATEGORY"

# 4. Construct the note content with metadata
cat <<EOF > "${CATEGORY}/${FILENAME}"
---
layout: default
title: ${CLEAN_TITLE}
date: ${ISSUE_DATE}
author: ${ISSUE_AUTHOR}
issue: https://github.com/coltonchrane/TechNotes/issues/${ISSUE_NUMBER}
---

${ISSUE_BODY}
EOF

echo "Created ${CATEGORY}/${FILENAME}"
