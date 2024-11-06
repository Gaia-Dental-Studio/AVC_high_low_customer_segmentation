
import pandas as pd
import numpy as np
from random import choice, choices, sample
import datetime
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans

class ModelTransactionGenerator:
    def __init__(self, treatment_df, total_price, price_basis, num_unique_patients, total_unique_patients, dentist_providers, dentist_probabilities, start_date, end_date):
        self.treatment_df = treatment_df
        self.total_price = total_price  # total price of all transactions per year
        self.price_basis = price_basis
        self.num_unique_patients = num_unique_patients
        self.total_unique_patients = total_unique_patients
        self.dentist_providers = dentist_providers
        self.dentist_probabilities = dentist_probabilities
        self.start_date = start_date
        self.end_date = end_date
        
        # Generate the overall unique patient pool
        self.patient_ids = [f'Patient_{str(i).zfill(3)}' for i in range(1, self.total_unique_patients + 1)]
        self.patient_age_ids = np.random.randint(18, 80, size=self.total_unique_patients)
        self.patient_age_map = dict(zip(self.patient_ids, self.patient_age_ids))
        
        self.patient_transaction_df = None
        self.per_patient_summary_df = None

    def random_date(self, start, end):
        return start + datetime.timedelta(days=np.random.randint(0, (end - start).days))
    
    def get_eligible_days(self, year):
        # Calculate the start and end dates within the given year that fall into the overall start and end date range
        year_start = max(self.start_date, datetime.date(year, 1, 1))
        year_end = min(self.end_date, datetime.date(year, 12, 31))
        return (year_end - year_start).days + 1  # Add 1 to include the end day

    def create_transaction_df(self):
        transactions = []
        current_year = self.start_date.year
        end_year = self.end_date.year

        # Iterate over each year in the range
        while current_year <= end_year:
            eligible_days = self.get_eligible_days(current_year)
            if eligible_days <= 0:
                current_year += 1
                continue  # Skip years that have no eligible days

            # Calculate the number of unique patients for this year
            num_patients_for_year = int(self.num_unique_patients / 365 * eligible_days)
            patient_subset = sample(self.patient_ids, num_patients_for_year)

            # Calculate the maximum total price for this year
            max_total_price_for_year = self.total_price / 365 * eligible_days
            current_total_price = 0

            # Generate transactions for the current year
            while current_total_price <= max_total_price_for_year:
                # Randomly select a treatment
                treatment = self.treatment_df.sample(1).iloc[0]

                if self.price_basis == 'Indonesia':
                    price = treatment['total_price_IDR']
                    material_cost = treatment['total_cost_IDR']
                    duration = treatment['total_duration']
                else:  # 'Australia'
                    price = treatment['total_price_AUD']
                    material_cost = treatment['total_cost_AUD']
                    duration = treatment['total_duration']

                # Check if adding this transaction exceeds the maximum total price for the year
                if current_total_price + price > max_total_price_for_year:
                    break

                # Randomly select a patient from the subset and get their age
                patient_id = choice(patient_subset)
                age = self.patient_age_map[patient_id]

                # Randomly select a provider based on the given probabilities
                provider = choices(self.dentist_providers, self.dentist_probabilities)[0]

                # Generate a random date within the current year
                year_start_date = max(self.start_date, datetime.date(current_year, 1, 1))
                year_end_date = min(self.end_date, datetime.date(current_year, 12, 31))
                date = self.random_date(year_start_date, year_end_date)

                # Create a new transaction
                transaction = {
                    'Patient ID': patient_id,
                    'Age': age,
                    'Treatment': treatment['Treatment'],
                    'Duration': duration,
                    'Date': date,
                    'Provider Dentist': provider,
                    'Price': price,
                    'Material Cost': material_cost
                }

                # Append the transaction to the list
                transactions.append(transaction)

                # Update the accumulated total price for the year
                current_total_price += price

            # Move to the next year
            current_year += 1

        # Create the final DataFrame
        patient_transaction_df = pd.DataFrame(transactions)
        patient_transaction_df['Date'] = pd.to_datetime(patient_transaction_df['Date'])
        patient_transaction_df['Date'] = patient_transaction_df['Date'].dt.date  # Remove time component
        
        # Sort the DataFrame by date
        patient_transaction_df = patient_transaction_df.sort_values(by='Date')
        patient_transaction_df = patient_transaction_df.reset_index()
        patient_transaction_df = patient_transaction_df.drop(columns='index')
        
        self.patient_transaction_df = patient_transaction_df
        
        
        
        return patient_transaction_df
    
    
    
    
    
    
    def dentist_contributions(self):
        dentist_contributions = self.patient_transaction_df.groupby('Provider Dentist')['Price'].sum()

        #change name of Price column to Sales Contribution
        dentist_contributions = dentist_contributions.reset_index().rename(columns={'Price': 'Sales Contribution'})
        
        self.dentist_contributions = dentist_contributions
        
        return dentist_contributions


    def per_patient_summary(self):
        # Group by 'Patient ID' and calculate the required aggregations
        
        per_patient_summary = self.patient_transaction_df.groupby('Patient ID').agg(
            Grand_Total=('Price', 'sum'),
            Total_Material_Cost=('Material Cost', 'sum'),
            Treatment_Frequency=('Price', 'count'),  # Or you could use 'Treatment' to count non-null entries
            Average_Spending=('Price', 'mean'),
            Average_Material_Cost=('Material Cost', 'mean'),
            # get the recent date of transaction for each patient
            First_Transaction_Date=('Date', 'min'),
            Last_Transaction_Date=('Date', 'max')
        ).reset_index()
        
        per_patient_summary['First_Transaction_Date'] = pd.to_datetime(per_patient_summary['First_Transaction_Date']).dt.date
        per_patient_summary['Last_Transaction_Date'] = pd.to_datetime(per_patient_summary['Last_Transaction_Date']).dt.date
        
        # Sort summary_df by 'Grand Total' in descending order
        per_patient_summary = per_patient_summary.sort_values(by='Grand_Total', ascending=False).reset_index(drop=True)

        # Calculate the cumulative revenue percentage
        total_revenue = per_patient_summary['Grand_Total'].sum()
        per_patient_summary['Cumulative_Revenue'] = per_patient_summary['Grand_Total'].cumsum() / total_revenue * 100

        # Assign categories based on the cumulative revenue percentage
        per_patient_summary['Category'] = pd.cut(
            per_patient_summary['Cumulative_Revenue'],
            bins=[0, 20, 40, 60, 80, 100],  # Divides the cumulative percentage into 5 equal parts
            labels=[1, 2, 3, 4, 5],
            right=True  # Includes the right endpoint
        )
    

        # Convert the 'Category' column to integer type for clarity
        per_patient_summary['Category'] = per_patient_summary['Category'].astype(int)
        per_patient_summary['Label'] = per_patient_summary['Category'].apply(lambda x: 'High' if x <= 2 else 'Low')
        

        # drop column of Cummulative Revenue 
        per_patient_summary = per_patient_summary.drop(columns='Cumulative_Revenue')
        # per_patient_summary = per_patient_summary.rename(columns={'Grand_Total': 'Grand Total', 'Total_Material_Cost': 'Total Material Cost', 
        #                                                           'Treatment_Frequency': 'Treatment Frequency', 'Average_Spending': 'Average Spending',
        #                                                           'Average_Material_Cost': 'Average Material Cost'})
        per_patient_summary = per_patient_summary.reset_index()
        per_patient_summary = per_patient_summary.drop(columns='index')
        
        per_patient_summary['Age'] = per_patient_summary['Patient ID'].apply(lambda pid: self.patient_age_map[pid])
        
        #shift the Age column as second column 
        cols = per_patient_summary.columns.tolist()
        cols = cols[:1] + cols[-1:] + cols[1:-1]
        per_patient_summary = per_patient_summary[cols]
        
        
        self.per_patient_summary_df = per_patient_summary


        # Display the summary DataFrame
        return per_patient_summary
    
        
    def create_net_customer_gain(self):
        patient_transaction_df = self.patient_transaction_df
        start_date = self.start_date
        end_date = self.end_date
        
        # Add a Year column to patient_transaction_df for grouping
        patient_transaction_df['Year'] = pd.to_datetime(patient_transaction_df['Date']).dt.year

        # Initialize the net_customer_gain and unique_patient DataFrames
        years = sorted(patient_transaction_df['Year'].unique())
        net_customer_gain = pd.DataFrame(columns=['Year', 'New Patient', 'Leaving Patient', 'Total Unique Patients'])
        unique_patient = pd.DataFrame(columns=['Year', 'Patients'])
        
        # Iterate over each year and calculate new and leaving patients
        for year in years:
            # Get current year's data
            current_year_df = patient_transaction_df[patient_transaction_df['Year'] == year]
            total_unique_patients_count = current_year_df['Patient ID'].nunique()  # Count unique patients for the year
            
            # Get array of unique patient IDs for the current year
            unique_patients_list = current_year_df['Patient ID'].unique().tolist()
            
            # Append the result to unique_patient DataFrame
            unique_patient = unique_patient.append({
                'Year': year,
                'Patients': unique_patients_list
            }, ignore_index=True)
            
            if year == start_date.year:
                # Skip new patient calculation for the first year
                new_patients_count = 0
            else:
                # Find new patients for the current year
                previous_year_df = patient_transaction_df[
                    (patient_transaction_df['Date'] >= pd.to_datetime(year, format='%Y') - pd.Timedelta(days=365)) &
                    (patient_transaction_df['Date'] < pd.to_datetime(year, format='%Y'))
                ]

                new_patients = current_year_df.groupby('Patient ID')['Date'].min().reset_index()
                new_patients['Is_New'] = new_patients['Patient ID'].apply(
                    lambda pid: pid not in previous_year_df['Patient ID'].unique()
                )
                new_patients_count = new_patients['Is_New'].sum()

            # Find leaving patients for the current year
            if year < end_date.year:
                # Get patients from all previous years up to the current year - 1
                previous_patients = patient_transaction_df[patient_transaction_df['Year'] < year].groupby('Patient ID')['Date'].max().reset_index()
                previous_patients['Last_Transaction_Plus_One_Year'] = pd.to_datetime(previous_patients['Date']) + pd.Timedelta(days=365)

                # Check if any previous patients do not appear in the current year
                leaving_patients = previous_patients[
                    previous_patients.apply(
                        lambda row: row['Last_Transaction_Plus_One_Year'] <= pd.Timestamp(f'{year}-12-31') and
                        row['Patient ID'] not in current_year_df['Patient ID'].values, axis=1
                    )
                ]
                leaving_patients_count = leaving_patients['Patient ID'].nunique()
            else:
                # For the last year, check all patients from the prior year
                previous_year_patients = patient_transaction_df[patient_transaction_df['Year'] == year - 1]['Patient ID'].unique()
                leaving_patients_count = len([pid for pid in previous_year_patients if pid not in current_year_df['Patient ID'].values])

            # Append the results to net_customer_gain DataFrame
            net_customer_gain = net_customer_gain.append({
                'Year': year,
                'New Patient': new_patients_count,
                'Leaving Patient': leaving_patients_count,
                'Net Patient Gain': new_patients_count - leaving_patients_count,
                'Total Unique Patients': total_unique_patients_count
            }, ignore_index=True)
            
            # net_customer_gain = net_customer_gain.drop(columns='Total Unique Patients')
            net_customer_gain['Year'] = net_customer_gain['Year'].astype(str)
            net_customer_gain['Percentage Net Gain'] = net_customer_gain['Net Patient Gain'] / net_customer_gain['Total Unique Patients'] * 100
            
            net_customer_gain.to_csv('net_customer_gain.csv', index=False)

        return net_customer_gain, unique_patient
    
    
    
    def age_segmentation(self, k):# Sample data
        data = self.per_patient_summary_df


        # Run k-means clustering on the Age column
        kmeans_age = KMeans(n_clusters=k, random_state=0)
        data['Age Cluster'] = kmeans_age.fit_predict(data[['Age']])

        # Calculate the age range for each cluster
        cluster_summary = data.groupby('Age Cluster').agg(
            MeanAge=('Age', 'mean'),
            MeanGrandTotal=('Grand_Total', 'mean'),
            MinAge=('Age', 'min'),
            MaxAge=('Age', 'max')
        ).reset_index()

        # Sort clusters by MinAge for sequential processing
        cluster_summary.sort_values(by='MinAge', inplace=True)

        # Adjust cluster boundaries to ensure they are mutually exclusive and collectively exhaustive
        overall_min_age = data['Age'].min()
        overall_max_age = data['Age'].max()

        # Set the minimum age for the first cluster
        cluster_summary.iloc[0, cluster_summary.columns.get_loc('MinAge')] = overall_min_age

        # Adjust each cluster's MaxAge to ensure no gaps and mutual exclusivity
        for i in range(len(cluster_summary) - 1):
            cluster_summary.iloc[i, cluster_summary.columns.get_loc('MaxAge')] = (
                cluster_summary.iloc[i + 1, cluster_summary.columns.get_loc('MinAge')] - 1
            )

        # Ensure the last cluster's MaxAge reaches the overall maximum age
        cluster_summary.iloc[-1, cluster_summary.columns.get_loc('MaxAge')] = overall_max_age

        cluster_summary['Age Cluster'] = range(1, k+1)
        
        cluster_summary[['Age Cluster', 'MinAge', 'MaxAge']] = cluster_summary[['Age Cluster', 'MinAge', 'MaxAge']].astype(int)

        cluster_summary =  cluster_summary[['Age Cluster', 'MinAge', 'MaxAge']]

        # Display the modified cluster summary with age ranges
        return cluster_summary
    
    
    def clv_forecast(self):
        
        df = self.per_patient_summary_df
        base_date = self.end_date
        
            # Convert date columns to datetime format if they are not already
        df['First_Transaction_Date'] = pd.to_datetime(df['First_Transaction_Date'])
        df['Last_Transaction_Date'] = pd.to_datetime(df['Last_Transaction_Date'])
        base_date = pd.to_datetime(base_date)
        
        # Calculate the threshold date
        threshold_date = base_date - timedelta(days=365)
        
        # Filter out rows where Last_Transaction_Date is older than the threshold_date
        df = df[df['Last_Transaction_Date'] >= threshold_date]
        
        df['Days Since First Transaction'] = (base_date - df['First_Transaction_Date']).dt.days
        
        # Calculate Remaining Lifetime Value for the remaining rows
        df['Remaining Lifetime'] = (365 * 3) - df['Days Since First Transaction'] 
        
        
        df = df[df['Remaining Lifetime'] > 0]
        
        df['Grand_Total'] = df['Grand_Total'].astype(int)
        df['Expected Remaining Lifetime Value'] = df['Grand_Total'] / df['Days Since First Transaction'] * df['Remaining Lifetime']
        df['Expected Remaining Lifetime Value'] = df['Expected Remaining Lifetime Value'].astype(int)
        
        df = df[['Patient ID','Days Since First Transaction', 'Remaining Lifetime', 'Grand_Total', 'Expected Remaining Lifetime Value']]
        
        total_clv = df['Expected Remaining Lifetime Value'].sum()
        total_patients = df['Patient ID'].nunique()
        average_remaining_lifetime = df['Remaining Lifetime'].mean()
        
        
        return df, total_clv, total_patients, average_remaining_lifetime
    
    
    
    def plot_combo_chart(self, input_df):
        # Create a figure
        fig = go.Figure()

        # Add the Net Patient Gain line chart
        fig.add_trace(
            go.Scatter(
                x=input_df['Year'],
                y=input_df['Net Patient Gain'],
                name='Net Patient Gain',
                mode='lines+markers',
                line=dict(color='#1167b1'),
                yaxis='y1'
            )
        )

        # Add the Percentage Net Gain line chart
        fig.add_trace(
            go.Scatter(
                x=input_df['Year'],
                y=input_df['Percentage Net Gain'],
                name='Percentage Net Gain',
                mode='lines+markers',
                line=dict(color='#2ca02c'),
                yaxis='y2'
            )
        )

        # Update layout for dual y-axes with locked ranges
        fig.update_layout(
            title='Net Patient Gain and Percentage Net Gain Over Years',
            xaxis=dict(
                title='Year',
                tickmode='array',
                tickvals=input_df['Year'],  # Set ticks to match the actual data points
                ticktext=input_df['Year'].astype(str)  # Ensure labels are shown as strings
            ),
            yaxis=dict(
                title='Net Patient Gain',
                titlefont=dict(color='#1167b1'),
                tickfont=dict(color='#1167b1'),
                range=[-300, 300]  # Locked range for the left y-axis
            ),
            yaxis2=dict(
                title='Percentage Net Gain (%)',
                titlefont=dict(color='#2ca02c'),
                tickfont=dict(color='#2ca02c'),
                overlaying='y',
                side='right',
                showgrid=False,
                range=[-60, 60]  # Locked range for the right y-axis in percentage
            ),
            height=600,
            width=1000,
            legend=dict(x=0.01, y=0.99)
        )
        
        

        return fig
    
    

    def plot_combo_chart_general(self, input_df, x, y1, y2=None, y1_name=None, y2_name=None, graph_title='Line Chart'):
        # Create a figure
        fig = go.Figure()

        # Use provided y-axis names or default to the column names
        y1_label = y1_name if y1_name else y1.replace('_', ' ').title()
        y2_label = y2_name if y2_name else (y2.replace('_', ' ').title() if y2 else '')

        # Add the first line chart for y1
        fig.add_trace(
            go.Scatter(
                x=input_df[x],
                y=input_df[y1],
                name=y1_label,
                mode='lines+markers',
                line=dict(color='#1167b1'),
                yaxis='y1'
            )
        )

        # Add the second line chart for y2 if provided
        if y2:
            fig.add_trace(
                go.Scatter(
                    x=input_df[x],
                    y=input_df[y2],
                    name=y2_label,
                    mode='lines+markers',
                    line=dict(color='#2ca02c'),
                    yaxis='y2'
                )
            )

        # Update layout for dual y-axes with locked ranges if y2 is provided
        layout_args = dict(
            title=graph_title,
            xaxis=dict(
                title=x.replace('_', ' ').title(),
                tickmode='array',
                tickvals=input_df[x],  # Set ticks to match the actual data points
                ticktext=input_df[x].astype(str)  # Ensure labels are shown as strings
            ),
            yaxis=dict(
                title=y1_label,
                titlefont=dict(color='#1167b1'),
                tickfont=dict(color='#1167b1')
            ),
            height=600,
            width=1000,
            legend=dict(x=0.01, y=0.99)
        )

        if y2:
            layout_args['yaxis2'] = dict(
                title=y2_label + ' (%)',
                titlefont=dict(color='#2ca02c'),
                tickfont=dict(color='#2ca02c'),
                overlaying='y',
                side='right',
                showgrid=False
            )

        fig.update_layout(**layout_args)

        return fig


    
    



    def transaction_vs_patient(self):
        df = self.patient_transaction_df

        # Convert 'Date' to datetime and extract the year
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year

        # Group by Year and calculate unique patient count and total transaction count
        grouped_df = df.groupby('Year').agg(
            Unique_Patient_Count=('Patient ID', pd.Series.nunique),
            Transaction_Count=('Patient ID', 'count')
        ).reset_index()

        # Create overlapping area chart using Plotly Graph Objects
        fig = go.Figure()

        # Add trace for Unique Patient Count
        fig.add_trace(go.Scatter(
            x=grouped_df['Year'],
            y=grouped_df['Unique_Patient_Count'],
            mode='lines',
            fill='tozeroy',
            name='Unique Patient Count'
        ))

        # Add trace for Transaction Count
        fig.add_trace(go.Scatter(
            x=grouped_df['Year'],
            y=grouped_df['Transaction_Count'],
            mode='lines',
            fill='tonexty',
            name='Transaction Count'
        ))

        # Update layout
        fig.update_layout(
            title="Yearly Count of Unique Patients and Transactions",
            xaxis=dict(
                title='Year',
                tickmode='array',
                tickvals=grouped_df['Year'],
                ticktext=grouped_df['Year'].astype(str)
            ),
            yaxis=dict(title='Count'),
            template="plotly_white"
        )

        # Calculate averages
        average_transaction_per_year = grouped_df['Transaction_Count'].mean()
        average_patient_per_year = grouped_df['Unique_Patient_Count'].mean()

        return fig, average_transaction_per_year, average_patient_per_year

