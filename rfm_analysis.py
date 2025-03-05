import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


def app():
    # Title and description for the app
    st.title("RFM Analysis")
    st.write("This is a web application that helps businesses to segment their customers based on their purchase behavior. "
            "The app uses the RFM model to segment customers into different categories based on their recency, frequency, "
            "and monetary value.")

    # Load the data
    df = pd.read_csv("patient_transaction.csv")
    # df = pd.read_csv("haoey_data_processed.csv")
    
    ### Actual Transaction Data
    st.dataframe(df, hide_index=True)
    
    st.divider()

    st.markdown("### Date Filtering for RFM Analysis")

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

    df['Date_2'] = df['Date'].dt.date

    # Calculate RFM metrics
    rfm = df.groupby('Patient ID').agg({
        'Date': lambda x: (reference_date - x.max()).days,  # Recency
        'Date_2': lambda x: x.nunique(),                      # Frequency (count of unique dates)
        'Price': 'sum'                                      # Monetary
    }).rename(columns={'Date_2': 'Frequency', 'Price': 'Monetary'})

    # Rename Recency column separately as we used 'Date' twice
    rfm.rename(columns={rfm.columns[0]: 'Recency'}, inplace=True)
    
    # st.dataframe(rfm)
    # rfm.to_csv('sample_rfm.csv', index = False)

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
    
    def forced_binning(column, max_bins, labels):
        return pd.cut(column.rank(method="dense"), bins=max_bins, labels=labels, right=False)


    # Apply flexible binning for R, F, and M scores
    rfm['R_Score'] = flexible_binning(rfm['Recency'], 4, [4, 3, 2, 1])
    rfm['F_Score'] = flexible_binning(rfm['Frequency'], 4, [1, 2, 3, 4])
    rfm['M_Score'] = flexible_binning(rfm['Monetary'], 4, [1, 2, 3, 4])

    # RFM Segment and Score
    rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

    # Split the RFM_Segment into R, F, and M scores for pivot purposes
    rfm[['R_Score', 'F_Score', 'M_Score']] = rfm['RFM_Segment'].apply(lambda x: pd.Series(list(x)))

    st.write(len(rfm))
  

    st.markdown("#### RFM Calculation Result")

    st.dataframe(rfm, use_container_width=True)

    # Visualization objects
    
    col1, col2 = st.columns(2)

    with col1:

        # 1. RFM Segment Heatmap
        segment_counts = rfm.groupby(['R_Score', 'M_Score']).size().reset_index(name='Count')
        fig_1, ax1 = plt.subplots(figsize=(10, 8))

        # Convert numeric scores to formatted labels
        segment_counts['R_Label'] = 'R' + segment_counts['R_Score'].astype(str)
        segment_counts['M_Label'] = 'M' + segment_counts['M_Score'].astype(str)
        
        # rename column R_Label to R Score and M_Label to M Score
        segment_counts.rename(columns={'R_Label':'R Score', 'M_Label':'M Score'}, inplace=True)

        pivot_data = segment_counts.pivot(index="R Score", columns="M Score", values="Count")

        sns.heatmap(pivot_data, annot=True, fmt="d", ax=ax1)
        ax1.set_title("RFM Segment Distribution Heatmap")
        
        ax1.invert_yaxis()


        st.markdown("### RFM Segment Distribution Heatmap")
        st.write("This heatmap shows the distribution of patients across different RFM segments," 
                "based on Recency and Monetary scores. The Recency score (rows) represents how recently patients have visited,"
                "and the Monetary score (columns) indicates their total spending.")

        # Display the heatmap in Streamlit
        st.pyplot(fig_1)

    with col2:

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

    col3, col4 = st.columns(2)

    with col3:

        # 3. RFM Segment Count Bar Plot
        fig_3, ax3 = plt.subplots(figsize=(12, 6))
        sns.countplot(data=rfm, x='RFM_Score', 
                      color='royalblue',
                      ax=ax3)
        ax3.set_title("Patient Distribution by RFM Score")
        ax3.set_xlabel("RFM Score")
        ax3.set_ylabel("Number of Patients")


        st.markdown("### Patient Distribution by RFM Score")

        st.write("This bar plot shows the distribution of patients across different overall RFM Scores," 
                "allowing you to understand the variety and number of patients in each score category.")
        # Display the bar plot in Streamlit
        st.pyplot(fig_3)


        
        # # 3. RFM Segment Swarm Plot (Horizontal)
        # fig_4, ax4 = plt.subplots(figsize=(12, 6))

        # # Create a binned column for Monetary values
        # rfm['Monetary_Binned'] = pd.cut(rfm['Monetary'], bins=20, labels=False)

        # # Swarmplot with horizontal orientation
        # sns.swarmplot(data=rfm, y='Monetary_Binned', x='Monetary', 
        #             color='royalblue', ax=ax4, size=5, alpha=0.7)

        # ax4.set_title("Patient Distribution by Monetary Value (Swarm Plot)")
        # ax4.set_ylabel("Monetary Value (Binned)")
        # ax4.set_xlabel("Monetary Value")
        # ax4.set_yticks(range(20))  # Ensures bins are labeled correctly
        # ax4.tick_params(axis='y', rotation=0)

        # st.pyplot(fig_4)

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
        
    

    def assign_segment(row):
        """Assigns customer segment based on RFM_Segment and RFM scores."""
        if row['RFM_Segment'] == '444':
            return 'Best Customers'
        elif row['RFM_Segment'] == '244':
            return 'Almost Lost'
        elif row['RFM_Segment'] == '144':
            return 'Lost Customers'
        elif row['RFM_Segment'] == '111':
            return 'Lost Cheap Customers'
        elif (row['RFM_Segment'] != '444') and (
            int(row['R_Score']) >= 3 and int(row['F_Score']) >= 3 and int(row['M_Score']) >= 3):
            return 'Valuable Customers'
        elif (row['RFM_Segment'] != '111') and (
            int(row['R_Score']) <= 2 and int(row['F_Score']) <= 2 and int(row['M_Score']) <= 2):
            return 'Less Valuable Customers'
        else:
            return 'Moderate Customers'  # Default fallback for any unexpected cases

    def assign_segment_category(row):
        if row['Segment'] in ['Best Customers', 'Almost Lost', 'Valuable Customers']:
            return 'Customers to Retain'
        elif row['Segment'] in ['Lost Customers', 'Lost Cheap Customers', 'Less Valuable Customers']:
            return 'Customers to Concern'
        
        else:
            return 'Customers to Improve'

    # Apply function to create the new 'Segment' column
    rfm['Segment'] = rfm.apply(assign_segment, axis=1)
    rfm['Segment Category'] = rfm.apply(assign_segment_category, axis=1)

    
    
    # create treemap with sns and matplotlib for "Best Customers", "Almost Lost", "Lost Customers", "Lost Cheap Customers"
    
    # Best Customers
    best_customers = rfm[rfm['RFM_Segment']=='444']
    best_customers_count = len(best_customers)
    best_customers_count
    
    # Almost Lost
    almost_lost = rfm[rfm['RFM_Segment']=='244']
    almost_lost_count = len(almost_lost)
    almost_lost_count
    
    # Lost Customers
    lost_customers = rfm[rfm['RFM_Segment']=='144']
    lost_customers_count = len(lost_customers)
    lost_customers_count
    
    # Lost Cheap Customers
    lost_cheap_customers = rfm[rfm['RFM_Segment']=='111']
    lost_cheap_customers_count = len(lost_cheap_customers)
    lost_cheap_customers_count
    
    # Create Valuable Customers which have combination score of 3 or 4 except 444
    valuable_customers = rfm[(rfm['RFM_Segment'] != '444') & 
                             ((rfm['R_Score'].astype(int) >= 3) & 
                              (rfm['F_Score'].astype(int) >= 3) & 
                              (rfm['M_Score'].astype(int) >= 3))]
    
    valuable_customers_count = len(valuable_customers)
    valuable_customers_count
    

    
    # Create Less Valuable Customers which have combination score of 1 or 2 except 111
    less_valuable_customers = rfm[(rfm['RFM_Segment'] != '111') & 
                                  ((rfm['R_Score'].astype(int) <= 2) &
                                   (rfm['F_Score'].astype(int) <= 2) & 
                                   (rfm['M_Score'].astype(int) <= 2))]
    less_valuable_customers_count = len(less_valuable_customers)
    less_valuable_customers_count
    
    
    moderate_customers_count = len(rfm[rfm['Segment'] == 'Moderate Customers'])
    
    # # Others Customers
    # others_customers = rfm[(rfm['RFM_Segment'] != '444') & 
    #                        (rfm['RFM_Segment'] != '244') & 
    #                        (rfm['RFM_Segment'] != '144') & 
    #                        (rfm['RFM_Segment'] != '111') &
    #                        (rfm['RFM_Segment'].isin(valuable_customers['RFM_Segment']) == False) &
    #                        (rfm['RFM_Segment'].isin(less_valuable_customers['RFM_Segment']) == False)]
    # others_customers_count = len(others_customers)
    
    

    # Define segment names and their corresponding values
    labels = [
        "Segmented", "Others",  
        "Best Customers", "Almost Lost", "Lost Customers", "Lost Cheap Customers",
        "Valuable Customers", "Less Valuable Customers"
    ]

    # Define hierarchy structure
    parents = [
        "All Customers", "All Customers",  
        "Segmented", "Segmented", "Segmented", "Segmented",  
        "Others", "Others"
    ]

    # Define values (size of each segment)
    values = [
        0,  # "Segmented" total
        0,  # "Others" total
        best_customers_count, almost_lost_count, lost_customers_count, lost_cheap_customers_count,
        valuable_customers_count, less_valuable_customers_count
    ]

    # Explicit color mapping
    color_discrete_map = {
        "Segmented": "lightgrey",  # Parent
        "Others": "lightgrey",  # Parent
        "Best Customers": "lightblue",
        "Almost Lost": "lightblue",
        "Valuable Customers": "lightblue",
        "Less Valuable Customers": "pink",
        "Lost Customers": "pink",
        "Lost Cheap Customers": "pink"
    }

    # Create Treemap
    fig_4 = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=[color_discrete_map[label] for label in labels])  # Assign colors explicitly
    ))

    # Update layout
    fig_4.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        treemapcolorway=["lightblue", "pink", "lightgrey"]
    )


    # Define segment names and their corresponding values
    labels = [
        "Customers to Retain", "Customers to Improve", "Customers to Concern",  # New parent categories
        "Best Customers", "Almost Lost", "Valuable Customers",  # Light Blue
        "Moderate Customers",
        "Less Valuable Customers", "Lost Customers", "Lost Cheap Customers"  # Pink
    ]

    # Define hierarchy structure (assigning new parents)
    parents = [
        "All Customers", "All Customers", "All Customers",  # Parents of the two categories
        "Customers to Retain", "Customers to Retain", "Customers to Retain",  # Light Blue
        "Customers to Improve",
        "Customers to Concern", "Customers to Concern", "Customers to Concern"  # Pink
    ]

    # Define values (size of each segment)
    values = [
        0,  # "Customers to Retain" total (inferred)
        0,  # "Customers to Improve" total (inferred)
        0,  # "Customers to Concern" total (inferred)
        best_customers_count, almost_lost_count, valuable_customers_count,  # Light Blue
        moderate_customers_count,
        less_valuable_customers_count, lost_customers_count, lost_cheap_customers_count  # Pink
    ]

    # Calculate percentage values dynamically
    total_customers = sum(values[3:])  # Ignore parent nodes
    values_percentage = [
        "0%", "0%", "0%",  # Parents (ignored)
        f"{(best_customers_count / total_customers) * 100:.2f}%",
        f"{(almost_lost_count / total_customers) * 100:.2f}%",
        f"{(valuable_customers_count / total_customers) * 100:.2f}%",
        f"{(moderate_customers_count / total_customers) * 100:.2f}%",
        f"{(less_valuable_customers_count / total_customers) * 100:.2f}%",
        f"{(lost_customers_count / total_customers) * 100:.2f}%",
        f"{(lost_cheap_customers_count / total_customers) * 100:.2f}%"
    ]

    # Explicit color mapping
    color_discrete_map = {
        "Customers to Retain": "lightgrey",  # Parent color
        "Customers to Improve": "lightgrey",  # Parent color
        "Customers to Concern": "lightgrey",  # Parent color
        "Best Customers": "lightblue",
        "Almost Lost": "lightblue",
        "Valuable Customers": "lightblue",
        "Moderate Customers": "plum",
        "Less Valuable Customers": "pink",
        "Lost Customers": "pink",
        "Lost Cheap Customers": "pink"
    }

    # Create hover text format (only appears when hovering)
    custom_hover_text = [
        f"Segment: {label}<br>Value: {value}<br>Percentage: {percentage}"
        for label, value, percentage in zip(labels, values, values_percentage)
    ]

    # Create Treemap
    fig_5 = go.Figure(go.Treemap(
        labels=labels,  # Only segment names will be visible inside the blocks
        parents=parents,
        values=values,
        marker=dict(colors=[color_discrete_map[label] for label in labels]),  # Assign explicit colors
        hovertext=custom_hover_text,  # Detailed information appears on hover
        hoverinfo="text"  # Show hover text only when hovering
    ))

    # Update layout
    fig_5.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        treemapcolorway=["lightblue", "pink", "lightgrey"]
    )




    st.markdown("### Customer Segmentation Treemap")
    
    st.write("This treemap visualizes the segmentation of customers based on their RFM scores. "
            "The segments include 'Best Customers', 'Almost Lost', 'Lost Customers', 'Lost Cheap Customers', 'Valuable Customers', and 'Less Valuable Customers'. "
            "The 'Valuable Customers' and 'Less Valuable Customers' belong to 'Others' category and the rest belong to 'Segmented' category.")
    
    st.write("Valuable Customers are those who have a combination score of 3 or 4 in Recency, Frequency, or Monetary except 444 (Best Customers). ")
    st.write("Less Valuable Customers are those who have a combination score of 1 or 2 in Recency, Frequency, or Monetary except 111 (Lost Cheap Customers).")



    # st.plotly_chart(fig_4)
    

    st.plotly_chart(fig_5)
        
        
    rfm_by_segment = rfm.groupby('Segment').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'RFM_Score': 'mean',
        'Segment Category': 'first',
        'Segment': 'size'  # Count occurrences of each segment
    }).rename(columns={'Segment': 'Count'}).reset_index()
    
    # round into two decimal for all numeric column in rfm_by_segment
    rfm_by_segment = rfm_by_segment.round(0)
        
        

        
