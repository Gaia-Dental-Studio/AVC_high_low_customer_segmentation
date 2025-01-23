import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns


def app():
    # Title and description for the app
    st.title("RFM Analysis")
    st.write("This is a web application that helps businesses to segment their customers based on their purchase behavior. "
            "The app uses the RFM model to segment customers into different categories based on their recency, frequency, "
            "and monetary value.")

    # Load the data
    df = pd.read_csv("patient_transaction.csv")

    # Convert date to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    col1, col2 = st.columns(2)

    with col1:
        beginning_date = st.date_input("Select the beginning date", min_value=dt.datetime(2018, 1, 1), max_value=dt.datetime(2023, 12, 31), value=dt.datetime(2018, 1, 1))
        beginning_date = dt.datetime.combine(beginning_date, dt.datetime.min.time())
    with col2:
        reference_date = st.date_input("Select the reference date", min_value=dt.datetime(2018, 1, 1), max_value=dt.datetime(2023, 12, 31))
        reference_date = dt.datetime.combine(reference_date, dt.datetime.min.time())
        
    df = df[df['Date'] >= beginning_date]

    # Calculate RFM metrics
    rfm = df.groupby('Patient ID').agg({
        'Date': lambda x: (reference_date - x.max()).days,  # Recency
        'Patient ID': 'count',                              # Frequency
        'Price': 'sum'                                      # Monetary
    }).rename(columns={'Date': 'Recency', 'Patient ID': 'Frequency', 'Price': 'Monetary'})

    # Function to attempt quantile binning with fallback
    def flexible_binning(column, max_bins, labels):
        num_bins = max_bins
        while num_bins > 1:
            try:
                # Attempt to use pd.qcut with the current number of bins
                return pd.qcut(column, num_bins, labels=labels[:num_bins], duplicates='drop')
            except ValueError:
                # Reduce the number of bins if there's a ValueError
                num_bins -= 1
        # If it fails down to 1 bin, just assign the single label to all rows
        return pd.Series([labels[0]] * len(column), index=column.index)

    # Apply flexible binning for R, F, and M scores
    rfm['R_Score'] = flexible_binning(rfm['Recency'], 4, [4, 3, 2, 1])
    rfm['F_Score'] = flexible_binning(rfm['Frequency'], 4, [1, 2, 3, 4])
    rfm['M_Score'] = flexible_binning(rfm['Monetary'], 4, [1, 2, 3, 4])

    # RFM Segment and Score
    rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

    # Split the RFM_Segment into R, F, and M scores for pivot purposes
    rfm[['R_Score', 'F_Score', 'M_Score']] = rfm['RFM_Segment'].apply(lambda x: pd.Series(list(x)))

    st.dataframe(rfm)

    # Visualization objects

    # 1. RFM Segment Heatmap
    segment_counts = rfm.groupby(['R_Score', 'M_Score']).size().reset_index(name='Count')
    fig_1, ax1 = plt.subplots(figsize=(10, 8))
    pivot_data = segment_counts.pivot(index="R_Score", columns="M_Score", values="Count")
    sns.heatmap(pivot_data, annot=True, fmt="d", ax=ax1)
    ax1.set_title("RFM Segment Distribution Heatmap")

    st.markdown("### RFM Segment Distribution Heatmap")
    st.write("This heatmap shows the distribution of patients across different RFM segments," 
            "based on Recency and Monetary scores. The Recency score (rows) represents how recently patients have visited,"
            "and the Monetary score (columns) indicates their total spending.")

    # Display the heatmap in Streamlit
    st.pyplot(fig_1)


    # 2. Recency-Frequency Scatter Plot
    fig_2, ax2 = plt.subplots(figsize=(7, 7))
    sns.scatterplot(data=rfm, x='Recency', y='Frequency', size='Monetary', hue='RFM_Score', palette="viridis", sizes=(20, 200), ax=ax2)
    ax2.set_title("Recency-Frequency Scatter Plot")
    ax2.set_xlabel("Recency (days)")
    ax2.set_ylabel("Frequency (number of transactions)")
    ax2.legend(title='RFM Score')

    st.markdown("### Recency-Frequency Scatter Plot")

    st.write("This scatter plot visualizes the relationship between Recency and Frequency for each patient."
            "The size of each point represents the patient’s Monetary score, while the color indicates the overall RFM Score.")

    # Display the scatter plot in Streamlit
    st.pyplot(fig_2)

    # 3. RFM Segment Count Bar Plot
    fig_3, ax3 = plt.subplots(figsize=(12, 6))
    sns.countplot(data=rfm, x='RFM_Score', palette='coolwarm', ax=ax3)
    ax3.set_title("Patient Distribution by RFM Score")
    ax3.set_xlabel("RFM Score")
    ax3.set_ylabel("Number of Patients")


    st.markdown("### Patient Distribution by RFM Score")

    st.write("This bar plot shows the distribution of patients across different overall RFM Scores," 
            "allowing you to understand the variety and number of patients in each score category.")
    # Display the bar plot in Streamlit
    st.pyplot(fig_3)


    st.markdown("### Filter by Customer Segment")


    col1, col2 = st.columns(2)

    with col1:
        st.metric("Best Customers", len(rfm[rfm['RFM_Segment']=='444']), help="These are your most valuable customers who have visited recently, make frequent purchases, and spend the most. Represented by Score 4 in all three categories.")
        st.metric("Loyal Customers", len(rfm[rfm['F_Score']=='4']), help="These customers make frequent purchases and are loyal to your business. Represented by Score 4 in Frequency.")
        st.metric("Big Spenders", len(rfm[rfm['M_Score']=='4']), help="These customers spend the most on your products or services. Represented by Score 4 in Monetary.")
        
    with col2:
        st.metric("Almost Lost", len(rfm[rfm['RFM_Segment']=='244']), help="These customers have visited recently and make frequent purchases but have not spent much. Represented by Score 2 in Monetary.")
        st.metric("Lost Customers", len(rfm[rfm['RFM_Segment']=='144']), help="These customers have not visited recently, make few purchases, and have not spent much. Represented by Score 1 in Recency and Monetary.")
        st.metric("Lost Cheap Customers", len(rfm[rfm['RFM_Segment']=='111']), help="These customers have not visited recently, make few purchases, and have not spent much. Represented by Score 1 in all three categories.")
        
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Best Customers", "Loyal Customers", "Big Spenders", "Almost Lost", "Lost Customers", "Lost Cheap Customers"])

    with tab1:
        st.dataframe(rfm[rfm['RFM_Segment']=='444'])
    with tab2:
        st.dataframe(rfm[rfm['F_Score']=='4'])
    with tab3:
        st.dataframe(rfm[rfm['M_Score']=='4'])
    with tab4:
        st.dataframe(rfm[rfm['RFM_Segment']=='244'])
    with tab5:
        st.dataframe(rfm[rfm['RFM_Segment']=='144'])
    with tab6:
        st.dataframe(rfm[rfm['RFM_Segment']=='111'])
        