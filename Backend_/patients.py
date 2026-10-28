from fastapi import APIRouter
from sqlalchemy import func

from Database_1 import SessionLocal
from PatientRecord_2 import PatientRecord

router = APIRouter()


@router.get("/patients")
def get_patients():

    db = SessionLocal()

    try:
        patient_ids = (
            db.query(PatientRecord.Patient_id)
            .filter(PatientRecord.Patient_id.isnot(None))
            .distinct()
            .all()
        )

        result = []
        for (patient_id,) in patient_ids:

            records = (
                db.query(PatientRecord)
                .filter(PatientRecord.Patient_id == patient_id)
                .order_by(PatientRecord.created_at.desc())
                .all()
            )

            latest = records[0]
            if latest.probability <45:
                risk="LOW"

            elif latest.probability>45 and latest.probability<70:
                risk='MEDIUM'

            else:
                risk='HIGH'
            
            result.append({
                "Patient_id": patient_id,
                "total_records": len(records),
                "latest_probability": latest.probability,
                "latest_prediction": latest.prediction,
                "Risk":risk,
                "last_updated": latest.created_at
            })
            

        return result

    finally:
        db.close()

@router.get("/patients/{patient_id}")
def patient_history(patient_id: str):

    db = SessionLocal()

    try:

        records = (
            db.query(PatientRecord)
            .filter(PatientRecord.Patient_id == patient_id)
            .order_by(PatientRecord.created_at)
            .all()
        )

        return records

    finally:
        db.close()