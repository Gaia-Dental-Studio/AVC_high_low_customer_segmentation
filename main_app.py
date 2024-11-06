import streamlit as st
import pandas as pd

def app():

    # Title and description
    st.title('Customer Category Segmentation')

    st.write("""
    This calculator measures the effect of changing the average spend of each customer category and their count 
    on overall revenue, overall cost, and profit.
    """)

    # Load the historical data (replace 'average_historical_data.csv' with the actual path to the CSV file)
    average_historical_data = pd.read_csv('average_historical_data.csv')
    average_historical_data['Average Grand Total (Rp.)'] = average_historical_data['Average Spending (Rp.)'] * average_historical_data['Average Treatment Frequency']
    average_historical_data['Average Total Material Cost (Rp.)'] = average_historical_data['Average Material Cost (Rp.)'] * average_historical_data['Average Treatment Frequency']

    average_historical_data['Average Grand Total (Rp.)'] = average_historical_data['Average Grand Total (Rp.)'].round(0)
    average_historical_data['Average Total Material Cost (Rp.)'] = average_historical_data['Average Total Material Cost (Rp.)'].round(0)

    # Display a data editor for user to modify the customer category details
    st.subheader('Customer Category Data')
    
    calculation_scheme = st.radio("Select Calculation Scheme", ["By Average Spending per treatment and Treatment Frequency", "By Grand Total Spending"])
    
    if calculation_scheme == "By Average Spending per treatment and Treatment Frequency":
        average_historical_data = st.data_editor(average_historical_data, key="customer_category_data", 
                                                 hide_index=True, use_container_width=True, 
                                                 column_order=["Category", "Average Spending (Rp.)", "Average Material Cost (Rp.)", "Average Treatment Frequency", "Count"])
        
    else:
        average_historical_data = st.data_editor(average_historical_data, key="customer_category_data", 
                                                 hide_index=True, use_container_width=True, 
                                                 column_order=["Category", "Average Grand Total (Rp.)", "Average Total Material Cost (Rp.)", "Count"])


    st.write('The underlying data are based on total of three months historical data.')
    # Divider for separation of sections
    st.divider()

    # Function to calculate category-specific metrics
    def calculate_category_metrics(data, calculation_scheme):
        # Create a new DataFrame for metrics
        metrics_df = pd.DataFrame(columns=["Category", 'Count Proportion (%)', "Revenue (Rp.)", "Cost (Rp.)", "Profit (Rp.)"])
        
        # Calculate the total count across all categories
        total_count = data['Count'].sum()
        
        for index, row in data.iterrows():
            # Round revenue, cost, and profit to 0 decimal places
            if calculation_scheme == "By Average Spending per treatment and Treatment Frequency":
                revenue = round(row['Average Spending (Rp.)'] * row['Average Treatment Frequency'] * row['Count'], 0)
                cost = round(row['Average Material Cost (Rp.)'] * row['Average Treatment Frequency'] * row['Count'], 0)
            else:
                revenue = round(row['Average Grand Total (Rp.)'] * row['Count'], 0)
                cost = round(row['Average Total Material Cost (Rp.)'] * row['Count'], 0)
            
            profit = round(revenue - cost, 0)
            
            # Calculate the proportion of this category's count to the total count
            proportion = round((row['Count'] / total_count) * 100, 2)  # Rounded to 2 decimal places
            
            # Append the row to metrics_df
            metrics_df = metrics_df._append({
                "Category": f"Category {index + 1}",
                "Count Proportion (%)": proportion,
                "Revenue (Rp.)": revenue,
                "Cost (Rp.)": cost,
                "Profit (Rp.)": profit,
                
            }, ignore_index=True)
        
        return metrics_df

    # Calculate the metrics based on the user-modified data
    category_metrics_df = calculate_category_metrics(average_historical_data, calculation_scheme)

    # Display category-specific metrics in a dataframe format
    st.subheader('Category-Specific Metrics')
    st.dataframe(category_metrics_df, hide_index=True)

    st.write("Count Proportion (%) is the proportion of each category's count of customer to the total count of all categories.")

    # Divider for separation of sections
    st.divider()

    # Section for overall metrics visualization (Three Months)
    st.subheader("Overall Metrics")
    st.caption("Expected performance in three months")

    # Calculate current overall metrics
    total_revenue = category_metrics_df["Revenue (Rp.)"].sum()
    total_cost = category_metrics_df["Cost (Rp.)"].sum()
    total_profit = total_revenue - total_cost

    # Check if initial metrics are already stored in session state
    if "initial_total_revenue" not in st.session_state:
        st.session_state.initial_total_revenue = total_revenue
        st.session_state.initial_total_cost = total_cost
        st.session_state.initial_total_profit = total_profit

    # Calculate deltas
    revenue_delta = ((total_revenue - st.session_state.initial_total_revenue) / st.session_state.initial_total_revenue) * 100
    cost_delta = ((total_cost - st.session_state.initial_total_cost) / st.session_state.initial_total_cost) * 100
    profit_delta = ((total_profit - st.session_state.initial_total_profit) / st.session_state.initial_total_profit) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Total Revenue (3 months)", value=f"Rp.{total_revenue:,.0f}", delta=f"{revenue_delta:.2f}%")
        st.metric(label="Total Cost (3 months)", value=f"Rp.{total_cost:,.0f}", delta=f"{cost_delta:.2f}%")

    with col2:
        st.metric(label="Total Profit (3 months)", value=f"Rp.{total_profit:,.0f}", delta=f"{profit_delta:.2f}%")

    # Divider before per-month metrics
    st.divider()

    # Section for overall metrics visualization (Per Month)
    st.subheader("Per Month Metrics")

    # Calculate per-month metrics
    per_month_revenue = total_revenue / 3
    per_month_cost = total_cost / 3
    per_month_profit = total_profit / 3

    # Calculate deltas for per-month metrics
    per_month_revenue_delta = revenue_delta / 3
    per_month_cost_delta = cost_delta / 3
    per_month_profit_delta = profit_delta / 3

    col3, col4 = st.columns(2)

    with col3:
        st.metric(label="Total Revenue (per month)", value=f"Rp.{per_month_revenue:,.0f}", delta=f"{per_month_revenue_delta:.2f}%")
        st.metric(label="Total Cost (per month)", value=f"Rp.{per_month_cost:,.0f}", delta=f"{per_month_cost_delta:.2f}%")

    with col4:
        st.metric(label="Total Profit (per month)", value=f"Rp.{per_month_profit:,.0f}", delta=f"{per_month_profit_delta:.2f}%")
