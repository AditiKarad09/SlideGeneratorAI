# Slide Generator AI

## Overview

This project is a Python-based application that automates the creation of presentations and documentation from various file formats such as CSV, JSON, and PDF. It integrates with the Gemini API to analyze and structure the data, generate visualizations, and produce PowerPoint presentations and Word documents.

## Features

- **Data Parsing:** Processes CSV, JSON, and PDF files to extract relevant content.
- **Chart Generation:** Automatically generates charts based on the input data using Python libraries like Matplotlib and Seaborn.
- **Presentation Creation:** Generates PowerPoint presentations with dynamically structured slides.
- **Documentation Generation:** Creates Word documents summarizing the analyzed data.
- **Light Blue Background:** Adds a visually appealing light blue background to all slides in the PowerPoint presentation.

## Prerequisites

- **Python Version:** Ensure Python 3.8+ is installed.
- **Install Required Libraries:** Install dependencies listed in `requirements.txt` by running:

  ```bash
  pip install -r requirements.txt
  ```

## Configuration

1. **Replace the Gemini API Key:**
   - Open `gemini_config.py`.
   - Replace the placeholder API key with your own valid Gemini API key.

     Example:
     ```python
     model = GeminiAPI(api_key="your_api_key_here")
     ```

## File Structure

```
.
├── main.py                   # Main script to run the application
├── file_processing.py        # Handles file validation and parsing (CSV, JSON, PDF, etc.)
├── chart_function.py         # Generates charts and saves them as images
├── ppt_generation.py         # Creates PowerPoint presentations
├── word_documentation.py     # Generates Word documents
├── gemini_config.py          # Configuration for interacting with the Gemini API
├── helpers.py                # Helper functions for text and data cleanup
├── plot_code.py              # Handles plotting and saving charts
└── requirements.txt          # Required Python libraries
```

## How It Works

1. **File Processing:**
   - The `file_processing.py` module validates the file format and processes content based on the file type (CSV, JSON, PDF, etc.).

2. **Data Analysis:**
   - Relevant data is analyzed and passed to the Gemini API for summarization and structuring.

3. **Chart Generation:**
   - Charts are generated dynamically using Matplotlib and Seaborn, based on the extracted data.

4. **Presentation Creation:**
   - Slides are created in PowerPoint using the `pptx` library, structured according to the output from the Gemini API.
   - Each slide has a light blue background for a consistent and professional look.

5. **Documentation Creation:**
   - Word documents are generated with headings, bullet points, tables, and charts, summarizing the data and insights.

## How to Run the Code

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/SlideGeneratorAI.git
   cd SlideGeneratorAI
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Replace the Gemini API Key:**
   - Open `gemini_config.py` and replace the placeholder API key with your own.

4. **Run the Application:**

   ```bash
   python main.py
   ```

5. **Provide the File Path:**
   - Enter the path to the input file (CSV, JSON, or PDF) when prompted.

6. **Output:**
   - The script will generate:
     - A PowerPoint presentation (`output2.pptx`)
     - A Word document (`output_document.docx`)
     - Charts saved as individual image files (e.g., `chart1.png`)

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.


