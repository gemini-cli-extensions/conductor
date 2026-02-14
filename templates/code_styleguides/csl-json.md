# CSL-JSON Style Guide

This document outlines standards for working with CSL-JSON (Citation Style Language JSON) format for bibliographic data.

## Overview of CSL-JSON Format

CSL-JSON is a standardized JSON format for bibliographic metadata used by:

- Citation processors (pandoc-citeproc, citeproc-js)
- Reference managers (Zotero, Mendeley)
- Academic publishing tools
- Bibliography generation

It provides a unified format that can be formatted into any citation style (APA, MLA, Chicago, IEEE, etc.) using CSL style files.

## File Structure and Naming

### File Naming

```
references.json          # Default name for single file
bibliography.json        # Alternative name
refs-2026-02.json       # With date suffix
project-references.json  # Project-specific
```

### File Structure

```json
{
  "references": [
    {
      "id": "smith2024",
      "type": "article-journal",
      ...
    },
    {
      "id": "jones2023",
      "type": "book",
      ...
    }
  ]
}
```

## Required Fields

Every CSL-JSON entry must have:

```json
{
  "id": "unique-identifier",  // Required: Unique citation key
  "type": "document-type"     // Required: CSL document type
}
```

### Common Document Types

- `article-journal` - Journal articles
- `book` - Books
- `chapter` - Book chapters
- `paper-conference` - Conference papers
- `report` - Technical reports
- `webpage` - Web pages
- `software` - Software
- `thesis` - Theses and dissertations
- `article-magazine` - Magazine articles
- `article-newspaper` - Newspaper articles

## Author Format

### Individual Authors

```json
{
  "author": [
    {
      "family": "Smith",
      "given": "John A."
    },
    {
      "family": "Doe",
      "given": "Jane",
      "suffix": "Jr."
    }
  ]
}
```

### Corporate Authors

```json
{
  "author": [
    {
      "literal": "World Health Organization"
    }
  ]
}
```

### Multiple Authors

```json
{
  "author": [
    { "family": "Smith", "given": "John" },
    { "family": "Jones", "given": "Mary" },
    { "family": "Brown", "given": "Robert" }
  ]
}
```

### Editors

```json
{
  "editor": [
    { "family": "Smith", "given": "John" }
  ]
}
```

## Date Fields

### Issued Date (Publication Date)

```json
{
  "issued": {
    "date-parts": [[2024, 3, 15]]  // Year, Month, Day
  }
}

{
  "issued": {
    "date-parts": [[2024, 3]]      // Year, Month only
  }
}

{
  "issued": {
    "date-parts": [[2024]]          // Year only
  }
}

{
  "issued": {
    "literal": "Spring 2024"       // Non-standard date
  }
}
```

### Accessed Date

```json
{
  "accessed": {
    "date-parts": [[2026, 2, 14]]
  }
}
```

## Complete Examples

### Journal Article

```json
{
  "id": "smith2024neural",
  "type": "article-journal",
  "title": "Neural Networks in Climate Modeling: A Comprehensive Review",
  "author": [
    { "family": "Smith", "given": "John A." },
    { "family": "Johnson", "given": "Emily R." }
  ],
  "container-title": "Journal of Climate Science",
  "volume": "45",
  "issue": "3",
  "page": "234-256",
  "DOI": "10.1234/jcs.2024.0123",
  "issued": {
    "date-parts": [[2024, 6]]
  },
  "abstract": "This paper reviews recent advances...",
  "keyword": ["neural networks", "climate modeling", "machine learning"]
}
```

### Book

```json
{
  "id": "jones2023python",
  "type": "book",
  "title": "Advanced Python Programming",
  "author": [
    { "family": "Jones", "given": "Michael" }
  ],
  "publisher": "Tech Books Publishing",
  "publisher-place": "San Francisco, CA",
  "edition": "3rd",
  "volume": "1",
  "number-of-pages": "456",
  "ISBN": "978-1-234-56789-0",
  "issued": {
    "date-parts": [[2023]]
  },
  "abstract": "A comprehensive guide to advanced Python..."
}
```

### Book Chapter

