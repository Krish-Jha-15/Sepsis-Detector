from fastapi import APIRouter

from Patient_History_id import get_patient_history
from Database_1 import SessionLocal

rotue=APIRouter()
@rotue.get('/current_status')
def current_status(id:int):
    db=SessionLocal()
    history=get_patient_history(db,id)

    