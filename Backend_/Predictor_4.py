import joblib
import torch
import torch.nn as nn
import numpy as np
import pandas as pd

from Database_1 import SessionLocal
from PatientRecord_2 import PatientRecord
from Patient_History_id import get_patient_history

FEATUREs=joblib.load(r"C:\Users\KRISH JHA\OneDrive\Desktop\Sepsis\model\saved_models\feature_columns.pkl")
SCALE=joblib.load(r"C:\Users\KRISH JHA\OneDrive\Desktop\Sepsis\model\saved_models\scaler.pkl")
FEATURE_MEAN=joblib.load(r'C:\Users\KRISH JHA\OneDrive\Desktop\Sepsis\model\saved_models\avg_columns.pkl')
# torch.load(r'C:\Users\KRISH JHA\OneDrive\Desktop\Sepsis\model\saved_models\dl_best_model.pth')

class SepsisGRU(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers, dropout=0.0):
        super().__init__()

        self.GRU = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )

        self.output = nn.Linear(hidden_size, 1)

    def forward(self, x):

        gru_output, _ = self.GRU(x)

        logits = self.output(gru_output).squeeze(-1)

        return logits

def prepare_input_new(patient_data: dict):

    processed_data=[]
    for feature in FEATUREs:

        if feature in patient_data:
            processed_data.append(patient_data[feature])

        else:
            processed_data.append(FEATURE_MEAN[feature]) 

    return processed_data

def prepare_input_existing(db,patient_data,id):
    
    history=get_patient_history(db,id)
    processed_data=[]
    for feature in FEATUREs:

        if feature in patient_data:
            processed_data.append(patient_data[feature])
            # print("-> Input")
        elif feature in history.columns:
            
            
            value = (
                history[feature]
                .rolling(window=6, min_periods=1)
                .mean()
                .iloc[-1]
            )
            # print("-> History")
            if pd.isna(value):
                value = FEATURE_MEAN[feature]
            processed_data.append(value)

        else:
            print("-> Mean")
            processed_data.append(FEATURE_MEAN[feature])
    
    return processed_data

def scale_input(processed_data):

    data=pd.DataFrame(
        [processed_data],
        columns=FEATUREs
    )
    print("========== DATA BEFORE SCALING ==========")
    print(data)

    print("========== DATA TYPES ==========")
    print(data.dtypes)

    print("========== EMPTY STRING COLUMNS ==========")
    print(data.columns[data.eq("").any()].tolist())
    scaled_data = SCALE.transform(data)

    return scaled_data

def to_tensor(scaled_data):

    tensor = torch.tensor(
        scaled_data,
        dtype=torch.float32
    )

    tensor = tensor.unsqueeze(1)

    return tensor

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = SepsisGRU(
    input_size=len(FEATUREs),
    hidden_size=64,
    num_layers=1
).to(device)

model.load_state_dict(
    torch.load(
        r"C:\Users\KRISH JHA\OneDrive\Desktop\Sepsis\model\saved_models\dl_best_model.pth",
        map_location=device
    )
)

model.eval()

def predict(db, patient_data, available, patient_id):

    if available:
        
        processed = prepare_input_existing(
            db,
            patient_data,
            patient_id
        )

    else:
        processed = prepare_input_new(patient_data)

    scaled = scale_input(processed)

    tensor = to_tensor(scaled).to(device)

    with torch.no_grad():

        logits = model(tensor)

        risk = torch.sigmoid(logits)[0, -1].item()

    return {
        "prediction": int(risk >= 0.5),
        "risk_score": round(risk,4),
        "probability": round(risk*100,2)
    }


def new_predict(patient_data):

    processed = prepare_input_new(patient_data)

    scaled = scale_input(processed)

    tensor = to_tensor(scaled).to(device)

    with torch.no_grad():

        logits = model(tensor)

        risk = torch.sigmoid(logits)[0, -1].item()

    return {
        "prediction": int(risk >= 0.5),
        "risk_score": round(risk,4),
        "probability": round(risk*100,2)
    }

