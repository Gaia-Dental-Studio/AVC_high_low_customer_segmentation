import streamlit as st
import pandas as pd
from viz_analysis import VizAnalysis
import matplotlib.pyplot as plt

# Cache the data loading function
@st.cache_data
def load_data():
    return pd.read_csv('historical_data.csv')

# Cache the figure generation function
@st.cache_resource
def generate_figures(_viz, label=False):
    fig1 = _viz.plot_histogram_treat_freq(label)
    fig2 = _viz.plot_histogram_average_spending(label)
    fig3 = _viz.plot_scatter(label)
    fig4 = _viz.plot_swarm(label)
    fig5 = _viz.plot_histogram_grand_total(label)
    return fig1, fig2, fig3, fig4, fig5

def app():
    # Load your data using the cached function
    historical_data = load_data()

    # Initialize VizAnalysis class
    viz = VizAnalysis(historical_data)

    # Setting page title
    st.title("Treatment Data Visualization")

    select_mode = st.selectbox("Select Mode", ["By Category", "By Label (High & Low)"])

    # Cache and load the generated figures
    if select_mode == "By Category":
        fig1, fig2, fig3, fig4, fig5 = generate_figures(viz, label=False)
    else:
        fig1, fig2, fig3, fig4, fig5 = generate_figures(viz, label=True)

    # Display figures using Streamlit layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Histogram of Treatment Frequency")
        st.pyplot(fig1)
        
    with col2:
        st.markdown("##### Histogram of Average Spending")
        st.pyplot(fig2)

    st.header("Hisogram of Grand Total")
    st.pyplot(fig5)

    st.header("Scatter Plot of Treatment Frequency vs. Average Spending")
    st.pyplot(fig3)

    st.header("Swarm Plot of Grand Total by Category")
    st.pyplot(fig4)

    st.divider()

    st.header("Data Table")
    st.write(historical_data)
