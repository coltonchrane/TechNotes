---
layout: default
title: Converting Markdown to PDF on Ubuntu using Pandoc
parent: Linux
nav_order: 1
---

# Converting Markdown to PDF on Ubuntu using Pandoc

This guide provides a comprehensive walkthrough for using the Pandoc command-line interface (CLI) to transform Markdown (.md) files into professionally formatted PDF documents on Ubuntu.

## 1. Installation

Pandoc is a versatile document converter, but it requires a PDF engine (such as LaTeX) to generate PDF files. 

### Installing Pandoc
First, update your package list and install Pandoc using the apt package manager:

```bash
sudo apt update
sudo apt install pandoc
```

### Installing a PDF Engine
The most reliable way to generate PDFs with Pandoc is by installing a LaTeX distribution. For most users, the `texlive-latex-recommended` package is sufficient:

```bash
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

## 2. Basic Conversion

Once the dependencies are installed, you can perform a basic conversion using a single command in your terminal.

### Running the Command
Navigate to the folder containing your Markdown file and run:

```bash
pandoc input.md -o output.pdf
```

In this example:
- `input.md` is the source file.
- `-o` stands for output.
- `output.pdf` is the name of the file you wish to create.

## 3. Advanced Customization

Pandoc allows you to customize the output by adding flags to the command.

### Adding a Table of Contents
To automatically generate a Table of Contents (TOC) based on your Markdown headers, use the `--toc` flag:

```bash
pandoc input.md --toc -o output.pdf
```

### Adjusting Margins and Paper Size
You can pass variables to the LaTeX engine to modify the document layout. For example, to set 1-inch margins and use A4 paper size:

```bash
pandoc input.md -V geometry:margin=1in -V papersize:a4 -o output.pdf
```

### Using Alternative PDF Engines
If you prefer not to use LaTeX, you can use other engines like `wkhtmltopdf` or `weasyprint`, provided they are installed on your system:

```bash
pandoc input.md --pdf-engine=wkhtmltopdf -o output.pdf
```

---
**Source:** [GitHub Issue #23](https://github.com/coltonchrane/TechNotes/issues/23) | **Contributor:** @coltonchrane