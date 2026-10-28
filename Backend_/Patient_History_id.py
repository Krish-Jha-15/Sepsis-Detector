import pandas as pd

from PatientRecord_2 import PatientRecord


def get_patient_history(db, patient_id):

    records = (
        db.query(PatientRecord)
        .filter(PatientRecord.Patient_id == str(patient_id))
        .order_by(PatientRecord.created_at)
        .all()
    )

    if not records:
        return None

    history = pd.DataFrame([
        record.Patient_data
        for record in records
    ])

    return history


def check(db, patient_id):

    patient = (
        db.query(PatientRecord)
        .filter(PatientRecord.Patient_id == str(patient_id))
        .first()
    )

    return patient is not None