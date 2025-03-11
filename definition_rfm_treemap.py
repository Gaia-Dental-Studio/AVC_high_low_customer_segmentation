import streamlit as st


def app():

    # Introduction
    st.markdown("""
    The **Customer Segmentation Treemap** visually represents your patient base based on their **RFM (Recency, Frequency, and Monetary) scores**, grouping them into **three key customer categories**:

    1. **Customers to Concern** – Low-value, inactive patients who may not be worth significant retention efforts.  
    2. **Customers to Retain** – Your most valuable and engaged patients who should be prioritized.  
    3. **Customers to Improve** – Patients with potential for growth and engagement.  

    This segmentation **helps prioritize efforts** by highlighting which patients are worth focusing on, which require improvement, and which are unlikely to contribute significantly to your clinic's success.
    """)

    # Customers to Concern
    st.subheader("1. Customers to Concern (Low-Value or Inactive Customers)")
    st.markdown("""
    These patients have **low engagement, low spending, and infrequent visits**.  
    Since they are unlikely to generate high value, **focusing too much on them may not be efficient**.

    #### **Subsegments:**
    - **Less Valuable Customers**  
    - Patients with **RFM scores lower than 3 for Recency, Frequency, and Monetary**.  
    - They may visit occasionally but don’t contribute significantly.

    - **Lost Customers**  
    - Patients with **Recency = 1, Frequency = 4, and Monetary = 4**.  
    - **They were once valuable but haven’t returned in a long time.**  
    - A large number of Lost Customers **suggests a problem with patient retention.**  

    - **Lost Cheap Customers**  
    - Patients with the **lowest RFM scores (1,1,1)**.  
    - They are **low-frequency, low-spending, and inactive**—essentially **not worth re-engagement efforts.**  
    """)

    # Customers to Retain
    st.subheader("2. Customers to Retain (High-Value and Loyal Patients)")
    st.markdown("""
    These patients are **your best customers**—they are **loyal, engaged, and high spenders**. **Your primary goal should be to retain them.**

    #### **Subsegments:**
    - **Best Customers**  
    - Patients with **RFM scores of 4,4,4**—the highest possible score.  
    - They are your **most valuable, most engaged** patients.  
    - **Retention strategies should focus on VIP benefits and loyalty rewards.**  

    - **Almost Lost Customers**  
    - Patients with **Recency = 2, Frequency = 4, Monetary = 4**.  
    - They are still high-value but **show signs of disengagement.**  
    - **They require proactive re-engagement** (reminders, exclusive offers, or membership perks).  

    - **Valuable Customers**  
    - Patients with **RFM scores of 3 or higher for Recency, Frequency, and Monetary**.  
    - These are **high-potential patients worth nurturing**.  
    - **They are not quite at "Best Customer" status but still require strong retention efforts.**  
    """)

    # Customers to Improve
    st.subheader("3. Customers to Improve (Mid-Tier Patients with Growth Potential)")
    st.markdown("""
    These patients **have potential but need improvement** in their engagement, spending, or visit frequency.

    #### **Subsegment:**
    - **Moderate Customers**  
    - Patients with **a mix of high and low RFM scores** (e.g., **one metric is strong, but others are weak**).  
    - **They are good candidates for re-engagement strategies** (discounts, treatment plans, or follow-ups).  
    - If nurtured properly, they **can move into the "Customers to Retain" category.**  
    """)

    # How to use the treemap insights
    st.subheader("How to Use the Treemap for Patient Strategy?")
    st.markdown("""
    - **Assess Patient Distribution**  
    - **A high proportion of “Customers to Concern” indicates retention issues.**  
    - **A well-balanced distribution between "Customers to Retain" and "Customers to Improve" suggests sustainable patient engagement.**  

    - **Target Strategies Effectively**  
    - **Retain Best & Valuable Customers** with loyalty perks, priority scheduling, and special incentives.  
    - **Engage Moderate Customers** with targeted campaigns to improve frequency and spending.  
    - **Limit focus on Lost Cheap Customers**, as reactivation efforts may not be cost-effective.  

    - **Track Improvements Over Time**  
    - **Monitor shifts in segment sizes** to see if engagement strategies are successfully moving customers **from "Improve" to "Retain" instead of "Concern."**  
    """)

    st.success("By using this **Customer Segmentation Treemap**, you gain a **data-driven approach** to **patient engagement, retention, and clinic growth.** 🚀")
