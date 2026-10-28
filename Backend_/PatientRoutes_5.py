from fastapi import APIRouter
from typing import Dict,Any

from Predictor_4 import new_predict
from Database_1 import SessionLocal
from PatientRecord_2 import PatientRecord
from Patient_History_id import check

router=APIRouter()

@router.post('/new_patient')
def new_patient(patient_data:Dict[str,Any],Patient_id:str):

    db=SessionLocal()

    try:
        
        available=check(db,Patient_id)
        
        print("Patient ID:", Patient_id)
        print("Available:", available)
        if(available):
            return {
        "status": "Failed",
        "reason": "Id already Existed",
        "received_data": patient_data
    }
        result=new_predict(patient_data)
        
        record = PatientRecord(
            Patient_id=patient_data.get("id"),
            Patient_data=patient_data,
            prediction=result["prediction"],
            probability=result["probability"]
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
        "status": "Success",
        "prediction": {
            "sepsis": bool(result["prediction"]),
            "risk_score": result["risk_score"],
            "probability": f"{result['probability']}%",
            "risk_level": (
                "High"
                if result["risk_score"] >= 0.70
                else "Medium"
                if result["risk_score"] >= 0.50
                else "Low"
            )
        },
        "received_data": patient_data
    }
    
    finally:
        db.close()