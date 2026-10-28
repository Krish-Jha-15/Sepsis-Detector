import torch
from model.saved_models import dl_best_model

model=dl_best_model()

def predict(patient):
    features = [[
        patient.age,
        patient.heart_rate,
        patient.temperature,
        patient.wbc
    ]]

    model.eval()

    output=torch.sigmoid(model(features))
    
    return output


predict(
    age=10,
    heart_rate=75,
    temperature=40,
    wbc=100
)
