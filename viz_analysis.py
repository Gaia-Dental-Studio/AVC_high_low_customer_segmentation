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

# # Sample Usage (if running the script outside Streamlit)
# if __name__ == "__main__":
#     historical_data = pd.read_csv('historical_data.csv')
#     viz = VizAnalysis(historical_data)
#     fig1 = viz.plot_histogram_treat_freq()
#     fig2 = viz.plot_histogram_average_spending()
#     fig3 = viz.plot_scatter()
#     fig4 = viz.plot_swarm()
#     fig5 = viz.plot_histogram_grand_total()


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class VizAnalysis2:
    def __init__(self, data, pricing_basis='Australia'):
        self.data = data
        self.pricing_basis = pricing_basis
        self.currency_symbol = '$' if pricing_basis == 'Australia' else 'Rp.'

    def plot_histogram_treat_freq(self, label=False):
        if label is False:
            fig = px.histogram(self.data, x='Treatment Frequency', nbins=10)
        else:
            fig = px.histogram(self.data, x='Treatment Frequency', color='Label', barmode="stack", nbins=10)
        
        fig.update_xaxes(tickvals=list(range(1, 11)))
        fig.update_layout(
            xaxis_title="Treatment Frequency",
            yaxis_title="Count",
            bargap=0.1,
            height=600,
            width=700
        )
        return fig

    def plot_histogram_average_spending(self, label=False):
        if label is False:
            fig = px.histogram(self.data, x='Average Spending', nbins=20)
        else:
            fig = px.histogram(self.data, x='Average Spending', color='Label', barmode="stack", nbins=20)
        
        # fig.update_xaxes(
        #     tickvals=list(range(0, 6000001, 1000000)),
        #     ticktext=[f'{self.currency_symbol}{i/1000000:.0f}M' for i in range(0, 6000001, 1000000)]
        # )
        fig.update_layout(
            xaxis_title=f"Average Spending ({self.currency_symbol})",
            yaxis_title="Count",
            bargap=0.1,
            height=600,
            width=700
        )
        return fig

    def plot_histogram_grand_total(self, label=False):
        if label is False:
            fig = px.histogram(self.data, x='Grand Total', nbins=20)
        else:
            fig = px.histogram(self.data, x='Grand Total', color='Label', barmode="stack", nbins=20)
        
        # fig.update_xaxes(
        #     tickvals=list(range(0, 22000001, 1000000)),
        #     ticktext=[f'{self.currency_symbol}{i/1000000:.0f}M' for i in range(0, 22000001, 1000000)],
        #     tickangle=45
        # )
        fig.update_layout(
            xaxis_title=f"Grand Total ({self.currency_symbol})",
            yaxis_title="Count",
            bargap=0.1,
            height=600,
            width=1000
        )
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



    def plot_swarm(self, x):
        # Determine the number of unique values in x
        unique_values_count = self.data[x].nunique()
        
        # Define a bank of colors with at least 10 RGB values
        color_discrete_sequence_bank = [
            'rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
            'rgb(148, 103, 189)', 'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
            'rgb(188, 189, 34)', 'rgb(23, 190, 207)'
        ]
        
        # Adjust the color_discrete_sequence to match the number of unique values
        color_discrete_sequence = color_discrete_sequence_bank[:unique_values_count]

        # Create the plot
        fig = px.strip(
            self.data, 
            x=x, 
            y='Grand Total', 
            color=x,
            color_discrete_sequence=color_discrete_sequence,
            stripmode='overlay'
        )

        fig.update_traces(marker=dict(size=8, opacity=0.7))

        fig.update_layout(
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=f"Grand Total ({self.currency_symbol})",
            height=600,
            width=1000
        )
        
        return fig

    


    def histogram(self, data, column, color=None):
        
        # Create the histogram with or without color argument
        fig = px.histogram(
            data, 
            x=column, 
            color=color,  # Optional color argument
            nbins=20, 
            title=f'Histogram of {column}',
            labels={column: column.replace('_', ' ').title()},
            template='plotly_white'
        )
        
        # Update layout to stack if color is provided
        if color:
            fig.update_layout(barmode='stack')
            
        fig.update_layout(
            xaxis_title=column.replace('_', ' ').title(),
            yaxis_title='Count',
            bargap=0.1,
            height=600,
            width=800,
            title_x=0.5
        )
        
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        
        return fig

    


    
    # Function to calculate coefficient of variation and count customers in Q1 for high variation categories
    def assess_standard_deviation(self, df):
        result = []
        
        # Group by Category
        for category, group in df.groupby("Category"):
            # Calculate mean and std for Grand Total
            mean_grand_total = group["Grand Total"].mean()
            std_grand_total = group["Grand Total"].std()
            
            # Calculate Coefficient of Variation (CV)
            cv = std_grand_total / mean_grand_total
            
            # Check if high variation (CV > 0.2)
            high_variation = cv > 0.2
            
            # If high variation, calculate the number of patients in the first quartile
            q1 = group["Grand Total"].quantile(0.25)
            q1_customers = group[group["Grand Total"] <= q1].shape[0]
            
            # Append results to list
            result.append({
                "Category": category,
                "Coefficient of Variation": cv,
                "High Variation": high_variation,
                "Q1 Customer Count": q1_customers if high_variation else 0
            })
        
        # Convert results to DataFrame
        result_df = pd.DataFrame(result)
        
        return result_df
    
    def generate_insights(self, df):
        insights = []
        
        # Group by Category and process each category
        for category, row in df.iterrows():
            if row["High Variation"]:
                # Generate insight string for categories with high variation
                insight = (
                    f"It is found that Grand Total Spending variation in Category {row['Category']} is high. "
                    f"We need to improve the spending of about {row['Q1 Customer Count']} patients as they have significantly "
                    f"less spending compared to other patients in Category {row['Category']}. "
                    "Strategies such as treatment discounts could be offered to increase their spending habits."
                )
                insights.append(insight)
        
        return insights
    
    


    
    

# Sample Usage (if running the script outside Streamlit)
# if __name__ == "__main__":
#     historical_data = pd.read_csv('historical_data.csv')
#     viz = VizAnalysis(historical_data)
#     fig1 = viz.plot_histogram_treat_freq()
#     fig2 = viz.plot_histogram_average_spending()
#     fig3 = viz.plot_scatter()
#     fig4 = viz.plot_swarm()
#     fig5 = viz.plot_histogram_grand_total()
