import sqlite3
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split


conn=sqlite3.connect(r'C:\Users\KRISH JHA\OneDrive\Desktop\Sepsis\data_handling\sepsis.db')

cursor=conn.cursor()

print("Database is Connected")

feature_table=pd.read_sql_query("""
select * from feature_table
""",conn)

patient_outcome=feature_table.groupby('Patient_id')['SepsisLabel'].max().reset_index()

train_patients,test_patients=train_test_split(
    patient_outcome,
    test_size=0.3,
    random_state=42,
    stratify=patient_outcome['SepsisLabel']
)

print("Train patients:")
print(train_patients.head())

print("\nTest patients:")
print(test_patients.head())

train_ids=train_patients['Patient_id']
test_ids=test_patients['Patient_id']

train_data=feature_table[feature_table['Patient_id'].isin(train_ids)]
test_data=feature_table[feature_table['Patient_id'].isin(test_ids)]

drop_columns = [
    "Patient_id",
    "SepsisLabel",
    "Dataset"
]

feature_columns = [
    col for col in train_data.columns
    if col not in drop_columns
]

X_train = train_data[feature_columns].copy()
y_train = train_data["SepsisLabel"].copy()

X_test = test_data[feature_columns].copy()
y_test = test_data["SepsisLabel"].copy()

print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("X_test:", X_test.shape)
print("y_test:", y_test.shape)

