from sqlalchemy import Column,Integer,String,Float,DateTime,JSON
from datetime import datetime

from Database_1 import Base

# from predictor import predict


class PatientRecord(Base):

    __tablename__='patient_records'

    id=Column(Integer,primary_key=True,index=True)
    Patient_id=Column(String,nullable=False,index=True)
    Patient_data=Column(JSON,nullable=True)
    prediction=Column(Integer,nullable=False)
    probability=Column(Float,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    