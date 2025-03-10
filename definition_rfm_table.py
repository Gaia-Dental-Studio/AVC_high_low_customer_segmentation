import streamlit as st

def app():

    # Introduction
    st.markdown("""
    This table provides a **detailed breakdown of each patient’s Recency, Frequency, and Monetary Value (RFM) scores**. The **RFM scoring system** helps categorize patients based on their engagement and spending patterns, enabling a more targeted approach to patient retention and marketing.
    """)

    # Explanation of columns
    st.subheader("What Each Column Represents")
    st.markdown("""
    - **Patient ID**: A unique identifier for each patient.  
    - **Recency (days since last visit)**: How recently a patient has visited. Lower values indicate more recent visits.  
    - **Frequency (number of visits)**: The total number of times the patient has visited. Higher values mean more frequent visits.  
    - **Monetary (total spend)**: The total amount a patient has spent at the clinic.  
    """)

    # Explanation of RFM Scores and Segments
    st.subheader("The RFM Scores and Segments")
    st.markdown("""
    - **R_Score (1-4)**: Categorizes patients based on **Recency**, with higher scores (4) indicating more recent visits.  
    - **F_Score (1-4)**: Categorizes patients based on **Frequency**, with higher scores (4) indicating frequent visits.  
    - **M_Score (1-4)**: Categorizes patients based on **Monetary Value**, with higher scores (4) indicating high spenders.  
    - **RFM_Segment**: A three-digit code combining R, F, and M scores to classify the patient. Example:  
    - **RFM segment "434"** → **R_Score = 4, F_Score = 3, M_Score = 4**.  
    - **RFM_Score**: The sum of the individual RFM scores. Higher values indicate more valuable patients.  
    """)

    # How RFM scores are determined
    st.subheader("How Are RFM Scores Determined?")
    st.markdown("""
    The **R, F, and M scores are assigned using quantile binning**, which splits the data into four ranked groups (1-4). The process works as follows:

    1. **Sorting Patients**: Each metric (Recency, Frequency, Monetary) is sorted in ascending or descending order:
    - **Recency**: More recent visits → Higher scores (4), Older visits → Lower scores (1).  
    - **Frequency & Monetary**: More visits/spending → Higher scores (4), Fewer visits/spending → Lower scores (1).  

    2. **Applying Quantile Binning**: The dataset is divided into **four equal-sized groups (quartiles)**.  
    - If equal-sized groups aren’t possible, the algorithm adjusts dynamically to ensure fair segmentation.

    3. **Fallback Mechanism**: If data distribution prevents equal binning (due to duplicates or limited variation), the number of bins is **automatically reduced** to the largest possible valid grouping.

    This flexible approach ensures **balanced RFM scoring across different patient distributions**.
    """)

    # How to use the insights
    st.subheader("How to Use This Analysis in Your Clinic?")
    st.markdown("""
    - **Identify and Reward High-Value Patients** (e.g., RFM Score 11 or 12)  
    - These patients visit frequently, spend a lot, and recently had an appointment.  
    - Offer them loyalty programs or exclusive discounts to maintain engagement.  

    - **Target Patients at Risk of Churning** (e.g., RFM Score 6 or below)  
    - These patients haven’t visited recently and may have lower spending or frequency.  
    - Use personalized reactivation campaigns (emails, discounts, or check-up reminders) to bring them back.  

    - **Optimize Marketing for Mid-Tier Patients** (e.g., RFM Score 8-10)  
    - These patients show potential but need encouragement to become high-value customers.  
    - Offering bundled treatments, promotional pricing, or membership benefits can help.  
    """)

    st.success("By leveraging **RFM-based segmentation**, you can create highly effective retention and engagement strategies, ensuring that **valuable patients stay loyal** while reactivating those at risk of churning.")
