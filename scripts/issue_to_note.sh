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

# 4. Calculate nav_order for the note
# Count existing .md files in the category directory (excluding index.md)
NAV_ORDER=$(ls -1 "$SLUG_CATEGORY"/*.md 2>/dev/null | grep -v "index.md" | wc -l | xargs -I{} echo "{}+1" | bc)

# Construct the note content with metadata
cat <<EOF > "${SLUG_CATEGORY}/${FILENAME}"
---
layout: default
title: ${CLEAN_TITLE}
parent: ${CATEGORY}
nav_order: ${NAV_ORDER}
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

# 6. Ensure category index.md exists with navigation metadata
CATEGORY_INDEX="${SLUG_CATEGORY}/index.md"
if [ ! -f "$CATEGORY_INDEX" ]; then
    # Calculate nav_order for category: count existing category index files + Home(1) + New(1)
    CAT_NAV_ORDER=$(find . -maxdepth 2 -name "index.md" | grep -v "^./index.md" | wc -l | xargs -I{} echo "{}+2" | bc)
    cat <<EOF > "$CATEGORY_INDEX"
---
layout: default
title: ${CATEGORY}
has_children: true
nav_order: ${CAT_NAV_ORDER}
---

# ${CATEGORY}

- [${CLEAN_TITLE}](./${FILENAME})

[Back to Home](../index.md)
EOF
    echo "Created ${CATEGORY_INDEX} with navigation metadata"
else
    # Update existing category index (if not already there)
    if ! grep -qF "./${FILENAME}" "$CATEGORY_INDEX"; then
        # Insert after the H1 header
        sed -i "/# ${CATEGORY}/a - [${CLEAN_TITLE}](./${FILENAME})" "$CATEGORY_INDEX"
    fi
fi
