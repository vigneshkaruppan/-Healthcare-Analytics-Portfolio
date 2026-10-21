import pyodbc
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LENOVO\ SQLEXPRESS;"
    "DATABASE=ClinicalTrialDB;"
    "Trusted_Connection=yes;"
)
query = "SELECT * FROM AI_Prediction"
df = pd.read_sql(query, conn)

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

y = df["DropoutRisk"]
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

print("Accuracy:", accuracy)

print(classification_report(y_test, pred))
new_patient = [[
    55,
    1,
    5,
    2,
    3,
    4,
    2
]]

prediction = model.predict(new_patient)

probability = model.predict_proba(new_patient)

print("Prediction:", prediction)

print("Probability:", probability)

import joblib
joblib.dump(model, "dropout_model.pkl")
print("dropout_model.pkl created successfully!")