# Tech Notes 📝

A collection of technical notes, guides, and quick-reference documentation for various IT and development topics.

## 🚀 Features

- **AI-Powered Note Generation**: Automatically converts GitHub issues into formatted markdown notes using Gemini AI.
- **Automated Refinement**: Bot-driven updates to notes via PR comments.
- **Easy Categorization**: Automatically organizes notes into logical directories.

## 📂 Project Structure

```text
.
├── Disk Management/      # Storage, cleanup, and image compression
├── Docker/               # Containerization and orchestration
├── Markdown/             # Guides and references for markdown
├── Networking/           # Connectivity, SSH, and VPN guides
├── scripts/              # Automation tools and AI-driven generators
└── .github/workflows/    # CI/CD pipelines for note generation and PR fixing
```

## 📖 Contents

### [Programming Languages](./Programming%20Languages)
- [How C# Works](./Programming%20Languages/how_csharp_works.md)

### [Disk Management](./Disk%20Management)
- [Compress Image CLI](./Disk%20Management/compress_image_cli.md)
- [NCDU Guide](./Disk%20Management/ncdu.md)
- [Ubuntu 25 Cleanup](./Disk%20Management/ubuntu_25_cleanup.md)

### [Docker](./Docker)
- [Docker Cleanup Guide](./Docker/docker_cleanup_guide.md)
- [Docker File Watching](./Docker/docker_file_watching.md)

### [Markdown](./Markdown)
- [GitHub Emojis](./Markdown/github_emojis.md)
- [Markdown Guide](./Markdown/markdown_guide.md)

### [Networking](./Networking)
- [Docker Run in Production](./Networking/docker_run_in_prod.md)
- [LXC Run in Production](./Networking/lxc_run_in_prod.md)
- [SSH Setup Guide](./Networking/ssh_setup_guide.md)
- [VPN Setup Guide](./Networking/vpn_setup_guide.md)

## 🤖 Automation & Tools

This repository uses a **Gemini AI-powered bot** to streamline contributions.

- **`gemini_note_generator.py`**: A Python script that uses Gemini AI (`gemini-2.0-flash`) to transform raw issue text into clean, structured markdown.
- **`gemini_pr_fixer.py`**: Handles iterative refinements based on PR comments.
- **`issue_to_note.sh`**: A shell utility for basic issue-to-note conversion.

## 🤝 Contributing

We welcome new notes! You don't even need to touch the code—just open an issue.

1.  **Open an Issue**: Use the `[Category] Title` format.
2.  **Add the `contribution` label**: The bot will automatically generate a PR for you.
3.  **Refine**: Comment on the PR if you need the AI to adjust anything.

See [CONTRIBUTING_BOT.md](./CONTRIBUTING_BOT.md) for full details on how the automation works.
