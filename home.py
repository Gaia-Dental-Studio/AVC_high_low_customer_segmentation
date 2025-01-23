import streamlit as st
from streamlit_navigation_bar import st_navbar
import main_app
import analytics
import analytics2
import customer_based_app
import rfm_analysis

# Create navigation bar with two options
selection = st_navbar(["Customer-Based Analysis", "RFM Analysis"])

if selection == "Customer-Based Analysis":
    customer_based_app.app()

elif selection == "RFM Analysis":

    rfm_analysis.app()
    