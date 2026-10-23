import numpy as np
import pandas as pd
import joblib


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


EDUCATIONAL DEMONSTRATION DATA ONLY


These examples are generated from illustrative rules.


They are NOT real farm measurements or validated labels.


np.random.seed(42)


number_of_samples = 2000


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


Illustrative labels, not scientifically validated predictions.


risk_scores = (
(np.abs(ph - 7.5) > 1.0).astype(int)
+ ((temperature < 20) | (temperature > 32)).astype(int)
+ (oxygen < 5).astype(int)
+ (ammonia > 0.5).astype(int)
)


def assign_risk(score):
if score >= 3:
return "High Risk"
elif score >= 1:
return "Medium Risk"
return "Low Risk"


labels = risk_scores.apply(assign_risk)


X_train, X_test, y_train, y_test = train_test_split(
data,
labels,
test_size=0.2,
random_state=42,
stratify=labels
)


model = make_pipeline(
StandardScaler(),
RandomForestClassifier(
n_estimators=150,
random_state=42,
class_weight="balanced"
)
)


model.fit(X_train, y_train)


predictions = model.predict(X_test)


print("Model training completed.")
print("Accuracy:", round(accuracy_score(y_test, predictions), 3))
print(classification_report(y_test, predictions))


joblib.dump(model, "aquaguard_model.pkl")


print("Saved model as aquaguard_model.pkl")


