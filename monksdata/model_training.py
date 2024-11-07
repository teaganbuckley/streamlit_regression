import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

def load_data(file):
    df = pd.read_csv(file)
    return df

def prepare_data(df):
    df.columns = df.columns.str.strip()
    required_columns = ['Total users', 'New users', 'Sessions', 'Bounce rate', 'Key events']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"The following required columns are missing: {missing_columns}")
    X = df[['Total users', 'New users', 'Sessions', 'Bounce rate']]
    y = df['Key events']
    return X, y

def train_model(model_file='trained_model.pkl', training_file='streamlit_monksdata.csv'):
    training_data = load_data(training_file)
    X_train, y_train = prepare_data(training_data)
    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, model_file)
    return model