```json
{
  "id": "brown2024chapter",
  "type": "chapter",
  "title": "Machine Learning in Healthcare",
  "author": [
    { "family": "Brown", "given": "Sarah" }
  ],
  "container-title": "Handbook of Medical Informatics",
  "editor": [
    { "family": "Davis", "given": "Robert" },
    { "family": "Wilson", "given": "Lisa" }
  ],
  "publisher": "Academic Press",
  "publisher-place": "Boston, MA",
  "page": "123-145",
  "edition": "2nd",
  "issued": {
    "date-parts": [[2024]]
  }
}
```

### Conference Paper

```json
{
  "id": "lee2024conference",
  "type": "paper-conference",
  "title": "Efficient Algorithms for Large-Scale Data Processing",
  "author": [
    { "family": "Lee", "given": "David" },
    { "family": "Chen", "given": "Wei" }
  ],
  "container-title": "Proceedings of the 2024 International Conference on Big Data",
  "publisher": "IEEE",
  "publisher-place": "New York, NY",
  "page": "45-52",
  "event": "International Conference on Big Data 2024",
  "event-place": "San Francisco, CA",
  "DOI": "10.1109/BigData.2024.00123",
  "issued": {
    "date-parts": [[2024, 12]]
  }
}
```

### Technical Report

```json
{
  "id": "nasa2024report",
  "type": "report",
  "title": "Analysis of Satellite Data for Climate Research",
  "author": [
    { "literal": "NASA Goddard Space Flight Center" }
  ],
  "publisher": "NASA",
  "publisher-place": "Greenbelt, MD",
  "number": "NASA/TM-2024-12345",
  "genre": "Technical Memorandum",
  "issued": {
    "date-parts": [[2024, 8]]
  },
  "URL": "https://ntrs.nasa.gov/citations/20240001234"
}
```

### Web Page

```json
{
  "id": "mdn2024web",
  "type": "webpage",
  "title": "JavaScript Reference",
  "author": [
    { "literal": "Mozilla Developer Network" }
  ],
  "container-title": "MDN Web Docs",
  "URL": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference",
  "issued": {
    "date-parts": [[2024, 1, 15]]
  },
  "accessed": {
    "date-parts": [[2026, 2, 14]]
  }
}
```

### Software

```json
{
  "id": "python2024",
  "type": "software",
  "title": "Python",
  "author": [
    { "literal": "Python Software Foundation" }
  ],
  "version": "3.12.0",
  "publisher": "Python Software Foundation",
  "URL": "https://www.python.org/",
  "issued": {
    "date-parts": [[2024, 10, 2]]
  }
}
```

### Thesis

```json
{
  "id": "garcia2024thesis",
  "type": "thesis",
  "title": "Deep Learning Approaches to Natural Language Understanding",
  "author": [
    { "family": "Garcia", "given": "Maria" }
  ],
  "publisher": "Stanford University",
  "publisher-place": "Stanford, CA",
  "genre": "Ph.D. dissertation",
  "number-of-pages": "250",
  "issued": {
    "date-parts": [[2024]]
  }
}
```

## Field Reference Table

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique identifier (citation key) | `"smith2024"` |
| `type` | Document type | `"article-journal"` |
| `title` | Title of work | `"Article Title"` |
| `author` | List of authors | Array of name objects |
| `editor` | List of editors | Array of name objects |
| `container-title` | Journal/book title | `"Journal Name"` |
| `publisher` | Publisher name | `"Academic Press"` |
| `publisher-place` | Publication location | `"New York, NY"` |
| `volume` | Volume number | `"45"` |
| `issue` | Issue number | `"3"` |
| `page` | Page range | `"123-145"` |
| `edition` | Edition statement | `"2nd"` |
| `DOI` | Digital Object Identifier | `"10.1234/example"` |
| `ISBN` | International Standard Book Number | `"978-1-234-56789-0"` |
| `URL` | Web address | `"https://example.com"` |
| `issued` | Publication date | Date object |
| `accessed` | Access date | Date object |
| `abstract` | Abstract text | `"Abstract content..."` |
| `keyword` | Keywords/tags | Array of strings |
| `language` | Language code | `"en-US"` |
| `note` | Additional notes | `"Note content"` |

