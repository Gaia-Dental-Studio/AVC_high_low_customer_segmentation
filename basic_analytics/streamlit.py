import streamlit as st 
import pandas as pd 
import numpy as np
import pickle
import locale


# st.set_page_config(layout="wide")
def app():

    


    st.title('Clinic Basic Analytics Dashboard')

    st.write("This dashboard is created to provide basic analytics for a clinic." 
            " The analytics provided are descriptive type of analytics")

    with open('basic_analytics/variable_metrics.pkl', 'rb') as file:
        variable_metrics = pickle.load(file)

    # load all pickle files
    with open('basic_analytics/age_category_count.pkl', 'rb') as file:
        age_category_count = pickle.load(file)
        
        
    with open('basic_analytics/age_distribution.pkl', 'rb') as file:
        age_distribution = pickle.load(file)
        
    with open('basic_analytics/average_unique_customer_per_year.pkl', 'rb') as file:
        average_unique_customer_per_year = pickle.load(file)
        
    with open('basic_analytics/count_transaction.pkl', 'rb') as file:
        count_transaction = pickle.load(file)
        
    with open('basic_analytics/count_transaction_yearly.pkl', 'rb') as file:
        count_transaction_yearly = pickle.load(file)
        
    with open('basic_analytics/diagnosa_count.pkl', 'rb') as file:
        diagnosa_count = pickle.load(file)
        
    with open('basic_analytics/fee_distribution.pkl', 'rb') as file:
        fee_distribution = pickle.load(file)
        
    with open('basic_analytics/keluhan_count.pkl', 'rb') as file:
        keluhan_count = pickle.load(file)
        
    with open('basic_analytics/treatment_count.pkl', 'rb') as file:
        treatment_count = pickle.load(file)
        
    with open('basic_analytics/count_unique_per_gender.pkl', 'rb') as file:
        count_unique_gender = pickle.load(file)
        
    with open('basic_analytics/fee_distribution_swarm.pkl', 'rb') as file:
        fee_distribution_swarm = pickle.load(file)
        
    grouped_by_age = pd.read_csv('basic_analytics/grouped_by_age.csv')


    st.markdown("### Transaction Overview")

    transaction_log = pd.read_csv('basic_analytics/data_pasien.csv')

    transaction_log.drop(columns=['Nomor Hp'], inplace=True)

    # st.dataframe(transaction_log, use_container_width=True, hide_index=True)


    average_transaction_monthly = variable_metrics['average_transaction_monthly']
    average_transaction_yearly = variable_metrics['average_transaction_yearly']
    standard_deviation_transaction_monthly = variable_metrics['standard_deviation_transaction_monthly']
    standard_deviation_transaction_yearly = variable_metrics['standard_deviation_transaction_yearly']

    average_non_member_fee = variable_metrics['average_non_member_fee']
    average_member_fee = variable_metrics['average_member_fee']
    std_non_member_fee = variable_metrics['std_non_member_fee']
    std_member_fee = variable_metrics['std_member_fee']




    col1, col2 = st.columns(2)

    with col1:
        
        st.plotly_chart(count_transaction)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.metric("Average Transaction Monthly", average_transaction_monthly)
        with col4:
            st.metric("Standard Deviation Transaction Monthly", standard_deviation_transaction_monthly)
        
        
    with col2:
        
        st.plotly_chart(count_transaction_yearly)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.metric("Average Transaction Yearly", average_transaction_yearly)
        with col4:
            st.metric("Standard Deviation Transaction Yearly", standard_deviation_transaction_yearly)
        
    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(average_unique_customer_per_year)
        
    with col2:
        st.plotly_chart(count_unique_gender)

    st.markdown("### Age Distribution")

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(age_distribution)
        
    with col2:
        
        st.plotly_chart(age_category_count)
        

        

    st.markdown("### Fee Distribution")

    st.dataframe(grouped_by_age)

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(fee_distribution)
        
        col3, col4= st.columns(2)
        
        with col3:
            
            locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
            st.metric("Average Non Member Fee", f"Rp. {locale.format_string('%d', average_non_member_fee, grouping=True)}")
            st.metric("Standard Deviation Non Member Fee", f"Rp. {locale.format_string('%d', std_non_member_fee, grouping=True)}")
            
        with col4:
            st.metric("Average Member Fee", f"Rp. {locale.format_string('%d', average_member_fee, grouping=True)}")
            st.metric("Standard Deviation Member Fee", f"Rp. {locale.format_string('%d', std_member_fee, grouping=True)}")
    with col2:
        
        st.plotly_chart(fee_distribution_swarm)
        

    st.markdown("### Diagnosis, Complaints, and Treatment")


    col1, col2, col3 = st.columns(3)

    with col1:

        st.plotly_chart(keluhan_count)

    with col2:

        st.plotly_chart(diagnosa_count)
        
    with col3:
        
        st.plotly_chart(treatment_count)
