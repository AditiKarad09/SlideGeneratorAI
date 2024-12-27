# import json
#
# import pandas as pd
# from file_processing import validate_and_convert
# from chart_functions import gemini_recommend_chart_type,save_and_run_plot_code
# from ppt_generation import generate_pptx_from_gemini
# from word_documentation import generate_word_documentation
# from gemini_config import model
#
# # --------------------------------------------------------------------
# # 6. MAIN FLOW
# # --------------------------------------------------------------------
# def get_document_summary(text):
#     """
#     (Optional) A helper to call Gemini for a summary of text from the document.
#     This can be appended into the final data that we pass to `generate_pptx_from_gemini`.
#     """
#     prompt = f"""
#     Please provide a concise summary of the following text:
#
#     {text}
#     """
#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Error calling Gemini API for summary: {str(e)}"
#
#
# if __name__ == "__main__":
#     print("This project will generate a proper summary of the provided data and create a Powerpoint"
#           " Presentation and a Word Documentation \n(Graphs are created if there is any tabular data in the provided "
#           "files and those are attached in the presentation and the documentation)")
#     print("Please enter either a JASON file , a PDF or a CSV File")
#
#     file_path = input("Enter the file path: ")
#     data = validate_and_convert(file_path)
#
#     if "error" in data:
#         print("Error processing file:", data["error"])
#         exit()
#
#     doc_summary = ""
#     if data.get("type") == "text":
#         # If it's just text, we might want to do a summary
#         doc_summary = get_document_summary(data["content"])
#         data["document_summary"] = doc_summary
#
#     # If the data is a table, generate a chart if possible
#     if data.get("type") == "json":
#         # If JSON is a dictionary, attempt to visualize key-value pairs
#         doc_summary = get_document_summary(json.dumps(data["content"], indent=4))
#         data["document_summary"] = doc_summary
#
#         # Example: Handle dictionary structures for graphing
#         df = pd.DataFrame.from_dict(data["content"], orient="index").reset_index()
#         df.columns = ["Key", "Value"]  # Customize based on JSON structure
#
#         # Generate charts if possible
#         chart_type = gemini_recommend_chart_type(df)
#         save_and_run_plot_code(chart_type, "plot_code.py")
#
#     elif data.get("type") == "table":
#         # Existing table handling remains unchanged
#         df = pd.DataFrame(data["content"])
#         doc_summary = get_document_summary(data["content"])
#         data["document_summary"] = doc_summary
#         if df.empty:
#             print("No table data found.")
#         else:
#             chart_type = gemini_recommend_chart_type(df)
#             save_and_run_plot_code(chart_type, "plot_code.py")
#
#     else:
#         print("No table data found.")
#
#
#     # Generate the PPT
#     print("-------------------------------------------------------------------------------------------------------------")
#     print("\nGenerating a PowerPoint Presentation")
#     generate_pptx_from_gemini(data, slides_title="My Gemini Presentation")
#     print("-------------------------------------------------------------------------------------------------------------")
#     print("\nGenerating a Word Documentation")
#     generate_word_documentation(data)
#     print("-------------------------------------------------------------------------------------------------------------")
#     print("Presentation is saved under the name output.pptx and the word document is saved under the name output_document.docs")
#     print('If the presentation is not proper please run the code again ')

import json

import pandas as pd
from file_processing import validate_and_convert
from chart_functions import gemini_recommend_chart_type, save_and_run_plot_code
from ppt_generation import generate_pptx_from_gemini
from word_documentation import generate_word_documentation
from gemini_config import model


# --------------------------------------------------------------------
# 6. MAIN FLOW
# --------------------------------------------------------------------
def get_document_summary(text):
    """
    (Optional) A helper to call Gemini for a summary of text from the document.
    This can be appended into the final data that we pass to `generate_pptx_from_gemini`.
    """
    prompt = f"""
    Please provide a concise summary of the following text:

    {text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error calling Gemini API for summary: {str(e)}"


if __name__ == "__main__":
    print("---------------------------------------------------------------------")
    print("Welcome to the document summarizer and report generator!")
    print("---------------------------------------------------------------------")
    print("NOTE")
    print("Before proceeding, please ensure you have added your Gemini API key in the 'gemini_config.py' file.")
    print("---------------------------------------------------------------------")
    print("This project will generate a proper summary of the provided data and create a PowerPoint Presentation "
          "and a Word Documentation. Graphs will be created if there is any tabular data in the provided files, "
          "and those will be attached to the presentation and the documentation.")
    print("---------------------------------------------------------------------")

    print("Please enter either a JSON file, a PDF, or a CSV file for processing.")

    file_path = input("Enter the file path: ")
    data = validate_and_convert(file_path)

    if "error" in data:
        print(f"Error processing file: {data['error']}")
        exit()

    doc_summary = ""
    if data.get("type") == "text":
        # If it's just text, we might want to do a summary
        doc_summary = get_document_summary(data["content"])
        data["document_summary"] = doc_summary

    # If the data is a table, generate a chart if possible
    if data.get("type") == "json":
        # If JSON is a dictionary, attempt to visualize key-value pairs
        doc_summary = get_document_summary(json.dumps(data["content"], indent=4))
        data["document_summary"] = doc_summary

        # Example: Handle dictionary structures for graphing
        df = pd.DataFrame.from_dict(data["content"], orient="index").reset_index()
        df.columns = ["Key", "Value"]  # Customize based on JSON structure

        # Generate charts if possible
        chart_type = gemini_recommend_chart_type(df)
        save_and_run_plot_code(chart_type, "plot_code.py")

    elif data.get("type") == "table":
        # Existing table handling remains unchanged
        df = pd.DataFrame(data["content"])
        doc_summary = get_document_summary(data["content"])
        data["document_summary"] = doc_summary
        if df.empty:
            print("No table data found.")
        else:
            chart_type = gemini_recommend_chart_type(df)
            save_and_run_plot_code(chart_type, "plot_code.py")

    else:
        print("No table data found.")

    # Generate the PPT
    print(
        "-------------------------------------------------------------------------------------------------------------")
    print("\nGenerating a PowerPoint Presentation...")
    generate_pptx_from_gemini(data, slides_title="My Gemini Presentation")
    print(
        "-------------------------------------------------------------------------------------------------------------")

    print("\nGenerating a Word Documentation...")
    generate_word_documentation(data)
    print(
        "-------------------------------------------------------------------------------------------------------------")

    print(
        "Presentation has been saved as 'output.pptx' and the Word document has been saved as 'output_document.docx'.")
    print("If the presentation is not formatted correctly, please run the code again.")
    print(
        "-------------------------------------------------------------------------------------------------------------")
