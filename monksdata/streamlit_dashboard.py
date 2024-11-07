import streamlit as st
from model_training import load_data, prepare_data, train_model  # Import your functions

# Streamlit UI
st.title('Key Events Impact Analysis Tool')
uploaded_file = st.file_uploader("Upload your GA4 data", type='csv')

if uploaded_file is not None:
    # Load data
    data = load_data(uploaded_file)
    X, y = prepare_data(data)
    
    # Train the model
    model, X_test, y_test = train_model(X, y)
    
    # Display results
    st.write("Model Coefficients:")
    st.write(dict(zip(X.columns, model.coef_)))
    
    prediction = model.predict(X_test)
    st.write("Predictions of Key Events on Test Data:")
    st.line_chart(prediction)