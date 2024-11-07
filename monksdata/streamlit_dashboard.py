import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
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

# Tool description
st.write("This interactive tool empowers you to analyze the impact of various website metrics on key event outcomes. ")

# Data Preparation section
st.header("Data Preparation")
with st.expander("Upload Your Data", icon=":material/upload:"):
    st.write("Please upload at least three months of GA4 data with the following fields: Day, Sessions, Total Users, New Users, Bounce Rate, and Key Events.")
    # File uploader
    uploaded_file = st.file_uploader("Upload your GA4 data", type='csv', key='ga4_data_uploader')

    if uploaded_file is not None:
        # Load data
        data = load_data(uploaded_file)
        X, y = prepare_data(data)

        # Train the model
        model, X_test, y_test = train_model(X, y)

# Data Insights section
if 'X' in locals():  # Check if X is defined
    st.header("Data Insights")
    
    # Coefficients section
    with st.expander("Coefficients", icon=":material/info:"):
        st.write("Coefficients represent the relationship between each metric and the key events. A positive coefficient indicates that an increase in the predictor will lead to an increase in key events, while a negative coefficient indicates the opposite.")
        coefficients = dict(zip(X.columns, model.coef_))
        
        # Formatting the coefficients for better readability
        formatted_coefficients = {k: f"{v:.2f}" for k, v in coefficients.items()}
        sorted_coefficients = sorted(formatted_coefficients.items(), key=lambda item: item[1], reverse=True)

        st.write("### Coefficients Summary")
        for variable, value in sorted_coefficients:
            st.write(f"**{variable}**: {value}")

    # Scatter plots section
    with st.expander("Scatter Plots", icon=":material/analytics:"):
        st.write("Scatter plots visualize the relationship between each metric and the key events. Each point represents a data sample; the closer the points are to a straight line, the stronger the relationship.")
        for predictor in X.columns:
            plot_scatter(X, y, predictor)

    # Insights section
    with st.expander("Insights", icon=":material/insights:"):
        strongest_positive = max(coefficients, key=coefficients.get)
        strongest_negative = min(coefficients, key=coefficients.get)
        st.write(f"From this data, we can see that the '{strongest_positive}' variable has the strongest positive correlation with Key Events.")
        st.write(f"Conversely, the '{strongest_negative}' variable has the strongest negative correlation with Key Events.")

# Data Prediction section
if 'X' in locals():  # Only show the prediction section if data has been loaded
    st.header("Data Prediction")
    with st.expander("Impact Calculator", icon=":material/calculate:"):
        st.write("Predict how changes in your key GA4 metrics will impact your key events.")
        
        # User input for the calculator
        selected_variable = st.selectbox("Select the metric you'd like to evaluate.", options=X.columns)
        daily_change = st.number_input("What is the daily change you want to simulate (positive or negative)?", value=0.0, format="%.2f")

        period = st.radio("Select the period to model", ["Week", "Month", "Quarter"])
        
        if st.button("Calculate Impact"):
            # Determine change based on selected period
            if period == "Week":
                total_change = daily_change * 7
            elif period == "Month":
                total_change = daily_change * 30
            elif period == "Quarter":
                total_change = daily_change * 90

            # Calculate predicted impact
            current_values = X.mean()  # Average current values
            current_x_value = current_values[selected_variable]
            new_x_value = current_x_value + total_change
            input_data = pd.DataFrame({col: [current_values[col]] for col in X.columns})
            input_data[selected_variable] = new_x_value
            predicted_y = model.predict(input_data)[0]

            # Calculate the change in key events
            original_predicted_y = model.predict([current_values])[0]
            change_in_events = predicted_y - original_predicted_y

            # Construct the result message
            if change_in_events > 0:
                result_message = f"Over a {period}, changing your {selected_variable} by {daily_change} a day is predicted to drive an additional {change_in_events:.2f} key events."
            else:
                result_message = f"Over a {period}, changing your {selected_variable} by {daily_change} a day is predicted to cause {abs(change_in_events):.2f} fewer key events to happen on site."

            # Display the result message
            st.write(result_message)