import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from gemini_config import model

# --------------------------------------------------------------------
# 2. CHART FUNCTIONS
# --------------------------------------------------------------------

def gemini_recommend_chart_type(table_df, purpose="visualize data"):
    """
    Calls Gemini to recommend a chart type for the given table.
    """
    columns_info = ", ".join([f"'{col}'" for col in table_df.columns])
    sample_records = table_df.head(3).to_dict(orient="records")

    prompt = f"""
I have a table with columns: {columns_info}.
Sample rows: {sample_records}.
I want to {purpose}. 
I want to visualize data. Plot the code using python and give me only the chart. Dont plot it all in one chart using subplots
Save each plot seperately. I want to get a list of all the plot names that are being saved in an array.
Give me everything under two function only. First function which has all the code for plotting data. 
I dont want to pass any data to second function. I should have hardcoded data that i am plotting in the second function. 
The second function will also call the first function and return whatever the first function is returning. The name of the second function should always be main().
I dont any if __name__ == "__main__":. Just two functions in python code. I will be exporting one of the functions in another file and executing it
So i dont want any execution code here. Just two functions. 
And only give me the code. I dont want any text describing anything. Only the code. The main function of this could should be create_plot
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"

def plot_data_automatically(table_df, chart_type_suggestion, output_name="chart.png"):
    """
    Generates and saves a chart based on the table data and chart type suggestion.
    """
    numeric_cols = table_df.select_dtypes(include=["int", "float"]).columns
    non_numeric_cols = table_df.select_dtypes(exclude=["int", "float"]).columns
    suggestion_lower = chart_type_suggestion.lower()

    plt.figure()
    if suggestion_lower in ["line", "scatter"] and len(numeric_cols) >= 2:
        if suggestion_lower == "line":
            plt.plot(table_df[numeric_cols[0]], table_df[numeric_cols[1]], marker="o")
        else:
            plt.scatter(table_df[numeric_cols[0]], table_df[numeric_cols[1]], c="blue")
        plt.title(f"{chart_type_suggestion.capitalize()} Chart")

    elif suggestion_lower in ["hist", "distribution"] and len(numeric_cols) >= 1:
        sns.histplot(table_df[numeric_cols[0]])
        plt.title(f"{chart_type_suggestion.capitalize()} Plot")

    elif suggestion_lower in ["bar", "column"] and len(numeric_cols) >= 1 and len(non_numeric_cols) >= 1:
        plt.bar(table_df[non_numeric_cols[0]], table_df[numeric_cols[0]], color="orange")
        plt.title(f"{chart_type_suggestion.capitalize()} Chart")

    elif suggestion_lower in ["bar", "column"] and len(non_numeric_cols) >= 1:
        sns.countplot(x=table_df[non_numeric_cols[0]])
        plt.title(f"{chart_type_suggestion.capitalize()} Chart")

    else:
        print(f"Unsupported or ambiguous chart type: {chart_type_suggestion}")
        plt.close()
        return

    plt.tight_layout()
    plt.savefig(output_name)
    plt.close()

# --------------------------------------------------------------------
# 3. FUNCTION TO SAVE AND RUN CODE
# --------------------------------------------------------------------
def save_and_run_plot_code(text, output_file_name="plot_code.py"):
    """
    Saves the code for generating a plot based on Gemini's suggestion to a file and runs it.
    """
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)

    # print(f"\n{match}\n", )
    # Save the code to a file
    with open(output_file_name, "w") as file:
        if match:
            file.write(match.group(1))
        else:
            return None


    # print(f"Code saved to {output_file_name}. Run it locally to generate the plot.")
