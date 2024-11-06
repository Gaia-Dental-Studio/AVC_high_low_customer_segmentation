import streamlit as st
import pandas as pd
from viz_analysis import VizAnalysis2
import plotly.express as px



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
    viz = VizAnalysis2(historical_data)

    

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
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.markdown("##### Histogram of Average Spending")
        st.plotly_chart(fig2, use_container_width=True)

    st.header("Histogram of Grand Total")
    st.plotly_chart(fig5, use_container_width=True)

    st.header("Scatter Plot of Treatment Frequency vs. Average Spending")
    st.plotly_chart(fig3, use_container_width=True)

    st.header("Swarm Plot of Grand Total by Category")
    st.plotly_chart(fig4, use_container_width=True)


    st.divider()
    
    with st.container(border=True):
        pass


    with st.container(border=True):
    # Display insights in Streamlit
        st.markdown("### Insights from Category-Based Spending (Generative AI Analytics)")

        st.write("""
        ### Category 1
        - **Grand Total**: 12.5M
        - **Average Spending per visit**: 1.8M

        **Actionable Insight**: Patients in Category 1 are high-value clients. Focus on retaining them by offering loyalty programs or exclusive services. This segment could also benefit from personalized treatment plans or VIP services.
        """)

        st.write("""
        ### Category 2
        - **Grand Total**: 6.3M
        - **Average Spending per visit**: 1.83M

        **Actionable Insight**: Although the overall spending is lower, these patients spend a significant amount per visit. Encourage repeat visits with targeted promotions or referral incentives, aiming to boost the total spend over time.
        """)

        st.write("""
        ### Category 3
        - **Grand Total**: 3.9M
        - **Average Spending per visit**: 1.03M

        **Actionable Insight**: These patients may be mid-tier in terms of total spending, but the lower average spending suggests they may require more affordable treatment plans. Consider offering bundled treatments or discounts to drive more frequent visits.
        """)

        st.write("""
        ### Category 4
        - **Grand Total**: 2.3M
        - **Average Spending per visit**: 921K

        **Actionable Insight**: This group might be more price-sensitive. Introduce budget-friendly packages or financing options to make higher-value treatments more accessible.
        """)

        st.write("""
        ### Category 5
        - **Grand Total**: 597K
        - **Average Spending per visit**: 283K

        **Actionable Insight**: These patients are likely low-frequency, low-spending visitors. Consider strategies like upselling during visits or offering discounts on high-demand treatments to increase their spending.
        """)


    st.divider()
    
    with st.container(border=True):
        st.markdown("### Insights from Category-Based Spending (User Specified Analysis)")
    
        result_df = viz.assess_standard_deviation(historical_data)
        # st.dataframe(result_df, hide_index=True)
        
        insights = viz.generate_insights(result_df)
        
        for insight in insights:
            st.write(insight)
    
    st.divider()
    

    st.header("Data Table")
    st.write(historical_data)

