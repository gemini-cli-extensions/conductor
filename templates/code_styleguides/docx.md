# DOCX (Word Document) Style Guide

This document outlines standards for creating, formatting, and managing DOCX files programmatically in this project.

## When to Use DOCX vs Other Formats

### Use DOCX When

- **Business documents**: Contracts, proposals, formal reports
- **Collaboration**: Documents requiring track changes and comments
- **Rich formatting**: Complex layouts with mixed content types
- **Templates**: Documents with dynamic placeholders
- **Legacy compatibility**: Integration with Microsoft Office workflows
- **Signatures**: Documents requiring digital signatures

### Use Alternatives When

- **Markdown**: Documentation, READMEs, simple formatted text
- **PDF**: Final distribution, print-ready documents
- **HTML**: Web content, interactive documents
- **LaTeX**: Academic papers, complex mathematical content

## Tool Selection

### python-docx

Best for creating documents from scratch:

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
doc.add_heading('Document Title', 0)
doc.save('output.docx')
```

### docxtpl

Best for template-based documents:

```python
from docxtpl import DocxTemplate

doc = DocxTemplate('template.docx')
context = {
    'company_name': 'Acme Corp',
    'date': '2026-02-14',
    'total': 1500.00
}
doc.render(context)
doc.save('generated.docx')
```

## Document Structure

### Standard Document Outline

```
1. Title Page
   - Document title
   - Subtitle (if any)
   - Author/organization
   - Date
   - Version

2. Table of Contents (optional)

3. Executive Summary (optional)

4. Main Content
   - Sections with clear hierarchy
   - Consistent formatting

5. Appendices (if needed)

6. References/Bibliography (if needed)
```

### Title Page Example

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_title_page(doc, title, subtitle='', author='', date=''):
    # Title
    title_para = doc.add_paragraph()
    title_run = title_para.add_run(title)
    title_run.bold = True
    title_run.font.size = Pt(24)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle
    if subtitle:
        doc.add_paragraph()
        subtitle_para = doc.add_paragraph()
        subtitle_run = subtitle_para.add_run(subtitle)
        subtitle_run.font.size = Pt(16)
        subtitle_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Spacing
    for _ in range(5):
        doc.add_paragraph()

    # Author and date
    if author:
        author_para = doc.add_paragraph()
        author_run = author_para.add_run(author)
        author_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if date:
        date_para = doc.add_paragraph()
        date_run = date_para.add_run(date)
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Page break
    doc.add_page_break()
```

## Typography

### Font Standards

```python
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE

# Set default font
def set_default_font(doc, font_name='Calibri', font_size=11):
    style = doc.styles['Normal']
    font = style.font
    font.name = font_name
    font.size = Pt(font_size)

# Heading styles
def configure_heading_styles(doc):
    # Heading 1
    h1 = doc.styles['Heading 1']
    h1.font.name = 'Calibri'
    h1.font.size = Pt(16)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # Heading 2
    h2 = doc.styles['Heading 2']
    h2.font.name = 'Calibri'
    h2.font.size = Pt(14)
    h2.font.bold = True
```

### Color Palette

```python
from docx.shared import RGBColor

# Standard colors
COLORS = {
    'black': RGBColor(0x00, 0x00, 0x00),
    'dark_gray': RGBColor(0x44, 0x44, 0x44),
    'medium_gray': RGBColor(0x88, 0x88, 0x88),
    'light_gray': RGBColor(0xCC, 0xCC, 0xCC),
    'primary_blue': RGBColor(0x00, 0x66, 0xCC),
    'accent_green': RGBColor(0x00, 0x88, 0x00),
    'warning_red': RGBColor(0xCC, 0x00, 0x00)
}
```

## Headings Hierarchy

```python
# Create document structure
def create_document_structure(doc):
    # Title
    doc.add_heading('Main Title', level=0)

    # Section 1
    doc.add_heading('1. Introduction', level=1)
    doc.add_paragraph('Introduction content...')

    # Subsection 1.1
    doc.add_heading('1.1 Background', level=2)
    doc.add_paragraph('Background content...')

    # Subsection 1.2
    doc.add_heading('1.2 Objectives', level=2)
    doc.add_paragraph('Objectives content...')

    # Section 2
    doc.add_heading('2. Methodology', level=1)
    doc.add_paragraph('Methodology content...')
```

## Paragraphs and Alignment

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

# Paragraph with custom formatting
def add_formatted_paragraph(doc, text, alignment='left', bold=False,
                           italic=False, space_after=Pt(12)):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic

    # Alignment
    if alignment == 'center':
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif alignment == 'right':
        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif alignment == 'justify':
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Spacing
    para.paragraph_format.space_after = space_after

    return para

# Line spacing
para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
```

## Lists

### Bullet Lists

```python
# Create bullet list
bullet_list = doc.add_paragraph('First item', style='List Bullet')
doc.add_paragraph('Second item', style='List Bullet')
doc.add_paragraph('Third item', style='List Bullet')

# Nested bullets
outer = doc.add_paragraph('Outer item', style='List Bullet')
inner = doc.add_paragraph('Nested item', style='List Bullet 2')
```

### Numbered Lists

```python
# Create numbered list
doc.add_paragraph('First step', style='List Number')
doc.add_paragraph('Second step', style='List Number')
doc.add_paragraph('Third step', style='List Number')

# Restart numbering (if needed)
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def restart_numbering(paragraph):
    """Restart numbering for a paragraph."""
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    numPr = OxmlElement('w:numPr')
    ilvl = OxmlElement('w:ilvl')
    ilvl.set(qn('w:val'), '0')
    numId = OxmlElement('w:numId')
    numId.set(qn('w:val'), '1')
    numPr.append(ilvl)
    numPr.append(numId)
    pPr.append(numPr)
