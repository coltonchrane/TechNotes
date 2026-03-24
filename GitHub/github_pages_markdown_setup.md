# Setting Up GitHub Pages for Markdown Repositories

This guide provides a straightforward walkthrough for hosting a website directly from a GitHub repository containing Markdown files. It focuses on the simplest setup for users who want their documentation rendered as a clean, readable website with minimal overhead.

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

## 3. Applying a Jekyll Theme

Because your repository contains raw Markdown, GitHub can automatically convert these files into a styled website using its built-in Jekyll integration. This eliminates the need to write HTML or CSS manually.

### 3.1 Using the Theme Chooser
1. In the GitHub Pages settings menu, look for the **Theme Chooser** section.
2. Click **Change theme**.
3. Browse the available themes (such as Cayman, Slate, or Minimal) and click **Select theme**.

Once selected, GitHub will automatically create or update a `_config.yml` file in your repository. You can manually edit this file later to add a title or description:

```yaml
theme: jekyll-theme-cayman
title: My Tech Notes
description: A collection of technical guides and documentation.
```

## 4. Viewing Your Site

After you save your settings, GitHub Actions will trigger a background process to build and deploy your site.

1. Wait approximately 1–2 minutes.
2. Refresh the **Pages** settings page.
3. You will see a notification bar at the top stating: "Your site is live at..." followed by a URL (usually `https://username.github.io/repo-name/`).
4. Any Markdown file in your repo (e.g., `setup.md`) will now be accessible as a rendered page at that URL (e.g., `.../setup.html`).

---
**Source:** [GitHub Issue #8](https://github.com/coltonchrane/TechNotes/issues/8) | **Contributor:** @coltonchrane