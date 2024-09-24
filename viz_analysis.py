import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class VizAnalysis:
    def __init__(self, data):
        self.data = data
    
    def plot_histogram_treat_freq(self, label=False):
        plt.figure(figsize=(10, 6))
        
        if label is False:
            sns.histplot(data=self.data, x='Treatment Frequency')
        else: 
            sns.histplot(data=self.data, x='Treatment Frequency', hue='Label', multiple="stack")
        plt.xticks(np.arange(1, 11, 1))
        plt.tight_layout()
        fig = plt.gcf()
        return fig
    
    def plot_histogram_average_spending(self, label=False):
        plt.figure(figsize=(10, 6))
        
        if label is False:
            sns.histplot(self.data['Average Spending'])
        else:
            sns.histplot(data=self.data, x='Average Spending', hue='Label', multiple="stack")
        # plt.xticks(np.arange(1, 11, 1))
        # edit xticks to show in million rupiah format interval of 1 million rupiah maximum 6 rupiah
        plt.xticks(np.arange(0, 6000001, 1000000), [f'Rp.{i/1000000:.0f}M' for i in np.arange(0, 6000001, 1000000)])
        plt.tight_layout()
        fig = plt.gcf()
        return fig
    
    def plot_histogram_grand_total(self, label=False):
        plt.figure(figsize=(10, 6))
        
        if label is False:
            sns.histplot(self.data['Grand Total'])
        else:
            sns.histplot(data=self.data, x='Grand Total', hue='Label', multiple="stack")
        # plt.xticks(np.arange(1, 11, 1))
        # edit xticks to show in million rupiah format interval of 1 million rupiah maximum 22 rupiah with label slightly rotated
        plt.xticks(np.arange(0, 22000001, 1000000), [f'Rp.{i/1000000:.0f}M' for i in np.arange(0, 22000001, 1000000)], rotation=45)
        
        plt.tight_layout()
        fig = plt.gcf()
        return fig


    def plot_scatter(self, label=False):
        plt.figure(figsize=(10, 6))
        
        if label is False:
            sns.scatterplot(data=self.data, x='Treatment Frequency', y='Average Spending', hue='Category', palette=['red', 'grey', 'green', 'yellow', 'purple'])
        else:
            sns.scatterplot(data=self.data, x='Treatment Frequency', y='Average Spending', hue='Label', palette=['red', 'green'])
        
        plt.tight_layout()
        fig = plt.gcf()
        return fig

    def plot_swarm(self, label=False):
        plt.figure(figsize=(10, 6))
        if label is False:
            sns.swarmplot(data=self.data, x='Category', y='Grand Total', hue='Category', palette=['red', 'grey', 'green', 'yellow', 'purple'])
        else:
            sns.swarmplot(data=self.data, x='Label', y='Grand Total', hue='Label', palette=['red', 'green'])
        
        plt.yticks(np.arange(0, 25000001, 5000000), [f'Rp.{i/1000000:.0f}M' for i in np.arange(0, 25000001, 5000000)])
        plt.tight_layout()
        fig = plt.gcf()
        return fig

# Sample Usage (if running the script outside Streamlit)
if __name__ == "__main__":
    historical_data = pd.read_csv('historical_data.csv')
    viz = VizAnalysis(historical_data)
    fig1 = viz.plot_histogram_treat_freq()
    fig2 = viz.plot_histogram_average_spending()
    fig3 = viz.plot_scatter()
    fig4 = viz.plot_swarm()
    fig5 = viz.plot_histogram_grand_total()
