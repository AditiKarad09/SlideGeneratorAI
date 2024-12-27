import google.generativeai as genai

# --------------------------------------------------------------------
# 0. CONFIGURE GEMINI
# --------------------------------------------------------------------
genai.configure(api_key="AIzaSyBq6S9KcXYfNzFiv32X0wtBen7GSEQu7gU")  # Replace with your actual key
model = genai.GenerativeModel("gemini-1.5-flash")
