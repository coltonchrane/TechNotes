---
layout: default
title: Fixing wkhtmltopdf Installation on Linux
parent: Linux
nav_order: 3
---

# Fixing wkhtmltopdf Installation on Linux

This guide provides a solution for users who encounter issues when trying to install `wkhtmltopdf` via the standard package manager. It details how to manually install the official package to ensure full functionality for Markdown-to-PDF conversions.

## 1. The Problem with Default Repositories

In many Linux distributions, the version of `wkhtmltopdf` provided in the default repositories (via `sudo apt install wkhtmltopdf`) is reduced in functionality. It often lacks a patched version of Qt, which is required for advanced rendering features like headers, footers, and proper CSS support. This frequently leads to installation failures or broken PDF outputs.

## 2. Manual Installation via .deb Package

To resolve these issues, you should download and install the official package directly from the project's releases page.

### 2.1. Download the Correct Package
Go to the [official wkhtmltopdf downloads page](https://wkhtmltopdf.org/downloads.html) and find the package that matches your specific distribution and architecture. 

For example, if you are using Ubuntu 22.04 (Jammy Jellyfish) on a 64-bit system, you can download the package using `wget`:

```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltopdf_0.12.6.1-2.jammy_amd64.deb
```

### 2.2. Install the Package
Once the download is complete, use `dpkg` to install the local file:

```bash
sudo dpkg -i wkhtmltopdf_0.12.6.1-2.jammy_amd64.deb
```

### 2.3. Resolving Dependency Errors
It is common for `dpkg` to report missing dependencies (such as `xfonts-75dpi` or `xfonts-base`). If this happens, run the following command to automatically fetch and install the required dependencies:

```bash
sudo apt --fix-broken install
```

## 3. Verifying the Installation

After the installation process finishes, check that the binary is working correctly and verify the version:

```bash
wkhtmltopdf --version
```

You should see an output indicating the version number and that it is compiled with a patched version of Qt. You can now proceed with converting your Markdown notes to PDF without errors.

---
**Source:** [GitHub Issue #29](https://github.com/coltonchrane/TechNotes/issues/29) | **Contributor:** @coltonchrane