import streamlit as st 
import pandas as pd
import numpy as np
import datetime
from model_customer_based import ModelTransactionGenerator
from viz_analysis import VizAnalysis2


# st.set_page_config(layout="wide")

st.title("Customer Based Quality Analysis")

with st.expander("Transaction Data Generation"):
    st.markdown("### Transaction Data Generation")
    # Load treatment data
    treatment_df = pd.read_csv(r'Item Code and Treatments/treatment_with_details.csv')

    # Define inputs
    total_price = 1862464
    price_basis = 'Australia'
    num_unique_patients = 1000
    total_unique_patients = 1010
    dentist_providers = ['RE', 'BEC', 'CQ', 'DA', 'WS']
    dentist_probabilities = [0.54, 0.003, 0.27, 0.002, 0.185]


    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", datetime.date(2018, 1, 1))

    with col2:
        end_date = st.date_input("End Date", datetime.date(2023, 12, 31))


    # calculate the number of days between the start and end dates
    days = (end_date - start_date).days

    st.write(f"Days Between: {days}")

    # Create an instance of the class
    transaction_generator = ModelTransactionGenerator(
        treatment_df=treatment_df,
        total_unique_patients = total_unique_patients,
        total_price=total_price,
        price_basis=price_basis,
        num_unique_patients=num_unique_patients,
        dentist_providers=dentist_providers,
        dentist_probabilities=dentist_probabilities,
        start_date=start_date,
        end_date=end_date
    )

    # Generate the transaction DataFrame
    patient_transaction_df = transaction_generator.create_transaction_df()
    patient_transaction_df.to_csv('patient_transaction.csv', index=False)

    # Display the generated DataFrame
    st.dataframe(patient_transaction_df)

st.divider()

st.markdown("# Descriptive Analytics")

st.markdown("## Overall Summary")

st.markdown('### Transaction vs. Number of Patient')
transaction_vs_patient_chart, average_transaction_per_year, average_patients_per_year= transaction_generator.transaction_vs_patient()

st.plotly_chart(transaction_vs_patient_chart)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Transaction to Patient Ratio", round(average_transaction_per_year/average_patients_per_year, 2))
with col2:
    st.metric("Average Transaction per Year", round(average_transaction_per_year, 1))
with col3:
    st.metric("Average Patients per Year", round(average_patients_per_year,1))
    


st.markdown("## Per Patient Summary")

per_patient_summary = transaction_generator.per_patient_summary()

per_patient_summary.to_csv('per_patient_summary.csv', index=False)  

st.dataframe(per_patient_summary)


st.markdown("## Net Customer Gain")

net_customer_gain, unique_patient = transaction_generator.create_net_customer_gain()

# st.dataframe(unique_patient, hide_index=True, use_container_width=True)

st.dataframe(net_customer_gain[['Year', 'New Patient', 'Leaving Patient', 'Net Patient Gain', 'Total Unique Patients']] ,hide_index=True)

st.plotly_chart(transaction_generator.plot_combo_chart(net_customer_gain))

st.plotly_chart(transaction_generator.plot_combo_chart_general(net_customer_gain, x='Year', y1='Total Unique Patients', y1_name='Total Active Patients', graph_title='Total Active Patients'))


st.markdown("## Customer Lifetime Value Analysis")

st.write(f"Assumption of Today's Date: {end_date}")

clv_df, total_clv, total_clv_patients, average_remaining_lifetime = transaction_generator.clv_forecast()
st.dataframe(clv_df, hide_index=True)

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Patients with Remaining Lifetime", total_clv_patients)

    st.metric("Total Expected Remaining Lifetime Value", f"${total_clv:,.0f}")
    
with col2:
    st.metric("Average Remaining Lifetime (Years)", round(average_remaining_lifetime/365, 1))


st.divider()

st.markdown("## Demographic Analysis")

st.markdown("### Age Distribution")



per_patient_summary = per_patient_summary.rename(columns={'Grand_Total': 'Grand Total', 'Total_Material_Cost': 'Total Material Cost', 
                                                            'Treatment_Frequency': 'Treatment Frequency', 'Average_Spending': 'Average Spending',
                                                            'Average_Material_Cost': 'Average Material Cost'})

viz = VizAnalysis2(per_patient_summary)

age_distribution = viz.histogram(per_patient_summary, 'Age')
st.plotly_chart(age_distribution)

st.markdown("### Per Age Group Analysis")

st.write("Adjust Age Range Group Category")

age_class = st.number_input("Age Class", min_value=1, max_value=10, value=5)

age_class_df =  transaction_generator.age_segmentation(age_class)

age_class_df = st.data_editor(age_class_df, key="age_class_data", hide_index=True)


# Function to map the Age Cluster
def map_age_cluster(age):
    cluster = age_class_df[(age_class_df['MinAge'] <= age) & (age_class_df['MaxAge'] >= age)]
    if not cluster.empty:
        return cluster['Age Cluster'].values[0]
    return None

# Apply the function to create the new column in df1
per_patient_summary['Age Cluster'] = per_patient_summary['Age'].apply(map_age_cluster)

age_group_histogram = viz.histogram(per_patient_summary, 'Grand Total', 'Age Cluster')
st.plotly_chart(age_group_histogram)

st.markdown("**Age Group Swarm Plot**")
age_swarm_plot = viz.plot_swarm(x='Age Cluster')
st.plotly_chart(age_swarm_plot)


with st.expander("High & Low Analytics"):
    
    st.markdown("### High & Low Customer Analytics")

    select_mode = st.selectbox("Select Mode", ["By Category", "By Label (High & Low)"])

    def generate_figures(_viz, label=False):
        fig1 = _viz.plot_histogram_treat_freq(label)
        fig2 = _viz.plot_histogram_average_spending(label)
        fig3 = _viz.plot_scatter(label)
        if label:
            fig4 = _viz.plot_swarm(x="Label")
        else:
            fig4 = _viz.plot_swarm(x="Category")
        
        fig5 = _viz.plot_histogram_grand_total(label)
        return fig1, fig2, fig3, fig4, fig5




    
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
    st.pyplot(fig3)


    st.header("Swarm Plot of Grand Total by Category")
    st.plotly_chart(fig4, use_container_width=True)
