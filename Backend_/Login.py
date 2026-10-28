from sqlalchemy import Column,Integer,String,Float,DateTime,JSON
from datetime import datetime

from Database_1 import Base

# from predictor import predict


class LoginDB(Base):

    __tablename__='Login_Detail'

    id=Column(Integer,primary_key=True,index=True)
    name=Column(str,nullable=False)
    email=Column(email,nullable=False)
    # password=Column
    created_at = Column(DateTime, default=datetime.utcnow)

    