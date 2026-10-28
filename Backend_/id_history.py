from fastapi import APIRouter

from Database_1 import SessionLocal
from PatientRecord_2 import PatientRecord

router = APIRouter()


@router.get("/id_history/{patient_id}")
def get_patient_record(patient_id: str):

    db = SessionLocal()

    try:

        records = (
            db.query(PatientRecord)
            .filter(PatientRecord.Patient_id == patient_id)
            .order_by(PatientRecord.created_at)
            .all()
        )

        if not records:
            return {
                "status": "Patient not found"
            }

        return {
            "Patient_id": patient_id,
            "total_records": len(records),
            "history": records
        }

    finally:
        db.close()