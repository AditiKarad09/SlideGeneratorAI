import google.generativeai as genai

# --------------------------------------------------------------------
# 0. CONFIGURE GEMINI
# --------------------------------------------------------------------
genai.configure(api_key="Add your own gemini api key here")  # Replace with your actual key
model = genai.GenerativeModel("gemini-1.5-flash")
