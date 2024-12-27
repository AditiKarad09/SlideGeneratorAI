import matplotlib.pyplot as plt
import os

def create_plots(data):
    plots = []
    for category in data:
        fig, ax = plt.subplots()
        ax.bar(['Sales', 'Profit'], [category['Sales'], category['Profit']])
        ax.set_title(category['Category'])
        plot_name = f"{category['Category']}_plot.png"
        plots.append(plot_name)
        plt.savefig(plot_name)
        plt.close(fig)  #Close the figure to free up memory

    return plots


def main():
    data = [{'Category': 'Electronics', 'Sales': 10000, 'Profit': 2000}, {'Category': 'Furniture', 'Sales': 15000, 'Profit': 3000}, {'Category': 'Stationery', 'Sales': 5000, 'Profit': 1000}]
    return create_plots(data)
