from fastapi import APIRouter
from Database_1 import SessionLocal
from PatientRecord_2 import PatientRecord

router = APIRouter()

@router.delete("/remove")
def remove_null_patients():

    db = SessionLocal()

    try:
        deleted = (
            db.query(PatientRecord)
            .filter(PatientRecord.Patient_id == None)
            .delete(synchronize_session=False)
        )

        db.commit()

        return {
            "deleted_records": deleted
        }

    finally:
        db.close()