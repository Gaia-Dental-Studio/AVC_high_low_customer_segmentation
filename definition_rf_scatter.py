import streamlit as st

def app():

    # Introduction
    st.markdown("""
    This scatter plot provides insights into patient behavior by analyzing **Recency**, **Frequency**, and **Monetary Value**—key components of **RFM (Recency, Frequency, Monetary) analysis**. Each point represents a patient, with characteristics influencing their engagement and revenue contribution to your clinic.
    """)

    # Explanation of Axes
    st.subheader("What Do the Axes Represent?")
    st.markdown("""
    - **X-axis (Recency in days)**: Measures how long it has been since a patient’s last visit.  
    - **Low recency (left side)**: Recently active patients.  
    - **High recency (right side)**: Patients who have not visited in a long time.  
    - **Y-axis (Frequency, number of transactions)**: Shows how often a patient has visited.  
    - **Higher values** indicate loyal patients who return frequently.  
    """)

    # Explanation of Data Point Characteristics
    st.subheader("Understanding the Data Point Characteristics")
    st.markdown("""
    - **Color (RFM Score)**: Patients are color-coded based on their RFM score:
    - **Darker colors (purple/blue)** indicate lower RFM scores, meaning less engaged patients.
    - **Lighter colors (green/yellow)** indicate higher RFM scores, representing valuable, engaged patients.
    - **Size (Monetary Value)**: The larger the bubble, the more revenue that patient has contributed.
    - **Smaller bubbles** represent low-spending patients.
    - **Larger bubbles** highlight high-value patients who contribute significantly to revenue.
    """)

    # Key insights
    st.subheader("Key Insights from the Scatter Plot")
    st.markdown("""
    1. **High-value, active patients**  
    - Found in the **top-left (low Recency, high Frequency, large bubbles)**.  
    - These are your **most engaged, high-spending patients** and should be nurtured with loyalty programs.  

    2. **At-risk high-value patients**  
    - Found in the **right side (high Recency, high Frequency, large bubbles)**.  
    - These patients used to visit frequently but have not returned for a long time.  
    - Consider sending reminders or exclusive offers to re-engage them.  

    3. **Low-engagement, low-value patients**  
    - Found in the **bottom-right (high Recency, low Frequency, small bubbles)**.  
    - These patients have low loyalty and low spending.  
    - Retention strategies might not be as effective here compared to high-value patients.  

    4. **Growing customers**  
    - Found in the **middle of the chart with mid-range Recency and Frequency**.  
    - These patients show potential for increased engagement and spending.  
    - Consider targeted promotions to move them towards becoming loyal, high-value patients.  
    """)

    # How to use the analysis
    st.subheader("How to Use This Analysis in Your Clinic?")
    st.markdown("""
    - **Maintain relationships with loyal, high-value patients** (top-left) through VIP perks.  
    - **Re-engage high-frequency but inactive patients** (right side) with targeted outreach.  
    - **Encourage mid-tier patients to increase visits and spending** using membership benefits or bundled services.  
    - **Assess which lower-tier patients may be worth retaining** or if resources are better allocated elsewhere.  
    """)

    st.success("By understanding patient engagement through **Recency, Frequency, and Monetary Value**, you can refine your clinic’s marketing, retention, and growth strategies effectively.")
