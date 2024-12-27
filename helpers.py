import re

# --------------------------------------------------------------------
# 3. HELPER FOR SPLITTING BULLETS ON PERIOD
# --------------------------------------------------------------------

def split_bullets_on_period(bullet_text):
    """
    Splits bullet_text on a period + optional space => distinct bullet lines.
    """
    bullet_text = bullet_text.strip()
    lines = re.split(r"\.\s+|\.$", bullet_text)
    lines = [l.strip() for l in lines if l.strip()]
    return lines

# --------------------------------------------------------------------
# 4. HELPERS FOR REFERENCES SLIDE CLEANUP
# --------------------------------------------------------------------

def cleanup_unwanted_references_text(text):
    """
    Removes placeholder or extra lines from the references slide content.
    For example, remove lines like:
      "Remember to replace placeholder text with actual data..."
    Adjust the patterns as needed to remove more unwanted lines.
    """
    # Remove any mention of "Remember to replace placeholder text..." case-insensitively
    text = re.sub(r"(?i)remember to replace placeholder.*", "", text).strip()
    # Remove mention of "The LaTeX document provides ..." if present
    text = re.sub(r"(?i)the latex document provides.*", "", text).strip()
    return text
