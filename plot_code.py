import matplotlib.pyplot as plt
import pandas as pd

def create_plots(data):
    df = pd.DataFrame(data)
    plots = []

    plt.figure(figsize=(10, 6))
    plt.plot(df['Month'], df['Temperature (°C)'])
    plt.xlabel('Month')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature vs Month')
    plt.savefig('temperature.png')
    plots.append('temperature.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(df['Month'], df['Rainfall (mm)'])
    plt.xlabel('Month')
    plt.ylabel('Rainfall (mm)')
    plt.title('Rainfall vs Month')
    plt.savefig('rainfall.png')
    plots.append('rainfall.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(df['Month'], df['Sales (Units)'])
    plt.xlabel('Month')
    plt.ylabel('Sales (Units)')
    plt.title('Sales vs Month')
    plt.savefig('sales.png')
    plots.append('sales.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(df['Month'], df['Advertising Budget ($)'])
    plt.xlabel('Month')
    plt.ylabel('Advertising Budget ($)')
    plt.title('Advertising Budget vs Month')
    plt.savefig('advertising.png')
    plots.append('advertising.png')
    plt.close()

    return plots


def main():
    data = [{'Month': 'January', 'Temperature (°C)': 5, 'Rainfall (mm)': 78, 'Sales (Units)': 120, 'Advertising Budget ($)': 500},
            {'Month': 'February', 'Temperature (°C)': 7, 'Rainfall (mm)': 65, 'Sales (Units)': 140, 'Advertising Budget ($)': 600},
            {'Month': 'March', 'Temperature (°C)': 10, 'Rainfall (mm)': 55, 'Sales (Units)': 200, 'Advertising Budget ($)': 700}]
    return create_plots(data)