## BibLaTeX Conversion

### Python Conversion

```python
import json

def biblatex_to_csl(biblatex_entry):
    """Convert BibLaTeX entry to CSL-JSON."""

    type_mapping = {
        'article': 'article-journal',
        'book': 'book',
        'inbook': 'chapter',
        'incollection': 'chapter',
        'inproceedings': 'paper-conference',
        'conference': 'paper-conference',
        'techreport': 'report',
        'mastersthesis': 'thesis',
        'phdthesis': 'thesis',
        'misc': 'document',
        'online': 'webpage',
        'software': 'software'
    }

    csl = {
        'id': biblatex_entry.get('key', ''),
        'type': type_mapping.get(biblatex_entry.get('type'), 'document')
    }

    # Map fields
    field_mapping = {
        'title': 'title',
        'author': 'author',
        'editor': 'editor',
        'booktitle': 'container-title',
        'journal': 'container-title',
        'publisher': 'publisher',
        'address': 'publisher-place',
        'volume': 'volume',
        'number': 'issue',
        'pages': 'page',
        'doi': 'DOI',
        'isbn': 'ISBN',
        'url': 'URL',
        'year': 'issued',
        'abstract': 'abstract'
    }

    for bib_field, csl_field in field_mapping.items():
        if bib_field in biblatex_entry:
            value = biblatex_entry[bib_field]
            if csl_field == 'issued':
                csl[csl_field] = {'date-parts': [[int(value)]]}
            else:
                csl[csl_field] = value

    return csl
```

### Using pandoc

```bash
# Convert BibLaTeX to CSL-JSON
pandoc references.bib -f biblatex -t csljson -o references.json

# Convert CSL-JSON to BibLaTeX
pandoc references.json -f csljson -t biblatex -o references.bib
```

## EndNote Conversion

### Export from EndNote

1. Select references in EndNote
2. File → Export
3. Choose "XML" format
4. Save as `.xml` file

### Convert to CSL-JSON

```python
import xml.etree.ElementTree as ET
import json

def endnote_to_csl(xml_file):
    """Convert EndNote XML to CSL-JSON."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    references = []

    for record in root.findall('.//record'):
        ref = {
            'id': record.find('rec-number').text if record.find('rec-number') is not None else '',
            'type': 'article-journal'  # Default, map based on reference type
        }

        # Extract title
        titles = record.find('titles')
        if titles is not None:
            title = titles.find('title')
            if title is not None:
                ref['title'] = title.text

        # Extract authors
        authors_elem = record.find('authors')
        if authors_elem is not None:
            authors = []
            for author in authors_elem.findall('author'):
                name_parts = author.text.split(',')
                if len(name_parts) == 2:
                    authors.append({
                        'family': name_parts[0].strip(),
                        'given': name_parts[1].strip()
                    })
            if authors:
                ref['author'] = authors

        references.append(ref)

    return {'references': references}
```

## Validation

### Schema Validation

```python
import json
import jsonschema

# CSL-JSON schema (simplified)
CSL_SCHEMA = {
    "type": "object",
    "properties": {
        "references": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "title": {"type": "string"}
                },
                "required": ["id", "type"]
            }
        }
    }
}

def validate_csl_json(data):
    """Validate CSL-JSON against schema."""
    try:
        jsonschema.validate(data, CSL_SCHEMA)
        return True, "Valid CSL-JSON"
    except jsonschema.ValidationError as e:
        return False, str(e)
```

### Required Fields Check

```python
def check_required_fields(csl_entry):
    """Check if entry has all required fields based on type."""
    required_by_type = {
        'article-journal': ['id', 'type', 'title', 'container-title', 'author', 'issued'],
        'book': ['id', 'type', 'title', 'author', 'publisher', 'issued'],
        'chapter': ['id', 'type', 'title', 'container-title', 'author', 'issued'],
        'paper-conference': ['id', 'type', 'title', 'container-title', 'author', 'issued'],
        'report': ['id', 'type', 'title', 'author', 'publisher', 'issued'],
        'webpage': ['id', 'type', 'title', 'URL', 'accessed'],
        'software': ['id', 'type', 'title', 'author', 'issued'],
        'thesis': ['id', 'type', 'title', 'author', 'publisher', 'genre', 'issued']
    }

    doc_type = csl_entry.get('type', 'document')
    required = required_by_type.get(doc_type, ['id', 'type'])

    missing = [field for field in required if field not in csl_entry]

    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, "All required fields present"
```

