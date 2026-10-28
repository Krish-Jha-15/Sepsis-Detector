from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Database_1 import Base, engine
from PatientRoutes_5 import router
from PatientRecRoutes_6 import router as patient_route
from id_history import router as id_history
from Predict import route as predict
from patients import router as patient
from remove_patient import router as remove

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sepsis Prediction API"
)

origins=[    "http://localhost:5173",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(patient_route)
app.include_router(id_history)
app.include_router(predict)
app.include_router(patient)
app.include_router(remove)


@app.get("/")
def home():
    return {
        "message": "Backend Running"
    }