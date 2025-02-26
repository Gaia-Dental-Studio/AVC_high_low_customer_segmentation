import streamlit as st
from streamlit_navigation_bar import st_navbar
import main_app
import analytics
import analytics2
import customer_based_app
import rfm_analysis
from basic_analytics import streamlit as basic_analytics
st.set_page_config(layout="wide")
# Create sidebar with two options
selection = st.sidebar.selectbox("Select Analysis Type", ["Basic Analytics","Customer-Based Analysis", "RFM Analysis"])

if selection == "Basic Analytics":
    basic_analytics.app()

elif selection == "Customer-Based Analysis":
    customer_based_app.app()

elif selection == "RFM Analysis":
    rfm_analysis.app()
    