import streamlit as st


def app():

    # Introduction
    st.markdown("""
    This histogram provides a visual representation of **patient distribution by their RFM Score**.  
    The **RFM Score** is calculated as the sum of the **Recency (R), Frequency (F), and Monetary (M) scores**, each ranging from **1 to 4**.  
    The final RFM Score typically falls between **3 (least engaged, low value) and 12 (most engaged, high value).**
    """)

    # Explanation of the histogram axes
    st.subheader("What Does This Histogram Show?")
    st.markdown("""
    - **X-axis (RFM Score)**: Represents the combined RFM score, ranging from **3 to 12**.  
    - **Y-axis (Number of Patients)**: Indicates how many patients belong to each RFM score category.  
    - Each bar represents the **number of patients in that RFM Score category**, helping to understand the distribution of patient engagement levels.  
    """)

    # Key insights
    st.subheader("Key Insights from the RFM Score Distribution")
    st.markdown("""
    ### **1. Higher RFM Scores (10-12) Indicate High-Value Patients**  
    - These patients visit frequently, spend a lot, and have visited recently.  
    - They are your most loyal and engaged customers.  
    - Consider implementing **VIP programs, exclusive discounts, or referral incentives** to retain them.  

    ### **2. Mid-Range RFM Scores (6-9) Represent Growth Opportunities**  
    - These patients have moderate engagement and spending.  
    - They might need **additional incentives** to transition into high-value segments.  
    - Strategies such as **personalized follow-ups, membership plans, or special promotions** can help convert them into loyal patients.  

    ### **3. Lower RFM Scores (3-5) Indicate At-Risk or Inactive Patients**  
    - These patients **haven't visited recently, don’t visit frequently, or don’t spend much**.  
    - They are **at risk of churning**, meaning they might never return unless re-engaged.  
    - Consider **re-engagement campaigns like email reminders, discount offers, or educational content** to encourage visits.  
    """)

    # How to use the insights
    st.subheader("How Can You Use This Information?")
    st.markdown("""
    - **Assess Patient Loyalty Trends**:  
    - If most patients fall into the **low to mid RFM range**, you may need to **focus on retention strategies** to increase engagement.  

    - **Optimize Marketing Efforts**:  
    - Target **high RFM patients** with loyalty programs and referral incentives.  
    - Encourage **mid-RFM patients** to increase their visits and spending through personalized promotions.  
    - Re-engage **low RFM patients** with automated reminders, discounts, or outreach efforts.  

    - **Monitor the Effectiveness of Retention Strategies**:  
    - Over time, the goal is to **shift more patients into higher RFM score categories** by improving engagement, visit frequency, and spending behavior.  
    """)

    st.success("By analyzing this **RFM Score Distribution**, you can make **data-driven decisions** to improve patient retention, engagement, and overall clinic revenue. 🚀")
