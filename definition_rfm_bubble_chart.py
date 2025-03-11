import streamlit as st


def app():

    # Introduction
    st.markdown("""
    The **Customer Segmentation Bubble Chart** provides a **high-level summary** of the patient base using:  

    - **X-axis**: **Monetary Value (AUD)** → The **average spending** per segment.  
    - **Y-axis**: **Frequency (Number of Visits)** → The **average number of visits** per segment.  
    - **Bubble Size**: **Customer Count in Segment** → The **larger the bubble, the more patients in that segment**.  

    This visualization builds on the **Customer Segmentation Treemap**, categorizing patients based on **RFM scores** and helping **identify engagement and revenue patterns** in the clinic.
    """)

    # Explanation of the axes
    st.subheader("How to Read the Bubble Chart?")
    st.markdown("""
    - **X-axis (Monetary Value in AUD)**  
    - Represents the **average spending** of customers within a segment.  
    - **Higher values (right side)** indicate high-spending patients.  
    - **Lower values (left side)** indicate low-spending patients.  

    - **Y-axis (Frequency of Visits)**  
    - Represents the **average number of visits** for a segment.  
    - **Higher values (top)** indicate frequent visitors.  
    - **Lower values (bottom)** indicate infrequent visitors.  

    - **Bubble Size (Customer Count in Segment)**  
    - **Larger bubbles** represent a **higher number of patients** in a segment.  
    - **Smaller bubbles** represent fewer patients.  
    - A **large bubble on the top-right** suggests a strong, loyal patient base.  
    - A **large bubble on the bottom-left** suggests a significant number of low-value, disengaged patients.  
    """)

    # Key insights
    st.subheader("Key Insights from the Chart")
    st.markdown("""
    ### **1. Best Customers (Top Right, Large Bubble)**  
    - **High monetary value, high visit frequency, and significant count.**  
    - These patients contribute the most revenue and visit regularly.  
    - **Retention efforts (loyalty programs, VIP benefits) should be prioritized for this group.**  

    ### **2. Lost Cheap Customers (Bottom Left, Small Bubble)**  
    - **Low monetary value, low frequency, and minimal engagement.**  
    - Patients who rarely visit and spend very little.  
    - **Retention efforts for this group may not be cost-effective.**  

    ### **3. Moderate Customers (Middle Left, Large Bubble)**  
    - **Moderate visit frequency but lower spending.**  
    - These patients could be **encouraged to spend more through promotional offers.**  
    - **Membership plans or personalized discounts** may improve their engagement.  

    ### **4. Valuable Customers (Upper Mid-Right, Mid-Size Bubble)**  
    - **Strong visit frequency and spending behavior.**  
    - They are **not as elite as Best Customers but are worth retaining.**  
    - **Targeted engagement (exclusive benefits, seasonal check-ups) can further strengthen loyalty.**  

    ### **5. Lost Customers (Lower Right, Small Bubble)**  
    - **Once highly engaged but now inactive (high monetary and frequency, but haven’t returned).**  
    - **These customers need reactivation campaigns** (reminders, promotions, or outreach).  

    ### **6. Almost Lost Customers (Upper Mid-Left, Small Bubble)**  
    - **Still have high frequency and spending, but showing signs of disengagement.**  
    - **Early intervention strategies** (follow-up calls, appointment reminders) can help retain them.  
    """)

    # How to use the chart insights
    st.subheader("How to Use This Chart for Decision Making?")
    st.markdown("""
    - **Prioritize Retention for High-Value Customers**  
    - Best Customers and Valuable Customers **should be retained with incentives and VIP experiences**.  
    - Losing these customers would significantly impact revenue.  

    - **Develop Growth Strategies for Moderate Customers**  
    - These patients **could be nurtured into high-value patients** with proper engagement strategies.  
    - Offering **preventive care plans, bundled treatments, or exclusive discounts** can increase visit frequency and spending.  

    - **Monitor At-Risk Segments**  
    - Lost Customers and Almost Lost Customers **require early intervention before they fully disengage**.  
    - Sending targeted marketing campaigns **can bring them back before they become Lost Cheap Customers.**  

    - **Avoid Over-Investing in Low-Value Customers**  
    - Lost Cheap Customers and Less Valuable Customers **may not be worth aggressive retention efforts**.  
    - Instead, focusing on **higher-potential segments ensures better ROI.**  
    """)

    st.success("By leveraging the **Customer Segmentation Bubble Chart**, clinics can **optimize their retention strategies**, **increase revenue from mid-tier patients**, and **ensure long-term sustainability by retaining high-value customers.** 🚀")
