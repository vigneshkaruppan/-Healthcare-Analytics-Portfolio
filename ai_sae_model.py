import pyodbc
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LENOVO\SQLEXPRESS;"
    "DATABASE=ClinicalTrialDB;"
    "Trusted_Connection=yes;"
)
df = pd.read_sql("SELECT * FROM AI_Prediction", conn)

conn.close()
print(df.head(10))
 
df["Gender"] = df["Gender"].map({
    "Male":0,
    "Female":1
})

df["LabStatus"] = df["LabStatus"].map({
    "Normal":0,
    "Abnormal":1,
    "Critical":2
})
X = df[
    [
        "Age",
        "Gender",
        "MissedVisits",
        "CompletedVisits",
        "AECount",
        "MedicationCount",
        "LabStatus"
    ]
]

y = df["SAERisk"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
model = LogisticRegression()

model.fit(X_train, y_train)
pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("SAE Model Accuracy:", accuracy)

print(classification_report(y_test, pred))

print(confusion_matrix(y_test, pred))
new_patient = [[
    58,
    1,
    5,
    2,
    3,
    5,
    2
]]

prediction = model.predict(new_patient)

probability = model.predict_proba(new_patient)

print("SAE Prediction:", prediction)

print("SAE Probability:", probability)

import joblib

joblib.dump(model, "sae_model.pkl")

print("sae_model.pkl created successfully!")
