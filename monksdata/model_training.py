import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load and preprocess data
def load_data(file):
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%Y%m%d')
    df.columns = df.columns.str.strip()  # Remove whitespace
    df.set_index('Date', inplace=True)
    return df

# Prepare data for modeling
def prepare_data(df):
    df = df[['Total users', 'New users', 'Sessions', 'Bounce rate', 'Key events']]
    X = df[['Total users', 'New users', 'Sessions', 'Bounce rate']]
    y = df['Key events']
    return X, y

# Train the model
def train_model(X, y):
    model = LinearRegression()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    return model, X_test, y_test