## Usage with Pandoc

### Basic Usage

```bash
# Generate bibliography from CSL-JSON
pandoc document.md --citeproc --bibliography=references.json -o output.pdf

# Use specific citation style
pandoc document.md --citeproc --bibliography=references.json \
  --csl=apa.csl -o output.pdf
```

### In Markdown

```markdown
---
bibliography: references.json
csl: apa.csl
---

Smith claims that climate change is accelerating [@smith2024neural].

# References
```

### YAML Metadata

```yaml
---
bibliography: references.json
csl: apa.csl
link-citations: true
reference-section-title: References
suppress-bibliography: false
---
```

## Style Files

### Common CSL Styles

| Style | File | Use Case |
|-------|------|----------|
| APA 7th | `apa.csl` | Social sciences |
| MLA 9th | `modern-language-association.csl` | Humanities |
| Chicago 17th | `chicago-author-date.csl` | History, general |
| IEEE | `ieee.csl` | Engineering, CS |
| Harvard | `harvard1.csl` | Various |
| Vancouver | `vancouver.csl` | Medicine, science |

### Download CSL Styles

```bash
# From official repository
git clone https://github.com/citation-style-language/styles.git

# Or download specific style
curl -O https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl
```

### Custom CSL Style

```xml
<?xml version="1.0" encoding="UTF-8"?>
<style xmlns="http://purl.org/net/xbiblio/csl" version="1.0" default-locale="en-US">
  <info>
    <title>Custom Style</title>
    <id>http://example.com/styles/custom</id>
    <link href="http://example.com/styles/custom" rel="self"/>
    <updated>2026-02-14T00:00:00+00:00</updated>
  </info>
  <citation>
    <layout>
      <text variable="citation-number"/>
    </layout>
  </citation>
  <bibliography>
    <layout>
      <text variable="title"/>
    </layout>
  </bibliography>
</style>
```

## Tools

### Zotero

- Export: File → Export Library → CSL JSON
- Import: File → Import
- Better BibTeX plugin for citation keys

### Mendeley

- Export: File → Export → CSL JSON
- Import: File → Import

### JabRef

- Export: File → Export → CSL JSON
- Import: File → Import into new library

### Python Libraries

```python
# citeproc-py
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc.source.json import CiteProcJSON

# Load CSL-JSON
bib_source = CiteProcJSON(json_data)

# Load style
bib_style = CitationStylesStyle('apa', validate=False)

# Create bibliography
bibliography = CitationStylesBibliography(
    bib_style,
    bib_source,
    formatter.html
)

# Format citation
citation = Citation([CitationItem('smith2024')])
bibliography.register(citation)
print(bibliography.cite(citation))
```

## Best Practices

1. Use consistent citation keys (e.g., `authorYearTitle`)
2. Include DOIs when available
3. Use standard date formats
4. Verify URLs are current
5. Include all required fields for the document type
6. Use UTF-8 encoding for special characters
7. Version control reference files
8. Use reference managers (Zotero, Mendeley)
9. Validate before using in production
10. Keep backups of reference libraries
11. Use consistent author name formatting
12. Include access dates for web resources

**BE CONSISTENT.** When creating citations, follow established patterns in the project.

*References:*

- [CSL Specification](https://docs.citationstyles.org/en/stable/specification.html)
- [CSL-JSON Schema](https://github.com/citation-style-language/schema)
- [Zotero CSL-JSON Documentation](https://www.zotero.org/support/dev/citation_styles/csl-json)
- [Pandoc Citations](https://pandoc.org/chunkedhtml-demo/8.20-citation-syntax.html)
- [CSL Style Repository](https://github.com/citation-style-language/styles)
