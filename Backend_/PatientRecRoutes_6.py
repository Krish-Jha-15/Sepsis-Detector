from fastapi import APIRouter

from Database_1 import SessionLocal

from PatientRecord_2 import PatientRecord

router=APIRouter()

@router.get("/patient_record")
def get_patient_record():

    db=SessionLocal()

    try:
        record=db.query(PatientRecord).all()
        return record
    
    finally:

        db.close()