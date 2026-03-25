---
layout: default
title: Converting Markdown to PDF on Ubuntu using Pandoc
parent: Linux
nav_order: 1
---

# Converting Markdown to PDF on Ubuntu using Pandoc

This guide provides a comprehensive walkthrough for using the Pandoc command-line interface (CLI) to transform Markdown (.md) files into professionally formatted PDF documents on Ubuntu. While LaTeX is the traditional engine for this process, Pandoc also supports HTML-based engines like wkhtmltopdf and WeasyPrint, which allow for styling via CSS.

## 1. Installation

Pandoc is a versatile document converter, but it requires an external PDF engine to generate PDF files. You can choose between a LaTeX distribution or HTML-based renderers.

### Installing Pandoc
First, update your package list and install Pandoc:

```bash
sudo apt update
sudo apt install pandoc
```

### Installing a PDF Engine
Depending on your needs, install one or more of the following engines:

**Option A: LaTeX (Recommended for academic/scientific papers)**
LaTeX provides high-quality typesetting and is the most common choice for Pandoc.
```bash
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

**Option B: wkhtmltopdf (Recommended for simple HTML-like rendering)**
This engine uses the WebKit rendering engine to convert HTML to PDF.
```bash
sudo apt install wkhtmltopdf
```

**Option C: WeasyPrint (Recommended for modern CSS layout support)**
WeasyPrint is a visual rendering engine for HTML and CSS that can export to PDF.
```bash
sudo apt install weasyprint
```

## 2. Basic Conversion

Once the dependencies are installed, you can perform a basic conversion. If you have multiple engines installed, you can specify which one to use.

### Default Conversion (LaTeX)
Navigate to the folder containing your Markdown file and run:
```bash
pandoc input.md -o output.pdf
```

### Conversion Using a Specific Engine
To use an alternative engine like `wkhtmltopdf` or `weasyprint`, use the `--pdf-engine` flag:
```bash
# Using wkhtmltopdf
pandoc input.md --pdf-engine=wkhtmltopdf -o output.pdf

# Using WeasyPrint
pandoc input.md --pdf-engine=weasyprint -o output.pdf
```

## 3. Advanced Customization

Pandoc allows you to customize the output by adding flags to the command, though the available flags may change depending on your chosen engine.

### Adding a Table of Contents
To automatically generate a Table of Contents (TOC) based on your Markdown headers:
```bash
pandoc input.md --toc -o output.pdf
```

### Layout Customization (LaTeX Only)
If using the default LaTeX engine, you can pass variables to modify the document layout, such as margins and paper size:
```bash
pandoc input.md -V geometry:margin=1in -V papersize:a4 -o output.pdf
```

### Styling with CSS (wkhtmltopdf and WeasyPrint)
A major advantage of using HTML-based engines is the ability to style your document using standard CSS. Create a `style.css` file and apply it during conversion:
```bash
pandoc input.md --css style.css --pdf-engine=weasyprint -o output.pdf
```

### Metadata and Headers
You can include metadata such as title and author directly in the command or via a YAML front matter block at the top of your Markdown file:
```bash
pandoc input.md --metadata title="My Document" --metadata author="John Doe" -o output.pdf
```

---
**Source:** [GitHub Issue #23](https://github.com/coltonchrane/AutoNotes/issues/23) | **Contributor:** @coltonchrane
---