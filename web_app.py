import streamlit as st
import pickle
from datetime import date
import numpy as np
import time
import pandas as pd

# Load necessary models and data
Adaboost = pickle.load(open('AdaBoost.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
country_codes = pickle.load(open('Country_Codes.pkl', 'rb'))
Customer_dataset = pickle.load(open('Customer_dataset.pkl','rb'))

# Function to process data
def process_data(data):
    arr = np.array(data)
    arr = arr.reshape(1, -1)
    trans_data = scaler.transform(arr)
    cluster = Adaboost.predict(trans_data)
    return cluster

# Set page configuration
st.set_page_config(
    page_title="Customer Segmentation Tool",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)


# Add a custom CSS style for enhancements
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        font-size: 16px;
        padding: 8px 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Web page title and introduction
st.title("📊 Customer Segmentation Tool")
st.markdown(
    """
    Welcome to the **Customer Segmentation Tool**!  
    Input customer details below to discover which cluster they belong to.  
    _Gain valuable insights and optimize your business strategies!_
    """
)

# Sidebar content
st.sidebar.header("Navigation")
st.sidebar.markdown("Navigate through the app using this panel.")

if st.sidebar.checkbox("About This App"):
    st.sidebar.subheader("About Customer Segmentation Tool")
    st.sidebar.markdown(
        """
        Welcome to the **Customer Segmentation Tool**!  
        This app helps businesses group customers into meaningful segments by analyzing their shopping behavior.  

        ### Key Features:
        - **Customer Clustering**: Groups customers into segments based on their recency, frequency, monetary values, and country.
        - **Intelligent Insights**: Gain a better understanding of high-value, dormant, and new customers.
        - **Interactive Dashboard**: User-friendly inputs and detailed results for better decision-making.

        ### Why Use This Tool?
        - Identify high-value customers to target for marketing campaigns.
        - Enhance customer retention by understanding inactive customer behavior.
        - Optimize business strategies with data-driven segmentation insights.
        """
    )

if st.sidebar.checkbox("Want details about all the clusters?"):
    st.sidebar.subheader("Cluster Details")
    st.sidebar.markdown(
        """
        **Cluster 0**:
        - Low Recency (recently active customers)
        - High Frequency and Monetary value (high-value customers)

        **Cluster 1**:
        - Moderate Recency
        - Moderate Frequency and Monetary value (average-value customers)

        **Cluster 2**:
        - High Recency (inactive customers)
        - Low Frequency and Monetary value (low-value customers)

        **Cluster 3**:
        - Low Recency (recently active customers)
        - Low Frequency and Monetary value (new customers)
        """
    )

# Input fields for customer data
st.header("🔍 Input Customer Details")

# Input: Customer ID
customer_id = st.text_input(
    "🔢 Customer ID", 
    help="Enter the unique Customer ID.", 
    placeholder="E.g., 12345"
)

# Input: Last Date of Purchase
last_purchase_date = st.date_input(
    "📅 Last Date of Purchase", 
    help="Select the date of the customer's last transaction."
)

# Input: Total Transaction Amount
total_transaction = st.number_input(
    "💰 Total Transaction Amount",
    min_value=0.0,
    step=0.01,
    format="%.2f",
    help="Enter the total amount spent by the customer in the store.",
)

# Input: Approximate Total Visits
total_visits = st.number_input(
    "🛒 Approx Total Visits",
    min_value=1,
    step=1,
    help="Enter the total number of visits the customer has made."
)

# Input: Country of Residence
country = st.selectbox(
    "🌍 Country of Residence",
    ['Select a country', 'United Kingdom', 'France', 'Australia', 'Netherlands', 'Germany',
     'Norway', 'EIRE', 'Switzerland', 'Spain', 'Poland', 'Portugal',
     'Italy', 'Belgium', 'Lithuania', 'Japan', 'Iceland',
     'Channel Islands', 'Denmark', 'Cyprus', 'Sweden', 'Austria',
     'Israel', 'Finland', 'Greece', 'Singapore', 'Lebanon',
     'United Arab Emirates', 'Saudi Arabia', 'Czech Republic', 'Canada',
     'Unspecified', 'Brazil', 'USA', 'European Community', 'Bahrain',
     'Malta', 'RSA'],
    help="Select the customer's country of residence."
)

# Submit button to process data
if st.button("🔎 Submit and Analyze"):
    if customer_id and country != "Select a country":
        # Calculate RFM metrics
        recency = (date.today() - last_purchase_date).days
        frequency = total_visits
        monetary = total_transaction
        country_encoded = country_codes[country]

        lst = [recency, frequency, monetary, country_encoded]

        # Process the data and predict the cluster
        with st.spinner("Processing your data..."):
            time.sleep(2)
            cluster_id = process_data(lst)

        st.success("🎉 Analysis Complete!")
        st.markdown(
            f"""
            ### **Results**
            - **Customer ID**: `{customer_id}`  
            - **Cluster Assigned**: `Cluster {cluster_id[0]}`  
            - **Recency**: `{recency} days since last purchase`  
            - **Frequency**: `{frequency} visits`  
            - **Monetary**: `${monetary:.2f}`  
            - **Country**: `{country}`  
            """
        )
    else:
        st.error("⚠️ Please ensure all fields are filled correctly!")

# Add a footer
st.markdown("---")
st.markdown(
    """
    **Built with ❤️ using [Streamlit](https://streamlit.io)**  
    _Optimize customer engagement with data-driven insights!_
    """
)
