from typing import Dict,Any
from fastapi import APIRouter

from Database_1 import SessionLocal
from Patient_History_id import check,get_patient_history
from Predictor_4 import predict
from PatientRecord_2 import PatientRecord

route=APIRouter()
@route.post("/predict")
def pred(Patient_Data: Dict[str, Any], id: int):

    print("Step 1")

    db = SessionLocal()

    try:
        print("Step 2")

        available = check(db, id)

        print("Available:", available)

        print("Step 3")

        result = predict(db, Patient_Data, available, id)

        print(result)

        print("Step 4")

        record = PatientRecord(
            Patient_id=str(id),
            Patient_data=Patient_Data,
            prediction=result["prediction"],
            probability=result["probability"]
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        print("Step 5")

        return result

    finally:
        db.close()