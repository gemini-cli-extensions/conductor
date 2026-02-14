# Markdown Style Guide

This document outlines Markdown formatting standards for documentation, READMEs, and content files in this project.

## File Naming Conventions

- Use lowercase letters and hyphens: `guide-name.md`, not `Guide Name.md`
- Use descriptive names: `api-documentation.md` not `doc1.md`
- README files should be uppercase: `README.md`
- Changelog files: `CHANGELOG.md`, `HISTORY.md`
- License files: `LICENSE.md`, `LICENSE.txt`

## Frontmatter Format

Include YAML frontmatter for structured documents:

```yaml
---
title: Document Title
description: Brief description of the document
author: Author Name
date: 2026-02-14
tags: [documentation, guide]
status: draft
---
```

## Headings Hierarchy and Capitalization

- Use ATX style (`#`) for all headings
- Maximum 6 levels (`######`)
- Capitalize first word and proper nouns only (sentence case)
- Include blank line before and after headings

```markdown
# Main Title (H1 - One per document)

## Section Heading (H2)

### Subsection (H3)

#### Detail Level (H4)
```

## Text Formatting

- **Bold**: Use `**text**` for emphasis, not `__text__`
- *Italic*: Use `*text*` for emphasis, not `_text_`
- `Code`: Use backticks for inline code, file names, and technical terms
- ***Bold and italic***: Use `***text***` sparingly

## Lists

### Unordered Lists

- Use `-` (hyphen) as the bullet marker
- Indent nested items with 2 spaces
- Maintain consistent punctuation (periods at end or none)

```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

### Ordered Lists

- Use `1.` for all items (auto-numbering)
- Or use sequential numbers `1.`, `2.`, `3.` for fixed order
- Indent nested items with 3 spaces

```markdown
1. First step
2. Second step
   1. Sub-step
   2. Another sub-step
3. Third step
```

## Code Blocks

- Always specify the language for syntax highlighting
- Use triple backticks (fenced code blocks)
- Use proper indentation inside code blocks

```markdown
```python
def hello_world():
    print("Hello, World!")
```

```javascript
console.log('Hello, World!');
```

```

## Links

### Internal Links
```markdown
[Link to another section](#section-heading)
[Link to file](./path/to/file.md)
[Link to image](../assets/image.png)
```

### External Links

```markdown
[External link](https://example.com)
[External link with title](https://example.com "Title")
```

### Anchor Links

- Convert headings to lowercase
- Replace spaces with hyphens
- Remove special characters

```markdown
## Section Heading
Link: [Go to Section](#section-heading)
```

## Tables

- Use pipe tables for simple data
- Include header separator line
- Align columns for readability (in source)
- Left-align text, right-align numbers

```markdown
| Feature | Description | Status |
|---------|-------------|--------|
| Feature A | Does something | Done |
| Feature B | Does another thing | In Progress |
```

## Blockquotes

- Use `>` for callouts and quotes
- Can nest blockquotes
- Combine with other formatting

```markdown
> **Note:** This is an important callout.

> **Warning:** Be careful with this operation.

> This is a standard blockquote.
```

## Images

- Always include alt text for accessibility
- Use descriptive file names
- Provide width/height when possible

```markdown
![Alt text describing the image](./path/to/image.png)
![Diagram showing architecture](./assets/architecture.png)
```

## Linting Rules (markdownlint)

Configure `.markdownlint.json`:

```json
{
  "default": true,
  "MD013": {
    "line_length": 120,
    "heading_line_length": 120,
    "code_block_line_length": 120
  },
  "MD024": {
    "allow_different_nesting": true
  },
  "MD033": false,
  "MD041": false
}
```

Common rules:

- **MD013**: Line length (configure 80-120 chars)
- **MD024**: No duplicate headings
- **MD033**: Inline HTML (disable if needed)
- **MD041**: First line must be H1

## Accessibility Guidelines

- Provide alt text for all images
- Use descriptive link text (not "click here")
- Maintain proper heading hierarchy (no skipping levels)
- Ensure sufficient color contrast in diagrams
- Use tables for tabular data only
- Test with screen readers

## Documentation Templates

### README Template

```markdown
# Project Name

Brief description of the project.

## Installation

```bash
npm install
```

## Usage

```javascript
const example = require('example');
```

## API Documentation

See [API.md](./API.md) for details.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)

```

### API Documentation Template
```markdown
# API Documentation

## Endpoint: `/api/v1/resource`

### GET

Returns list of resources.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Maximum results (default: 20) |
| offset | integer | No | Pagination offset |

**Response:**

```json
{
  "data": [...],
  "total": 100
}
```

```

## Best Practices

1. One H1 heading per document
2. Use blank lines between block elements
3. Keep lines under 120 characters
4. Use relative paths for internal links
5. Version control binary assets separately
6. Write for humans first, machines second
7. Preview before committing
8. Use spell check
9. Include examples for complex concepts
10. Update TOCs automatically when possible

**BE CONSISTENT.** When editing documentation, match the existing style.

*References:*
- [CommonMark Specification](https://commonmark.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
