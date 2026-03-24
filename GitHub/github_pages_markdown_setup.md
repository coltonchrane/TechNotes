# Setting Up GitHub Pages for Markdown Repositories

This guide provides a straightforward walkthrough for hosting a website directly from a GitHub repository containing Markdown files. It focuses on the simplest setup for users who want their documentation rendered as a clean, readable website with minimal overhead.

## Table of Contents
1. [Accessing Repository Settings](#1-accessing-repository-settings)
2. [Configuring Build and Deployment](#2-configuring-build-and-deployment)
3. [Creating the Configuration Files](#3-creating-the-configuration-files)
4. [Structuring Markdown with Front Matter](#4-structuring-markdown-with-front-matter)
5. [Viewing Your Site](#5-viewing-your-site)

## 1. Accessing Repository Settings
To begin the setup, navigate to the GitHub repository you wish to publish.
1. Click on the **Settings** tab located in the top navigation bar of your repository.
2. On the left-hand sidebar, locate the **Code and automation** section.
3. Click on **Pages**.

## 2. Configuring Build and Deployment
GitHub Pages offers several ways to build your site. For a simple repository consisting primarily of Markdown files, the branch-based method is the most efficient choice.
### 2.1 Select the Deployment Source
Under the **Build and deployment** section, follow these steps:
1. Ensure the **Source** dropdown is set to "Deploy from a branch".
2. Under **Branch**, click the dropdown and select your primary branch (usually `main` or `master`).
3. Select the folder you wish to serve (choose `/ (root)` if your files are in the main directory) and click **Save**.

## 3. Creating the Configuration Files
To make GitHub Pages work correctly with Jekyll (the engine that converts Markdown to HTML), you need a configuration file in the root of your repository. 
### 3.1 The _config.yml File
Create a file named `_config.yml` in your repository's root directory and add the following code:
```yaml
# Site settings
title: My Project Documentation
description: A helpful guide for my users.
theme: jekyll-theme-cayman
# Build settings
remote_theme: pages-themes/cayman@v0.2.0
plugins:
  - jekyll-remote-theme
```
*Note: You can replace `cayman` with other supported themes like `slate`, `architect`, `minimal`, or `merlot`.*

## 4. Structuring Markdown with Front Matter
For GitHub Pages to process your Markdown files into styled HTML pages, each file should ideally contain "Front Matter." This is a block of YAML code at the very top of the file.
### 4.1 Example index.md
Create an `index.md` file (which serves as your homepage) with the following structure:
```markdown
---
layout: default
title: Home
---
# Welcome to My Site
This is the homepage of my documentation. GitHub Pages automatically converts this Markdown into HTML.
## Quick Links
- [Setup Guide](setup.md)
- [API Reference](api.md)
```
### 4.2 Example Subpage (setup.md)
For other pages, use a similar block:
```markdown
---
layout: default
title: Setup Instructions
---
# Setup Guide
Follow these steps to install the project...
```

## 5. Viewing Your Site
After you save your settings and commit your files (`_config.yml` and your `.md` files), GitHub Actions will trigger a background process to build and deploy your site.
1. Wait approximately 1–2 minutes.
2. Refresh the **Pages** settings page.
3. You will see a notification bar at the top stating: "Your site is live at..." followed by a URL (usually `https://username.github.io/repo-name/`).
4. Any Markdown file in your repo will now be accessible as a rendered page at that URL (e.g., `setup.md` becomes `.../setup.html`).

---
**Source:** [GitHub Issue #8](https://github.com/coltonchrane/TechNotes/issues/8) | **Contributor:** @coltonchrane
---