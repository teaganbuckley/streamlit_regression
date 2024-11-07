import streamlit as st
import pandas as pd
import joblib

def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    required_columns = ['Total users', 'New users', 'Sessions', 'Bounce rate', 'Key events']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"The following required columns are missing: {missing_columns}")
    return df

def prepare_data(df):
    X = df[['Total users', 'New users', 'Sessions', 'Bounce rate']]
    return X

def load_model(file):
    model = joblib.load(file)
    return model

st.title("Simple Linear Regression Dashboard")
uploaded_file = st.file_uploader("Upload your CSV file:", type="csv")

if uploaded_file:
    data = load_data(uploaded_file)
    st.write("Raw Data:")
    st.dataframe(data)
    X = prepare_data(data)
    model = load_model('trained_model.pkl')

    if not X.empty:
        predictions = model.predict(X)
        data['Predicted Key Events'] = predictions
        st.write("Predictions:")
        st.dataframe(data[['Total users', 'New users', 'Sessions', 'Bounce rate', 'Predicted Key Events']])