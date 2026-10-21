import pyodbc
import pandas as pd

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LENOVO\ SQLEXPRESS;"
    "DATABASE=HospitalOperationsDB;"
    "Trusted_Connection=yes;"
)

print("✅ Connected to SQL Server successfully!")

query = "SELECT * FROM Patients"

patients_df = pd.read_sql(query, conn)

print(patients_df.head(10))
print("\nDataset Information:")
print(patients_df.info())

print("\nSummary Statistics:")
print(patients_df.describe(include="all"))
dept_summary = patients_df.groupby("Department").size()

print("\nPatients by Department:")
print(dept_summary)

import matplotlib.pyplot as plt
total_patients = len(patients_df)
print("Total Patients:", total_patients)
dept_counts = patients_df["Department"].value_counts()

print(dept_counts)
dept_counts.plot(kind="bar")

plt.title("Patients by Department")
plt.xlabel("Department")
plt.ylabel("Number of Patients")

plt.tight_layout()
plt.show()
gender_counts = patients_df["Gender"].value_counts()

gender_counts.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Gender Distribution")
plt.ylabel("")
plt.show()
admission_counts = patients_df["AdmissionType"].value_counts()

print(admission_counts)

admission_counts.plot(kind="bar")

plt.title("Admission Type")
plt.xlabel("Type")
plt.ylabel("Patients")

plt.tight_layout()
plt.show()
doctor_counts = patients_df["Doctor"].value_counts()

print(doctor_counts)

doctor_counts.plot(kind="bar")

plt.title("Doctor Workload")
plt.xlabel("Doctor")
plt.ylabel("Patients")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
patients_df.to_excel(
    "Hospital_Clean_Data.xlsx",
    index=False
)

print("Hospital_Clean_Data.xlsx exported successfully!")
import pandas as pd
import matplotlib.pyplot as plt
total_patients = len(patients_df)

opd_patients = (patients_df["AdmissionType"] == "OPD").sum()

ipd_patients = (patients_df["AdmissionType"] == "IPD").sum()

emergency_patients = (patients_df["AdmissionType"] == "Emergency").sum()

print(f"Total Patients: {total_patients}")
print(f"OPD Patients: {opd_patients}")
print(f"IPD Patients: {ipd_patients}")
print(f"Emergency Patients: {emergency_patients}")
patients_df["AdmissionDate"] = pd.to_datetime(patients_df["AdmissionDate"])
patients_df["DischargeDate"] = pd.to_datetime(patients_df["DischargeDate"])

patients_df["LengthOfStay"] = (
    patients_df["DischargeDate"] - patients_df["AdmissionDate"]
).dt.days

print(patients_df[["PatientName", "LengthOfStay"]])
alos = patients_df["LengthOfStay"].mean()

print(f"Average Length of Stay: {alos:.2f} days")
dept_alos = patients_df.groupby("Department")["LengthOfStay"].mean()

print(dept_alos)

dept_alos.plot(kind="bar")

plt.title("Average Length of Stay by Department")
plt.xlabel("Department")
plt.ylabel("Days")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
patients_df.to_excel("Hospital_Dashboard_Data.xlsx", index=False)

print("Dashboard data exported successfully!")