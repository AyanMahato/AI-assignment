import streamlit as st
from utils.data_handler import handle_csv_upload, connect_google_sheet
from utils.search_api import query_scraper_api
from utils.llm_handler import process_with_llm
from utils.agent import orchestrate_query

st.title("Automated Data Extraction with LLMs")
st.sidebar.header("Options")

# Upload CSV or Connect Google Sheets
upload_option = st.sidebar.selectbox("Choose Input Type", ["Upload CSV", "Connect Google Sheet"])
if upload_option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file:
        df = handle_csv_upload(uploaded_file)
        st.dataframe(df)
elif upload_option == "Connect Google Sheet":
    google_sheet_url = st.text_input("Enter Google Sheet URL")
    if google_sheet_url:
        df = connect_google_sheet(google_sheet_url)
        st.dataframe(df)

# Specify Query
query_template = st.text_input("Enter your query template with the key details about the data present in csv in {"+"brackets}")
if st.button("Run Query"):
    if 'df' in locals():
        results = orchestrate_query(df, query_template)
        st.write("Results:")
        st.dataframe(results)
        st.download_button("Download CSV", results.to_csv(index=False), file_name="results.csv")