```

## Tables Creation and Formatting

```python
from docx.shared import Inches

def create_formatted_table(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Light Grid Accent 1'

    # Header row
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        header_cells[i].text = header
        # Make header bold
        for paragraph in header_cells[i].paragraphs:
            for run in paragraph.runs:
                run.font.bold = True

    # Data rows
    for row_data in data:
        row = table.add_row()
        for i, value in enumerate(row_data):
            row.cells[i].text = str(value)

    # Set column widths
    if col_widths:
        for i, width in enumerate(col_widths):
            for cell in table.columns[i].cells:
                cell.width = Inches(width)

    return table

# Example usage
headers = ['Item', 'Quantity', 'Price', 'Total']
data = [
    ['Product A', '2', '$50.00', '$100.00'],
    ['Product B', '1', '$75.00', '$75.00'],
    ['Product C', '3', '$25.00', '$75.00']
]
create_formatted_table(doc, headers, data, [2, 1, 1, 1])
```

## Images and Captions

```python
from docx.shared import Inches

def add_image_with_caption(doc, image_path, caption_text, width_inches=5):
    # Add image
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    run.add_picture(image_path, width=Inches(width_inches))

    # Add caption
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_run = caption.add_run(f'Figure: {caption_text}')
    caption_run.italic = True
    caption_run.font.size = Pt(10)

    # Add spacing after
    caption.paragraph_format.space_after = Pt(12)
```

## Page Layout and Margins

```python
from docx.shared import Inches

def set_page_layout(doc, margin_top=1, margin_bottom=1,
                   margin_left=1, margin_right=1,
                   orientation='portrait'):
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(margin_top)
        section.bottom_margin = Inches(margin_bottom)
        section.left_margin = Inches(margin_left)
        section.right_margin = Inches(margin_right)

        if orientation == 'landscape':
            section.orientation = WD_ORIENT.LANDSCAPE
```

## Headers and Footers

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_header_footer(doc, header_text='', footer_text='', page_numbers=True):
    section = doc.sections[0]

    # Header
    header = section.header
    header_para = header.paragraphs[0]
    header_para.text = header_text
    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Footer
    footer = section.footer
    footer_para = footer.paragraphs[0]

    if page_numbers:
        # Add page number field
        footer_para.text = footer_text + ' ' if footer_text else ''
        footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Add page number field
        run = footer_para.add_run()
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')

        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"

        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')

        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
```

## Hyperlinks

```python
from docx.oxml.shared import OxmlElement, qn

def add_hyperlink(paragraph, url, text):
    """Add hyperlink to paragraph."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # Style hyperlink
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0000FF')
    rPr.append(color)

    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

    return hyperlink
```

## Templating with docxtpl

### Template Creation

```xml
<!-- In Word template, use Jinja2 syntax -->
Company: {{ company_name }}
Date: {{ date }}

Dear {{ client_name }},

{% for item in items %}
- {{ item.name }}: {{ item.price }}
{% endfor %}

Total: ${{ "%.2f"|format(total) }}
```

### Template Rendering

```python
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches

def render_document_template(template_path, output_path, context):
    doc = DocxTemplate(template_path)

    # Add images if needed
    if 'logo' in context:
        context['logo'] = InlineImage(doc, context['logo'], width=Inches(2))

    # Add complex objects
    context['formatted_date'] = context['date'].strftime('%B %d, %Y')

    doc.render(context)
    doc.save(output_path)

# Usage
context = {
    'company_name': 'Acme Corporation',
    'client_name': 'John Smith',
    'date': datetime.now(),
    'items': [
        {'name': 'Widget A', 'price': 99.99},
        {'name': 'Widget B', 'price': 149.99}
    ],
    'total': 249.98,
    'logo': 'company_logo.png'
}

render_document_template('template.docx', 'output.docx', context)
```

## Markdown to DOCX Conversion

```python
import markdown
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def markdown_to_docx(markdown_text, output_path):
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text)

    doc = Document()

    # Simple HTML parsing (for production, use BeautifulSoup)
    import re

    # Headers
    for level in range(1, 7):
        pattern = f'<h{level}>(.*?)</h{level}>'
        for match in re.finditer(pattern, html):
            doc.add_heading(match.group(1), level=level)

    # Paragraphs
    for match in re.finditer(r'<p>(.*?)</p>', html, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1))  # Remove inline tags
        doc.add_paragraph(text)

    # Lists
    # ... handle ul/ol

    doc.save(output_path)
```

## Accessibility

```python
def add_accessibility_features(doc):
    """Add accessibility features to document."""

    # Set document title
    doc.core_properties.title = 'Document Title'
    doc.core_properties.author = 'Author Name'

    # Add alt text to images (when adding images)
    # Note: python-docx doesn't directly support alt text well
    # Consider using OOXML for advanced accessibility

    # Ensure proper heading hierarchy
    # Check that headings don't skip levels

    # Use semantic table headers
    for table in doc.tables:
        # First row should be header
        pass
```

## Best Practices

1. Use templates for consistent branding
2. Define styles rather than inline formatting
3. Keep a style guide document
4. Version control templates separately
5. Use relative paths for images
6. Add document properties (title, author, keywords)
7. Test generated documents in multiple Word versions
8. Handle special characters properly
9. Use tables for tabular data, not for layout
10. Include page numbers in long documents
11. Add table of contents for documents >5 pages
12. Use built-in styles (Heading 1, List Bullet) for structure

**BE CONSISTENT.** When generating documents, follow established templates and styles.

*References:*

- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [docxtpl Documentation](https://docxtpl.readthedocs.io/)
- [Office Open XML (OOXML) Standard](https://ecma-international.org/publications-and-standards/standards/ecma-376/)
