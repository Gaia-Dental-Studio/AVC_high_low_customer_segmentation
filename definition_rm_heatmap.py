import streamlit as st


def app():

    # Introduction
    st.markdown("""
    This heatmap visualizes the distribution of patients based on **Recency (R Score)** and **Monetary Value (M Score)**—two key dimensions of the **RFM (Recency, Frequency, Monetary) model** used in customer analysis.
    """)

    # Explanation of R and M Scores
    st.subheader("What Do the Scores Mean?")
    st.markdown("""
    - **Recency (R Score)**: Measures how recently a patient has visited your clinic.  
    - Patients with **R4** have visited most recently.  
    - Patients with **R1** have not visited in a long time.  
    - **Monetary Value (M Score)**: Represents the total spending of a patient.  
    - Patients with **M4** have spent the most.  
    - Patients with **M1** have spent the least.  
    """)

    # How to interpret the heatmap
    st.subheader("How to Interpret the Heatmap?")
    st.markdown("""
    - Each cell represents the **number of patients** in a specific R-M category.
    - **Dark-colored cells (lower values)** indicate fewer patients, whereas **light-colored cells (higher values)** indicate more patients in that category.
    """)

    # Key insights from the heatmap
    st.subheader("Key Insights from Your Patient Base")
    st.markdown("""
    - **The Best Patients**: Patients in the **R4-M4 segment** are your most valuable—recent visitors with high spending. They are likely to be loyal and satisfied.
    - **The At-Risk Group**: Patients in **R1-M1 or R1-M2** segments haven’t visited recently and have lower spending. These are potential churn risks and may need re-engagement strategies.
    - **The High-Spending Inactive Group**: Patients in **R1-M4** used to spend a lot but haven’t visited recently. They may require targeted promotions to encourage them to return.
    """)

    # How to use the insights
    st.subheader("How to Use This Analysis in Your Clinic?")
    st.markdown("""
    1. **Loyalty and Retention Strategies**  
    - Prioritize patients in the **R4-M4** and **R3-M4** segments with VIP offers or exclusive benefits to maintain their loyalty.  

    2. **Reactivation Campaigns**  
    - Reach out to patients in the **R1 segments** (especially R1-M4) with reminders, discounts, or personalized messages to encourage them to book an appointment.  

    3. **Optimizing Marketing Efforts**  
    - Target mid-range patients (**R2-M3, R3-M3**) to convert them into high-value patients through value-added services or membership programs.  
    """)

    st.success("By leveraging this RFM analysis, you can tailor your patient engagement strategies, improve retention, and increase clinic revenue effectively.")
