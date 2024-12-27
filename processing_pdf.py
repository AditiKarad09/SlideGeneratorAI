import pdfplumber
import re

def latex_escape(text):
    """
    Escape common LaTeX special characters in a given string.
    This helps prevent LaTeX compilation errors for certain symbols.
    """
    replacements = {
        r'\\': r'\\textbackslash{}',
        r'&': r'\&',
        r'%': r'\%',
        r'\$': r'\$',
        r'#': r'\#',
        r'_': r'\_',
        r'{': r'\{',
        r'}': r'\}',
        r'~': r'\textasciitilde{}',
        r'\^': r'\textasciicircum{}',
    }
    for old, new in replacements.items():
        text = re.sub(old, new, text)
    return text


def extract_text_chunks(page):
    """
    Return a list of dict items like:
       {
         'type': 'text',
         'top': float,
         'bottom': float,
         'left': float,
         'right': float,
         'content': "some text line"
       }
    We group words by a rounded 'top' to form lines.
    """
    words = page.extract_words()  # each is { x0, x1, top, bottom, text }
    if not words:
        return []

    from collections import defaultdict
    line_map = defaultdict(list)

    # Group words by approximate line (rounded top)
    for w in words:
        top_key = round(w["top"])
        line_map[top_key].append(w)

    text_chunks = []
    for top_key in sorted(line_map.keys()):
        items = line_map[top_key]
        # Sort words by left coordinate
        items = sorted(items, key=lambda x: x["x0"])

        # Build a single text line
        line_text = " ".join([i["text"] for i in items])
        top = min(i["top"] for i in items)
        bottom = max(i["bottom"] for i in items)
        left = min(i["x0"] for i in items)
        right = max(i["x1"] for i in items)

        text_chunks.append({
            "type": "text",
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "content": line_text
        })

    return text_chunks


def extract_tables_with_bbox(page):
    """
    Use page.find_tables() to locate table bounding boxes and row data.
    Return a list of dict items like:
       {
         'type': 'table',
         'top': float,
         'bottom': float,
         'left': float,
         'right': float,
         'content': [ [...], [...], ... ]  # row data
       }
    """
    table_objs = page.find_tables()  # returns Table objects
    table_chunks = []

    for t in table_objs:
        x0, top, x1, bottom = t.bbox  # (x0, top, x1, bottom)
        data = t.extract()  # 2D list of cell data

        table_chunks.append({
            "type": "table",
            "top": top,
            "bottom": bottom,
            "left": x0,
            "right": x1,
            "content": data
        })

    return table_chunks


def boxes_overlap(boxA, boxB):
    """
    Check if two bounding boxes overlap (even partially).
    Each box is a dict with 'top', 'bottom', 'left', 'right'.
    The coordinate system in pdfplumber => 'top' < 'bottom' if measured from the top of the page.

    Overlap occurs if horizontally and vertically they intersect.
    """
    return not (
        boxA["right"] <= boxB["left"] or
        boxA["left"] >= boxB["right"] or
        boxA["bottom"] <= boxB["top"] or
        boxA["top"] >= boxB["bottom"]
    )


def table_to_latex(table_data):
    """
    Convert a 2D list (rows of strings) to a simple LaTeX tabular environment.
    Columns are separated by & and rows end with \\\\.
    """
    if not table_data:
        return ""

    # Find max number of columns across all rows
    max_cols = max(len(row) for row in table_data if row)
    if max_cols == 0:
        return ""

    latex = []
    # Example: 3 columns => {c|c|c}
    latex.append("\\begin{tabular}{" + "|".join(["c"] * max_cols) + "}")
    latex.append("\\hline")

    for row in table_data:
        # Ensure each row has the same number of columns
        if len(row) < max_cols:
            row += [""] * (max_cols - len(row))

        # Escape LaTeX specials
        escaped_cells = [latex_escape(cell.strip()) for cell in row]
        row_str = " & ".join(escaped_cells) + " \\\\"
        latex.append(row_str)
        latex.append("\\hline")

    latex.append("\\end{tabular}")
    return "\n".join(latex)


def process_pdf_in_flow(file_path):
    """
    1) For each page:
       - Extract text lines (with bounding boxes).
       - Extract tables (with bounding boxes).
       - Remove text lines that overlap any table's bounding box.
       - Combine the filtered text + tables, sort by 'top' coordinate.
       - Output them in that order to build a LaTeX doc string.
    2) Return the final LaTeX code as a string.
    """
    try:
        doc_latex = []
        doc_latex.append("\\documentclass{article}")
        doc_latex.append("\\usepackage[utf8]{inputenc}")
        doc_latex.append("\\usepackage{array}")
        doc_latex.append("\\begin{document}")

        with pdfplumber.open(file_path) as pdf:
            for pagenum, page in enumerate(pdf.pages, start=1):
                doc_latex.append(f"% --- Page {pagenum} ---")

                # Extract text lines with bounding boxes
                text_chunks = extract_text_chunks(page)
                # Extract tables with bounding boxes
                table_chunks = extract_tables_with_bbox(page)

                # Filter out text that overlaps any table
                filtered_text = []
                for line in text_chunks:
                    overlap_any_table = False
                    for tbl in table_chunks:
                        if boxes_overlap(line, tbl):
                            overlap_any_table = True
                            break
                    if not overlap_any_table:
                        filtered_text.append(line)

                # Combine filtered text and tables
                combined = filtered_text + table_chunks
                # Sort by 'top' to preserve vertical reading order
                combined_sorted = sorted(combined, key=lambda x: x["top"])

                # Build LaTeX in sorted order
                for item in combined_sorted:
                    if item["type"] == "text":
                        # Insert text as a line (with LaTeX escaping)
                        line_escaped = latex_escape(item["content"])
                        doc_latex.append(line_escaped + "\\\\")
                    else:
                        # It's a table
                        doc_latex.append("\\begin{center}")
                        doc_latex.append(table_to_latex(item["content"]))
                        doc_latex.append("\\end{center}")
                        doc_latex.append("")  # blank line for spacing

        doc_latex.append("\\end{document}")
        return "\n".join(doc_latex)

    except Exception as e:
        return f"Error processing PDF: {e}"


def process_pdf(file_path):
    """
    Top-level function called by dataValidation.py for PDFs.
    Returns a dict with a 'type': 'latex' and the 'content': <LaTeX string>.
    """
    latex_code = process_pdf_in_flow(file_path)
    return {
        "type": "latex",
        "content": latex_code
    }
