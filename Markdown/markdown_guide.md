---
layout: default
title: Markdown Guide
parent: Markdown
nav_order: 2
---

# Markdown Syntax Guide

A quick reference for common Markdown notation and formatting.

## Headers
```markdown
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
```

## Emphasis
```markdown
*Italic* or _Italic_
**Bold** or __Bold__
***Bold and Italic***
~~Strikethrough~~
```

## Lists
### Unordered
```markdown
- Item 1
- Item 2
  - Sub-item 2.1
  - Sub-item 2.2
```

### Ordered
```markdown
1. First item
2. Second item
3. Third item
```

### Task Lists
```markdown
- [x] Completed task
- [ ] Incomplete task
```

## Links & Images
```markdown
[Link Text](https://www.example.com)
![Image Alt Text](https://via.placeholder.com/150)
```

## Code
### Inline Code
```markdown
Use `backticks` for inline code.
```

### Code Blocks
~~~markdown
```python
def hello_world():
    print("Hello, World!")
```
~~~

## Blockquotes
```markdown
> This is a blockquote.
> It can span multiple lines.
```

## Tables
```markdown
| Header 1 | Header 2 |
| :---:    | :---     |
| Centered | Left     |
| Row 2    | Data     |
```

## Horizontal Rules
```markdown
---
```

## Collapsible Sections
```markdown
<details markdown="1">
<summary>Click to expand</summary>

Hidden content goes here.

</details>
```
