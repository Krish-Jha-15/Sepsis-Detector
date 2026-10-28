# Sepsis Early Warning System

An end-to-end machine learning system that estimates the risk of sepsis in ICU patients from routinely collected vital signs and laboratory values. A GRU-based sequence model, trained on the PhysioNet/Computing in Cardiology Challenge 2019 dataset, is served through a FastAPI backend that stores each patient's record history and returns a risk score with every prediction. A web frontend is currently in development.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [API Reference](#api-reference)
- [Getting Started](#getting-started)
- [Project Status and Limitations](#project-status-and-limitations)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)
- [References](#references)
- [Author](#author)

## Overview

Sepsis is a life-threatening response to infection, and outcomes depend heavily on how early it is recognised. This project addresses early detection as a prediction problem on hourly ICU data, and deliberately works with the difficulties that make clinical data hard rather than a clean benchmark:

- **Severe class imbalance.** Sepsis-positive hours make up under 2% of all records, and about 7% of patients develop sepsis.
- **Irregular, heavily missing measurements.** Many laboratory values are recorded only a handful of times per stay, and some are almost never recorded.
- **Evaluation that reflects the clinical setting.** Models are compared on area under the precision-recall curve (AUPRC) in addition to ROC-AUC, because accuracy is uninformative at this level of imbalance.

The repository contains the full workflow: raw data ingestion, cleaning, exploratory analysis, feature engineering, baseline and deep learning models, and a REST API that serves the trained model.

## Key Features

- Ingestion of more than 40,000 per-patient `.psv` files into a single SQLite database
- A reproducible, ordered cleaning pipeline: duplicate removal, physiological range validation, missingness indicators, and per-patient forward and backward fill
- Rolling-window features (3 hour and 6 hour mean, minimum, maximum and standard deviation) for seven vital signs
- Baseline models (Logistic Regression, Random Forest, XGBoost) and a GRU sequence model compared on a common patient-level split
- Patient-level train, validation and test splits, stratified by outcome, so no patient appears in more than one partition
- Class imbalance handled through a positively weighted loss, with model selection on validation AUPRC
- FastAPI service with persistent patient history, a fallback strategy for missing inputs, and risk stratification in the response
- Saved inference artifacts (model weights, scaler, feature list, training means) kept separate from training code

## System Architecture

```
  PhysioNet .psv files
          |
          v
  SQLite database  -->  Cleaning  -->  Feature engineering
                                               |
                                               v
                           Baselines (LR, RF, XGBoost)  and  GRU model
                                               |
                                               v
                     saved_models/  (weights, scaler, feature list, means)
                                               |
                                               v
   Frontend (in development)  <-->  FastAPI backend  <-->  SQLite (patient records)
```

At inference time the backend loads the trained artifacts once at startup. For a returning patient, any feature missing from the request is filled from that patient's recent stored history (rolling mean over the last six records); for a new patient, or a feature with no history, the training-set mean is used.

## Repository Structure

```
.
|-- backend/
|   |-- main.py                  Application entry point, CORS and router registration
|   |-- Database_1.py            SQLAlchemy engine, session factory and declarative base
|   |-- PatientRecord_2.py       ORM model for stored patient records
|   |-- Predictor_4.py           Model definition, input preparation, scaling and inference
|   |-- PatientRoutes_5.py       Endpoint to register a new patient and score it
|   |-- PatientRecRoutes_6.py    Endpoint to list all stored records
|   |-- Predict.py               Endpoint to score a new observation for a patient
|   |-- patients.py              Patient summary and per-patient history endpoints
|   |-- id_history.py            History lookup by patient identifier
|   |-- Patient_History_id.py    History retrieval and existence check helpers
|   `-- remove_patient.py        Maintenance endpoint for removing incomplete records
|
|-- model/
|   |-- data_handling/
|   |   |-- raw_data/            Load .psv files into SQLite
|   |   `-- Clean_data/          Cleaning and imputation pipeline
|   |-- EDA/                     Exploratory data analysis
|   |-- Feature_Engineering/     Rolling-window features and inference statistics
|   |-- deep_learning/
|   |   |-- base_model/          Patient-level split and baseline models
|   |   `-- DL.py                GRU training, validation and test evaluation
|   `-- saved_models/            Trained weights, scaler, feature list, training means
|
`-- frontend/                    Web interface (in development)
```

## Dataset

The project uses the training data from the [PhysioNet/Computing in Cardiology Challenge 2019](https://physionet.org/content/challenge-2019/), which provides hourly records from ICU patients across two hospital systems.

| Property | Value |
| --- | --- |
| Patients (training sets A and B) | 40,336 |
| Hourly records (after duplicate removal) | 1,552,210 |
| Patients who develop sepsis | 2,932 (7.3%) |
| Sepsis-positive hourly records | 27,916 (1.8%) |
| Raw variables | 40 clinical and administrative columns plus the sepsis label |

The raw data is not included in this repository. Download it from PhysioNet and place the `.psv` files under `model/data_handling/training/` before running the data pipeline.

## Methodology

### Data preparation

1. **Ingestion.** Each patient file is read and appended to a single SQLite table, with the file name used as the patient identifier.
2. **Deduplication.** Exact duplicate rows are removed.
3. **Range validation.** Values outside physiologically plausible bounds are set to missing rather than carried forward.
4. **Column filtering.** Variables that are missing in 95% or more of records (for example lactate, troponin and fibrinogen) are dropped.
5. **Missingness indicators.** A binary flag is added for each remaining variable that has missing values, so the model can use the fact that a measurement was not taken.
6. **Imputation.** Within each patient, records are ordered by ICU length of stay and filled forward, then backward. Values still missing after that, which belong to patients where a variable was never measured, are filled with the population median.

### Feature engineering

For seven vital signs (heart rate, oxygen saturation, temperature, systolic, mean and diastolic blood pressure, and respiratory rate), rolling mean, minimum, maximum and standard deviation are computed per patient over 3 hour and 6 hour windows. This yields 56 trend features in addition to the base measurements, demographics, ICU unit indicators and missingness flags.

### Modelling

| Model | Notes |
| --- | --- |
| Logistic Regression | Standardised inputs, balanced class weights, decision threshold chosen to reach a target recall |
| Random Forest | 200 trees, maximum depth 10, balanced class weights |
| XGBoost | 300 trees, depth 5, learning rate 0.05, positive-class weighting |
| GRU (final model) | Single-layer GRU with 64 hidden units and a per-time-step output; trained on whole patient sequences with padding and masking |

The GRU is trained with binary cross-entropy using a positive-class weight equal to the ratio of negative to positive records, the Adam optimiser (learning rate 0.001), and gradient clipping. Padded time steps are excluded from the loss. The checkpoint with the best validation AUPRC is saved.

### Evaluation protocol

- Patients are split 70/30 into training and test sets, stratified by whether the patient ever develops sepsis.
- The training portion is split again 80/20 into training and validation sets, using the same stratification.
- Scaling statistics are fitted on training patients only.
- Reported metrics are AUPRC and ROC-AUC, computed over all non-padded time steps.

## API Reference

The service exposes interactive documentation at `/docs` when running.

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Health check |
| POST | `/new_patient?Patient_id={id}` | Register a patient, score the submitted measurements, and store the record. Rejected if the identifier already exists. |
| POST | `/predict?id={id}` | Score a new observation for a patient and store it. Missing features are filled from the patient's stored history when available. |
| GET | `/patients` | Summary of every patient: record count, latest probability, prediction and risk band |
| GET | `/patients/{patient_id}` | Full stored record history for one patient |
| GET | `/id_history/{patient_id}` | Record history with a total count |
| GET | `/patient_record` | All stored records |
| DELETE | `/remove` | Delete records that have no patient identifier |

### Example

```bash
curl -X POST "http://127.0.0.1:8000/new_patient?Patient_id=P-1001" \
  -H "Content-Type: application/json" \
  -d '{"HR": 98, "O2Sat": 94, "Temp": 37.8, "SBP": 112, "MAP": 78, "DBP": 60, "Resp": 22, "Age": 67, "Gender": 1, "ICULOS": 12}'
```

```json
{
  "status": "Success",
  "prediction": {
    "sepsis": false,
    "risk_score": 0.3494,
    "probability": "34.94%",
    "risk_level": "Low"
  },
  "received_data": { "HR": 98, "O2Sat": 94, "...": "..." }
}
```

Feature names in the request body must match the model's input columns. Any feature that is omitted is filled automatically as described under [System Architecture](#system-architecture).

## Getting Started

### Prerequisites

- Python 3.10 or newer
- The trained artifacts in `model/saved_models/` (included in this repository)

### Installation

```bash
git clone <repository-url>
cd <repository-name>

python -m venv venv
source venv/bin/activate       

pip install -r requirements.txt
```

### Run the API

The paths to the saved artifacts are defined at the top of `backend/Predictor_4.py` and must point to the `model/saved_models/` directory on your machine.

```bash
cd backend
uvicorn main:app --reload
```

### Reproduce the model

1. Download the PhysioNet 2019 training data and place the `.psv` files under `model/data_handling/training/`.
2. Run the notebooks in order: `model/data_handling/raw_data`, `model/data_handling/Clean_data`, `model/EDA`, `model/Feature_Engineering`.
3. Run the baseline scripts in `model/deep_learning/base_model/` for comparison.
4. Run `model/deep_learning/DL.py` to train the GRU. Training requires a CUDA-capable GPU.

Database and file paths in the notebooks and scripts are currently absolute and should be edited to match your environment.

## Project Status and Limitations

- The data pipeline, models and backend API are functional. The frontend is under active development.
- The API scores a single time step per request. Temporal context for returning patients comes from the stored history, rather than from feeding the full sequence to the GRU.
- Rolling-window features are expected to be supplied by the client or are otherwise replaced by training means.
- Authentication, input schema validation and automated tests are not yet implemented.
- The model was developed and evaluated on one public dataset and has not been externally validated or calibrated for any specific hospital.

## Roadmap

- Complete the web frontend with a patient dashboard, risk trend charts and an observation entry form
- Validate request payloads with typed schemas
- Compute rolling-window features on the server from stored history
- Score full patient sequences at inference time
- Add probability calibration and report calibration curves
- Add authentication and automated tests
- Containerise the backend and frontend

## Disclaimer

This project is for research and educational purposes only. It is not a medical device, has not been clinically validated, and must not be used to diagnose, treat, or make decisions about real patients.

## References

Reyna, M. A., Josef, C. S., Jeter, R., et al. Early Prediction of Sepsis From Clinical Data: The PhysioNet/Computing in Cardiology Challenge 2019. *Critical Care Medicine*, 48(2), 2020.

## Author

Krish Jha
Integrated B.Tech - M.Tech, Electronics and Communication Engineering
The LNM Institute of Information Technology (LNMIIT), Jaipur