# TechNotes Automation Scripts

This directory contains automation tools designed to manage and maintain the [TechNotes](https://github.com/coltonchrane/TechNotes) documentation repository. These scripts leverage the Gemini API to streamline the conversion of GitHub issues and pull request feedback into high-quality technical documentation.

## 🛠️ Tools Overview

### 1. `gemini_note_generator.py`
A Python script that uses the Gemini API to transform a GitHub issue into a well-structured, slugified Markdown note.

- **Features**:
  - Analyzes issue title and body to suggest a category and filename.
  - Generates comprehensive content with H2/H3 headers and code blocks.
  - Automatically prepends Jekyll front matter for site navigation.
  - Updates the root `index.md` with links to the new note.
- **Environment Variables**:
  - `GEMINI_API_KEY`: Your Google Gemini API key.
  - `ISSUE_TITLE`: The title of the GitHub issue.
  - `ISSUE_BODY`: The body content of the issue.
  - `ISSUE_NUMBER`: The issue number for linking back to the source.
  - `ISSUE_AUTHOR`: The GitHub username of the contributor.
  - `GEMINI_MODEL`: (Optional) Defaults to `gemini-3-flash-preview`.

### 2. `gemini_pr_fixer.py`
A Python utility designed to refine existing notes or the repository index based on peer feedback or review comments.

- **Features**:
  - Updates specific files while preserving existing Jekyll front matter and structural elements.
  - Maintains repository style (numbered sections, source footers).
  - Automatically updates link titles in the root `index.md` if a note's title is modified during the refinement process.
- **Environment Variables**:
  - `GEMINI_API_KEY`: Your Google Gemini API key.
  - `FILE_PATH`: Path to the file to be updated (e.g., `Networking/ssh_setup.md`).
  - `COMMENT_BODY`: The feedback or instructions for the update.

### 3. `issue_to_note.sh`
A lightweight Bash alternative for converting GitHub issues into notes without deep AI analysis. It relies on a specific title format: `[Category] Title`.

- **Usage**: `./issue_to_note.sh "Title" "Body" "IssueNumber" "Author"`
- **Features**:
  - Extracts category from the title bracket (e.g., `[Linux]`).
  - Automatically calculates `nav_order` based on existing files.
  - Creates category directories and `index.md` files as needed.

## 🤖 GitHub Workflows

These scripts are integrated into the repository's automation via the following GitHub Actions workflows:

### 1. [Contribution Bot](../.github/workflows/contribution-bot.yml)
- **Triggers**: When an issue is opened or labeled with `contribution`.
- **Action**: Runs `gemini_note_generator.py` to create a new technical note from the issue content and automatically opens a Pull Request for review.

### 2. [PR Fixer](../.github/workflows/pr-fixer.yml)
- **Triggers**: When a comment is made on a Pull Request or a review is submitted.
- **Action**: Runs `gemini_pr_fixer.py` to refine the documentation based on the feedback provided in the comments, pushing updates directly to the PR branch.

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- `google-genai` Python library (`pip install google-genai`)
- A valid Google Gemini API Key.

### Integration
These scripts are intended to be triggered by GitHub Actions. Ensure your workflow files are configured to pass the necessary environment variables from the GitHub event context.
