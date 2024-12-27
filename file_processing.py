import json
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from processing_pdf import process_pdf  # Your existing PDF processing function

# --------------------------------------------------------------------
# 1. FILE PROCESSING FUNCTIONS
# --------------------------------------------------------------------

def process_text(text):
    """Convert plain text into structured JSON."""
    return {"type": "text", "content": text.strip()}


def process_json(json_str):
    """
    Parse JSON string and ensure it is in a valid structure for processing charts, PPTs, and Word documentation.
    """
    try:
        json_data = json.loads(json_str)

        # Check if JSON contains a valid structure for processing
        if isinstance(json_data, list):  # Assuming a list of dictionaries for tabular data
            return {"type": "table", "content": json_data}
        elif isinstance(json_data, dict):  # If JSON is a dictionary
            return {"type": "json", "content": json_data}
        else:
            return {"error": "Unsupported JSON format"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {str(e)}"}

def process_table(file_path):
    """Read tabular data (CSV/Excel) and convert it to JSON."""
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            return {"error": "Unsupported table format"}
        return {"type": "table", "content": df.to_dict(orient="records")}
    except Exception as e:
        return {"error": f"Failed to process table: {str(e)}"}

def process_css(css_str):
    """Parse CSS and return a JSON representation."""
    try:
        soup = BeautifulSoup(css_str, "html.parser")
        rules = []
        for rule in soup.text.split("}"):
            if "{" in rule:
                selector, properties = rule.split("{", 1)
                rules.append({"selector": selector.strip(), "properties": properties.strip()})
        return {"type": "css", "content": rules}
    except Exception as e:
        return {"error": f"Failed to process CSS: {str(e)}"}

def validate_and_convert(file_path):
    """
    Validate and convert different file types to a dictionary representation.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return process_text(f.read())

        elif ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                return process_json(f.read())

        elif ext in [".csv", ".xlsx"]:
            return process_table(file_path)

        elif ext == ".css":
            with open(file_path, "r", encoding="utf-8") as f:
                return process_css(f.read())

        elif ext == ".pdf":
            pdf_result = process_pdf(file_path)  # Assuming you have a process_pdf function
            if pdf_result.get("type") == "latex":
                return {"type": "latex", "content": pdf_result["content"]}
            else:
                return pdf_result
        else:
            return {"error": "Unsupported file format"}
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}
