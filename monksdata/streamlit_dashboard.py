import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from model_training import load_data, prepare_data, train_model  # Import your functions

# Function to create a scatter plot for a given predictor
def plot_scatter(X, y, predictor):
    fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis
    ax.scatter(X[predictor], y, alpha=0.6)
    ax.set_xlabel(predictor)
    ax.set_ylabel('Key Events')
    ax.set_title(f'Scatter Plot of {predictor} vs Key Events')
    st.pyplot(fig)  # Pass the figure to st.pyplot

# Streamlit UI
st.title('Key Events Impact Analysis Tool')

# Use a unique key for the file uploader
uploaded_file = st.file_uploader("Upload your GA4 data", type='csv', key='ga4_data_uploader')

if uploaded_file is not None:
    # Load data
    data = load_data(uploaded_file)
    X, y = prepare_data(data)
    
    # Train the model
    model, X_test, y_test = train_model(X, y)
    
    # Data Insights section
    st.subheader("Data Insights")

    # Coefficients section
    with st.expander("Coefficients", icon=":material/info:"):
        coefficients = dict(zip(X.columns, model.coef_))
        formatted_coefficients = {k: f"{v:.2f}" for k, v in coefficients.items()}
        st.write(formatted_coefficients)

    # Scatter plots section
    with st.expander("Scatter Plots", icon=":material/analytics:"):
        for predictor in X.columns:
            plot_scatter(X, y, predictor)

    # Insights section
    with st.expander("Insights", icon=":material/insights:"):
        strongest_positive = max(coefficients, key=coefficients.get)
        strongest_negative = min(coefficients, key=coefficients.get)
        st.write(f"From this data, we can see that the '{strongest_positive}' variable has the strongest positive correlation with Key Events. This means that this is most likely to drive more Key Events to the site.")
        st.write(f"Conversely, the '{strongest_negative}' variable has the strongest negative correlation with Key Events, indicating that increases in this metric might lead to a decrease in Key Events.")