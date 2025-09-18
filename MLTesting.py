import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

#AHHHHH

# Load Data
def load_data(file_path):
    """Load dataset from CSV file."""
    data = pd.read_csv(file_path)
    return data


# Preprocess Data
def preprocess_data(data):
    """Split dataset into features and targets."""
    # Features (X) and targets (y)
    X = data[['diameter', 'pitch', 'rpm', 'velocity']]
    y = data[['thrust', 'torque']]

    # Add domain-specific features
    X['rpm_squared'] = X['rpm'] ** 2
    X['diameter_pow4'] = X['diameter'] ** 4
    X['rpm_diameter_interaction'] = X['rpm'] * X['diameter']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


# Train Model
def train_model(X_train, y_train):
    """Train Random Forest model."""
    rf_model = RandomForestRegressor(random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    return rf_model


# Evaluate Model
def evaluate_model(model, X_test, y_test):
    """Evaluate model performance."""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Plot actual vs predicted thrust
    plt.scatter(y_test['thrust'], y_pred[:, 0], label='Thrust', alpha=0.5)
    plt.plot([y_test.min().min(), y_test.max().max()], [y_test.min().min(), y_test.max().max()], 'r--')
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.legend()
    plt.show()

    return mse, r2


# Save Model
def save_model(model, file_name):
    """Save the trained model to a file."""
    joblib.dump(model, file_name)
    print(f"Model saved to {file_name}")


# Load Model
def load_model(file_name):
    """Load a trained model from a file."""
    model = joblib.load(file_name)
    print(f"Model loaded from {file_name}")
    return model


# Predict with Hybrid Approach
def make_prediction(model, new_data, feature_names):
    """Make predictions with the trained model."""
    # Ensure new_data is a DataFrame with correct feature names
    new_data_df = pd.DataFrame(new_data, columns=feature_names)

    # Add domain-specific features
    new_data_df['rpm_squared'] = new_data_df['rpm'] ** 2
    new_data_df['diameter_pow4'] = new_data_df['diameter'] ** 4
    new_data_df['rpm_diameter_interaction'] = new_data_df['rpm'] * new_data_df['diameter']

    # Predict using Random Forest
    predictions = model.predict(new_data_df)

    # Apply physics-based constraints for extrapolation
    for i in range(len(predictions)):
        diameter = new_data_df.iloc[i]['diameter']
        rpm = new_data_df.iloc[i]['rpm']
        velocity = new_data_df.iloc[i]['velocity']

        # Example constraint: Thrust should not increase with velocity beyond a certain point
        if velocity > 20:  # Adjust this threshold based on your domain knowledge
            predictions[i, 0] = predictions[i, 0] * (20 / velocity)  # Reduce thrust as velocity increases

    return predictions


# Main Function
def main():
    retrain = True
    if retrain:
        # File path to your CSV
        file_path = 'all_props_data.csv'

        # Step 1: Load and preprocess data
        data = load_data(file_path)
        X_train, X_test, y_train, y_test = preprocess_data(data)

        # Step 2: Train the model
        rf_model = train_model(X_train, y_train)

        # Step 3: Evaluate the model
        evaluate_model(rf_model, X_test, y_test)

        # Step 4: Save the model
        save_model(rf_model, 'random_forest_model.pkl')

    # Step 5: Load the model (example)
    loaded_model = load_model('random_forest_model.pkl')

    # Step 6: Make predictions (example)
    # Example new data (diameter, pitch, rpm, velocity)
    for i in range(0, 30, 1):
        new_data = [[28, 9.2, 3000, i]]
        feature_names = ['diameter', 'pitch', 'rpm', 'velocity']
        predictions = make_prediction(loaded_model, new_data, feature_names)
        print(f"Predicted Thrust and Torque: {predictions}")


if __name__ == "__main__":
    main()