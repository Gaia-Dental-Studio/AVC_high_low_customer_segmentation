import streamlit as st
from streamlit_navigation_bar import st_navbar
import main_app
import analytics
import analytics2

# Create navigation bar with two options
selection = st_navbar(["Calculator", "Existing Analytics"])

if selection == "Calculator":
    main_app.app()

elif selection == "Existing Analytics":

    analytics2.app()
    
elif selection == "Test":
    analytics.app()