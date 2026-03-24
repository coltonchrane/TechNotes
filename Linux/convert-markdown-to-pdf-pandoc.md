---
layout: default
title: Converting Markdown to PDF on Ubuntu using Pandoc
parent: Linux
nav_order: 1
---

# Converting Markdown to PDF on Ubuntu using Pandoc

This guide provides a comprehensive walkthrough for using the Pandoc command-line interface (CLI) to transform Markdown (.md) files into professionally formatted PDF documents on Ubuntu. While LaTeX is the traditional engine for this process, Pandoc also supports HTML-based engines like `wkhtmltopdf` and `WeasyPrint`. These alternatives allow developers to leverage web technologies (HTML/CSS) for document styling, making them ideal for users more comfortable with web design than LaTeX typesetting.

## 1. Installation

Pandoc is a versatile document converter, but it requires an external PDF engine to generate PDF files. You can choose between a LaTeX distribution or HTML-based renderers depending on your layout requirements.

### Installing Pandoc
First, update your package list and install the Pandoc core:

```bash
sudo apt update
sudo apt install pandoc
```

### Installing a PDF Engine
Depending on your needs, install one or more of the following engines:

**Option A: LaTeX (Recommended for academic/scientific papers)**
LaTeX provides high-quality typesetting and is the most common choice for Pandoc, especially when complex mathematical formulas are involved.
```bash
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

**Option B: wkhtmltopdf (Recommended for legacy web rendering)**
This engine uses the WebKit rendering engine (the same engine powering older versions of Safari and Chrome) to convert HTML to PDF. It is stable and handles complex JavaScript-based elements well.
```bash
sudo apt install wkhtmltopdf
```

**Option C: WeasyPrint (Recommended for modern CSS layout support)**
WeasyPrint is a modern visual rendering engine for HTML and CSS. It is specifically designed for "web to PDF" conversion and supports modern CSS features like Flexbox, Grid, and the CSS Paged Media module.
```bash
sudo apt install weasyprint
```

## 2. Basic Conversion

Once the dependencies are installed, you can perform a basic conversion. Pandoc defaults to LaTeX if no engine is specified, but you can explicitly choose your renderer using the `--pdf-engine` flag.

### Default Conversion (LaTeX)
Navigate to the folder containing your Markdown file and run:
```bash
pandoc input.md -o output.pdf
```

### Conversion Using HTML Engines
When using HTML-based engines, Pandoc converts Markdown to an intermediate HTML structure before rendering it to PDF.

```bash
# Using wkhtmltopdf
pandoc input.md --pdf-engine=wkhtmltopdf -o output.pdf

# Using WeasyPrint
pandoc input.md --pdf-engine=weasyprint -o output.pdf
```

## 3. Advanced Customization

Pandoc allows you to customize the output by adding flags to the command. The customization methods vary significantly between LaTeX and HTML-based engines.

### Adding a Table of Contents
This works across all engines:
```bash
pandoc input.md --toc -o output.pdf
```

### Layout Customization (LaTeX Only)
If using the default LaTeX engine, use variables to modify the document layout:
```bash
pandoc input.md -V geometry:margin=1in -V papersize:a4 -o output.pdf
```

### Styling with CSS (wkhtmltopdf and WeasyPrint)
The primary advantage of `wkhtmltopdf` and `WeasyPrint` is the ability to use standard CSS. You can control margins, fonts, and page breaks using a `style.css` file.

**Example style.css:**
```css
body {
    font-family: 'Helvetica', sans-serif;
    line-height: 1.6;
}

h1 {
    color: #2c3e50;
    border-bottom: 2px solid #eee;
}

/* Specific to WeasyPrint and Paged Media */
@page {
    margin: 2cm;
    @bottom-right {
        content: counter(page);
    }
}
```

**Applying the CSS:**
```bash
pandoc input.md --css style.css --pdf-engine=weasyprint -o output.pdf
```

### Engine Comparison: Which to choose?

| Feature | LaTeX | wkhtmltopdf | WeasyPrint |
| :--- | :--- | :--- | :--- |
| **Best For** | Academic/Math | Legacy Web layouts | Modern CSS/Design |
| **Styling** | LaTeX templates | CSS (WebKit) | Modern CSS (Grid/Flex) |
| **Ease of Use** | Steep learning curve | Easy (Web devs) | Easy (Web devs) |
| **Footnotes** | Superior handling | Basic | Good |
| **Paged Media** | Native | Limited | Excellent support |

### Metadata and Headers
You can include metadata such as title and author directly in the command or via a YAML front matter block at the top of your Markdown file:
```bash
pandoc input.md --metadata title="Technical Report" --metadata author="Ubuntu User" -o output.pdf
```

---
**Source:** [GitHub Issue #23](https://github.com/coltonchrane/TechNotes/issues/23) | **Contributor:** @coltonchrane
---