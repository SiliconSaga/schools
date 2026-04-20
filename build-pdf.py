"""
Build a printable PDF from the school board whitepaper markdown files.
Usage: python build-pdf.py
Output: whitepaper.pdf in the same directory
"""

import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Files in print order -- core stack then supporting stack
CORE_STACK = [
    "00-executive-summary.md",
    "01-instructional-bridge.md",
    "04-paraprofessional-audit.md",
    "05-health-insurance.md",
    "13-regulatory-leverage.md",
    "07-rfi-templates.md",
]

SUPPORTING_STACK = [
    "02-open-image-project.md",
    "03-community-maintenance.md",
    "11-grant-writing.md",
    "14-open-budget-tools.md",
    "06-open-governance.md",
]

SITE_URL = "schools.siliconsaga.net"


def setup_styles():
    """Create paragraph styles for the PDF."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Title'],
        fontSize=28,
        leading=34,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=HexColor('#1a1a2e'),
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=HexColor('#444466'),
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        'CoverURL',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=HexColor('#2255aa'),
        spaceBefore=24,
    ))
    styles.add(ParagraphStyle(
        'CoverDate',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=HexColor('#888888'),
        spaceBefore=8,
    ))
    styles.add(ParagraphStyle(
        'SectionDivider',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=HexColor('#666688'),
        spaceBefore=36,
        spaceAfter=24,
    ))
    styles.add(ParagraphStyle(
        'ModuleTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        spaceBefore=6,
        spaceAfter=4,
        textColor=HexColor('#1a1a2e'),
    ))
    styles.add(ParagraphStyle(
        'ModuleSubtitle',
        parent=styles['Italic'],
        fontSize=11,
        leading=14,
        textColor=HexColor('#555577'),
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        spaceBefore=16,
        spaceAfter=6,
        textColor=HexColor('#1a1a2e'),
    ))
    styles.add(ParagraphStyle(
        'H3',
        parent=styles['Heading3'],
        fontSize=12,
        leading=15,
        spaceBefore=12,
        spaceAfter=4,
        textColor=HexColor('#333355'),
    ))
    styles['BodyText'].fontSize = 10
    styles['BodyText'].leading = 14
    styles['BodyText'].spaceAfter = 6
    styles.add(ParagraphStyle(
        'BulletItem',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        leftIndent=20,
        bulletIndent=8,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        'NumberedItem',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        leftIndent=20,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        'BlockQuote',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        leftIndent=24,
        rightIndent=12,
        textColor=HexColor('#444444'),
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        'CodeBlock',
        parent=styles['Code'],
        fontSize=8,
        leading=10,
        leftIndent=12,
        spaceAfter=6,
        backColor=HexColor('#f5f5f5'),
    ))
    styles.add(ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=HexColor('#999999'),
    ))

    return styles


def strip_front_matter(lines):
    """Remove Jekyll YAML front matter."""
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                return lines[i + 1:]
    return lines


def strip_metadata_block(lines):
    """Remove the Impact/Effort/Timeline metadata bullet block and surrounding ---."""
    # Find the first "- **Impact" or "- **This is" or "- **Document Type" line
    meta_start = None
    meta_end = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if meta_start is None:
            if stripped.startswith('- **Impact') or \
               stripped.startswith('- **This is') or \
               stripped.startswith('- **Document Type'):
                meta_start = i
                # Walk backward to find the --- before it
                for j in range(i - 1, max(i - 4, -1), -1):
                    if lines[j].strip() == '---':
                        meta_start = j
                        break
        elif meta_end is None:
            # We're past the start; look for the closing ---
            if stripped == '---':
                meta_end = i
                break
            elif stripped and not stripped.startswith('- **') and \
                    not line.startswith('  '):
                # Hit non-metadata content before a closing ---
                meta_end = i - 1
                break

    if meta_start is not None:
        if meta_end is None:
            meta_end = meta_start  # safety
        # Remove lines from meta_start through meta_end (inclusive)
        return lines[:meta_start] + lines[meta_end + 1:]

    return lines


def strip_nav_links(lines):
    """Remove 'Back to Index | Next:' nav links at the bottom."""
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('[Back to Index') or \
           stripped.startswith('*[Back to Index') or \
           (stripped.startswith('[Back to') and 'Next:' in stripped):
            continue
        result.append(line)
    return result


def md_inline(text):
    """Convert inline markdown to reportlab XML markup."""
    # Bold + italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" size="9">\1</font>', text)
    # Links: [text](url) -> text (url) for print
    text = re.sub(r'\[([^\]]+)\]\(https?://[^\)]+\)', r'\1', text)
    # Internal links: [text](page) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Escape XML entities that reportlab needs
    # (but not ones we already converted to tags)
    return text


def parse_table(lines, start_idx):
    """Parse a markdown table starting at start_idx. Returns (rows, end_idx)."""
    rows = []
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith('|'):
            break
        cells = [c.strip() for c in line.split('|')[1:-1]]
        # Skip separator rows
        if cells and all(re.match(r'^[-:]+$', c) for c in cells):
            i += 1
            continue
        rows.append(cells)
        i += 1
    return rows, i


def build_table(rows, styles):
    """Build a reportlab Table from parsed rows."""
    if not rows:
        return None

    # Convert markdown inline formatting in cells
    table_data = []
    for row_idx, row in enumerate(rows):
        styled_row = []
        for cell in row:
            cell_text = md_inline(cell)
            if row_idx == 0:
                styled_row.append(Paragraph(cell_text, styles['BodyText']))
            else:
                styled_row.append(Paragraph(cell_text, styles['BodyText']))
        table_data.append(styled_row)

    if not table_data:
        return None

    # Calculate column widths
    num_cols = max(len(r) for r in table_data)
    available = 6.5 * inch
    col_width = available / num_cols

    t = Table(table_data, colWidths=[col_width] * num_cols)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e8e8f0')),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def md_to_story(filepath, styles, is_exec_summary=False):
    """Convert a markdown file to a list of reportlab flowables."""
    story = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lines = [l.rstrip('\r\n') for l in lines]
    lines = strip_front_matter(lines)
    if not is_exec_summary:
        lines = strip_metadata_block(lines)
    lines = strip_nav_links(lines)

    i = 0
    in_code_block = False
    code_lines = []
    in_blockquote = False
    bq_lines = []
    paragraph_lines = []

    def flush_paragraph():
        nonlocal paragraph_lines
        if paragraph_lines:
            text = ' '.join(paragraph_lines)
            text = md_inline(text)
            story.append(Paragraph(text, styles['BodyText']))
            paragraph_lines = []

    def flush_blockquote():
        nonlocal bq_lines, in_blockquote
        if bq_lines:
            text = ' '.join(bq_lines)
            text = md_inline(text)
            story.append(Paragraph(text, styles['BlockQuote']))
            bq_lines = []
        in_blockquote = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code blocks
        if stripped.startswith('```'):
            if in_code_block:
                flush_paragraph()
                code_text = '<br/>'.join(
                    l.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    for l in code_lines
                )
                if code_text:
                    story.append(Paragraph(code_text, styles['CodeBlock']))
                code_lines = []
                in_code_block = False
            else:
                flush_paragraph()
                flush_blockquote()
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Horizontal rule
        if stripped == '---' or stripped == '***' or stripped == '___':
            flush_paragraph()
            flush_blockquote()
            story.append(HRFlowable(
                width="80%", thickness=0.5,
                color=HexColor('#cccccc'), spaceAfter=8, spaceBefore=8
            ))
            i += 1
            continue

        # Empty line
        if not stripped:
            flush_paragraph()
            if in_blockquote:
                flush_blockquote()
            i += 1
            continue

        # Headings
        if stripped.startswith('# ') and not stripped.startswith('## '):
            flush_paragraph()
            flush_blockquote()
            text = md_inline(stripped[2:])
            story.append(Paragraph(text, styles['ModuleTitle']))
            i += 1
            continue

        if stripped.startswith('## '):
            flush_paragraph()
            flush_blockquote()
            text = md_inline(stripped[3:])
            story.append(Paragraph(text, styles['H2']))
            i += 1
            continue

        if stripped.startswith('### ') or stripped.startswith('#### '):
            flush_paragraph()
            flush_blockquote()
            level = 4 if stripped.startswith('####') else 3
            text = md_inline(stripped[level + 1:])
            story.append(Paragraph(text, styles['H3']))
            i += 1
            continue

        # Subtitle line (italic on its own line right after title)
        if stripped.startswith('*') and stripped.endswith('*') and \
           not stripped.startswith('**') and len(stripped) > 20:
            flush_paragraph()
            text = stripped[1:-1]
            story.append(Paragraph(md_inline(text), styles['ModuleSubtitle']))
            i += 1
            continue

        # Table
        if stripped.startswith('|'):
            flush_paragraph()
            flush_blockquote()
            rows, end_idx = parse_table(lines, i)
            t = build_table(rows, styles)
            if t:
                story.append(Spacer(1, 6))
                story.append(t)
                story.append(Spacer(1, 6))
            i = end_idx
            continue

        # Blockquote
        if stripped.startswith('> '):
            flush_paragraph()
            bq_text = stripped[2:]
            bq_lines.append(bq_text)
            in_blockquote = True
            i += 1
            continue

        if in_blockquote and not stripped.startswith('>'):
            flush_blockquote()

        # Bullet points
        if stripped.startswith('- ') or stripped.startswith('* '):
            flush_paragraph()
            bullet_text = stripped[2:]
            # Collect continuation lines
            while i + 1 < len(lines) and lines[i + 1].startswith('  ') \
                    and not lines[i + 1].strip().startswith('- ') \
                    and not lines[i + 1].strip().startswith('* '):
                i += 1
                bullet_text += ' ' + lines[i].strip()
            text = md_inline(bullet_text)
            story.append(Paragraph(
                text, styles['BulletItem'],
                bulletText='\u2022'
            ))
            i += 1
            continue

        # Numbered items
        num_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if num_match:
            flush_paragraph()
            num = num_match.group(1)
            item_text = num_match.group(2)
            # Collect continuation lines
            while i + 1 < len(lines) and lines[i + 1].startswith('   ') \
                    and not re.match(r'^\d+\.', lines[i + 1].strip()):
                i += 1
                item_text += ' ' + lines[i].strip()
            text = md_inline(item_text)
            story.append(Paragraph(
                f"{num}. {text}", styles['NumberedItem']
            ))
            i += 1
            continue

        # Regular paragraph text -- accumulate
        paragraph_lines.append(stripped)
        i += 1

    flush_paragraph()
    flush_blockquote()

    return story


def add_footer(canvas, doc):
    """Add page footer with site URL and page number."""
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(HexColor('#999999'))
    canvas.drawString(
        inch, 0.5 * inch,
        SITE_URL
    )
    canvas.drawRightString(
        letter[0] - inch, 0.5 * inch,
        f"Page {doc.page}"
    )
    canvas.restoreState()


def build_cover(styles):
    """Build cover page."""
    story = []
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph(
        "Community Solutions for the<br/>School Budget Crisis",
        styles['CoverTitle']
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "A Resource-Optimized Model for District Stability",
        styles['CoverSubtitle']
    ))
    story.append(Paragraph(
        "Bridging the Budget Gap through Community-Led Infrastructure<br/>"
        "&amp; Shared Service Grants",
        styles['CoverSubtitle']
    ))
    story.append(Spacer(1, 36))
    story.append(HRFlowable(
        width="40%", thickness=1,
        color=HexColor('#888888'), spaceAfter=36
    ))
    story.append(Paragraph(
        f'<a href="https://{SITE_URL}">{SITE_URL}</a>',
        styles['CoverURL']
    ))
    story.append(Paragraph(
        "April 2026",
        styles['CoverDate']
    ))
    story.append(PageBreak())
    return story


def main():
    output_path = os.path.join(SCRIPT_DIR, "whitepaper.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = setup_styles()
    story = []

    # Cover page
    story.extend(build_cover(styles))

    # Core stack
    for idx, filename in enumerate(CORE_STACK):
        filepath = os.path.join(SCRIPT_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {filename}")
            continue

        print(f"  Adding: {filename}")
        is_exec = filename.startswith("00-")
        story.extend(md_to_story(filepath, styles, is_exec_summary=is_exec))

        if idx < len(CORE_STACK) - 1:
            story.append(PageBreak())

    # Divider between stacks
    story.append(PageBreak())
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("Supporting Materials", styles['SectionDivider']))
    story.append(HRFlowable(
        width="60%", thickness=0.5,
        color=HexColor('#aaaaaa'), spaceAfter=12
    ))
    story.append(Paragraph(
        "Additional proposals and detail supporting the core modules above.",
        styles['CoverSubtitle']
    ))
    story.append(PageBreak())

    # Supporting stack
    for idx, filename in enumerate(SUPPORTING_STACK):
        filepath = os.path.join(SCRIPT_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {filename}")
            continue

        print(f"  Adding: {filename}")
        story.extend(md_to_story(filepath, styles))

        if idx < len(SUPPORTING_STACK) - 1:
            story.append(PageBreak())

    # Build
    print(f"\nBuilding PDF...")
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Done: {output_path}")


if __name__ == "__main__":
    main()