#     fig_6 = px.scatter(
#     rfm_by_segment, 
#     x="Monetary", 
#     y="Frequency",
#     size="Count",  # You can change this to another metric if needed
#     color=['rgb(173, 216, 230)', 'rgb(135, 206, 235)', 'rgb(176, 224, 230)',
#            'rgb(255, 182, 193)', 'rgb(255, 192, 203)','rgb(250, 160, 180)']
# ,  # 'Customers to Retain' and 'Customers to Concern'
#     hover_name="Segment",  # Shows 'Best Customers', 'Almost Lost', etc.
#     size_max=60,  # Controls maximum bubble size
#     # log_x=True,  # Optional: Log scale for better distribution
#     title="Customer Segmentation Bubble Chart"
# )
    
    
    fig_6 = px.scatter(
    rfm_by_segment, 
    x="Monetary", 
    y="Frequency",
    size="Count",
    color="Segment",  # Using 'Segment' to categorize colors
    hover_name="Segment",
    size_max=60,
    title="Customer Segmentation Bubble Chart",
    color_discrete_map={  # Assign custom colors
        'Almost Lost': 'rgb(176, 224, 230)', 
        'Best Customers': 'rgb(93, 164, 214)',
        'Less Valuable Customers': 'rgb(255, 192, 203)',
        'Lost Cheap Customers': 'rgb(240, 128, 160)',
        'Lost Customers': 'rgb(250, 160, 180)',
        'Moderate Customers': 'rgb(142, 69, 133)',
        'Valuable Customers': 'rgb(176, 224, 230)'
    }
)


    # update layout fig_6 to rename x axis label as Monetary (AUD) and y label as Frequency (Number of Visit)
    fig_6.update_layout(
        xaxis_title="Monetary (AUD)",
        yaxis_title="Frequency (Number of Visit)"
    )
    
    st.plotly_chart(fig_6)
    
    