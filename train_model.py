import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# AQUAGUARD AI - DEMONSTRATION MODEL
# Uses synthetic data, not real farm measurements.


def generate_demo_data(number_of_samples=2000):
    np.random.seed(42)

    ph = np.random.uniform(4.5, 10.0, number_of_samples)
    temperature = np.random.uniform(15, 38, number_of_samples)
    oxygen = np.random.uniform(1, 12, number_of_samples)
    ammonia = np.random.uniform(0, 3, number_of_samples)

    data = pd.DataFrame({
        "ph": ph,
        "temperature": temperature,
        "oxygen": oxygen,
        "ammonia": ammonia
    })

    # Illustrative rules for generating demonstration labels.
    risk_score = (
        (np.abs(ph - 7.5) > 1.0).astype(int)
        + ((temperature < 20) | (temperature > 32)).astype(int)
        + (oxygen < 5).astype(int)
        + (ammonia > 0.5).astype(int)
    )

    labels = np.where(
        risk_score >= 3,
        "High Risk",
        np.where(risk_score >= 1, "Medium Risk", "Low Risk")
    )

    return data, labels


def main():
    print("Generating demonstration dataset...")

    data, labels = generate_demo_data()

    X_train, X_test, y_train, y_test = train_test_split(
        data,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    print("Training Random Forest model...")

    model = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced"
        )
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Demonstration test accuracy: {accuracy:.2%}")

    # Save the trained model.
    joblib.dump(model, "aquaguard_model.pkl")

    print("Model saved successfully: aquaguard_model.pkl")
    print("Training completed successfully.")


if __name__ == "__main__":
    main()



