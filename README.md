# Water Quality Prediction API

This project implements a Machine Learning solution to classify water quality based on physicochemical properties. It includes a full pipeline from Exploratory Data Analysis (EDA) and model training to a containerized REST API deployed with Docker.

---

##  Project Overview

* **Goal:** Predict the quality class of water samples (e.g., 0, 1, 2) based on input features like pH, Turbidity, Dissolved Oxygen, etc.
* **Dataset:** `WQD.xlsx - Final_Data.csv`
* **Model:** Random Forest Classifier (Hyperparameter tuned via GridSearch)
* **Deployment:** Flask API containerized with Docker.

---

## 📂 Project Structure
### Project Structure

```text
.
├── WQD.xlsx - Final_Data.csv
├── water_quality_model.ipynb
├── app.py
├── Dockerfile
├── requirements.txt
├── water_quality_model.pkl
├── scaler.pkl
└── model_columns.pkl
```
---

##  Prerequisites

* **Docker Desktop** (Running)
* **Python 3.9+** (Optional, for local development without Docker)

---

## Quick Start (Docker)

The easiest way to run this `application` is using `Docker`.

### 1. Build the Docker Image

Open your terminal in the project directory and run:

```bash
docker build -t water-quality-api .
```
### 2. Run the Container
Start the API on port 5000:

```bash
docker run -p 5000:5000 -d --name water-api water-quality-api
```
### 3. Test the API

Send a POST request to the prediction endpoint.

Using cURL (`Bash/Mac/Linux`):
```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{
    "Temp": 67.4,
    "Turbidity (cm)": 10.1,
    "DO(mg/L)": 0.2,
    "BOD (mg/L)": 7.4,
    "CO2": 10.1,
    "pH": 4.7,
    "Alkalinity (mg L-1 )": 218.3,
    "Hardness (mg L-1 )": 300.1,
    "Calcium (mg L-1 )": 337.1,
    "Ammonia (mg L-1 )": 0.2,
    "Nitrite (mg L-1 )": 4.3,
    "Phosphorus (mg L-1 )": 0.005,
    "H2S (mg L-1 )": 0.06,
    "Plankton (No. L-1)": 6069.6
}'
```
Using cURL (`Windows PowerShell`):
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"Temp": 67.4, "Turbidity (cm)": 10.1, "DO(mg/L)": 0.2, "BOD (mg/L)": 7.4, "CO2": 10.1, "pH": 4.7, "Alkalinity (mg L-1 )": 218.3, "Hardness (mg L-1 )": 300.1, "Calcium (mg L-1 )": 337.1, "Ammonia (mg L-1 )": 0.2, "Nitrite (mg L-1 )": 4.3, "Phosphorus (mg L-1 )": 0.005, "H2S (mg L-1 )": 0.06, "Plankton (No. L-1)": 6069.6}'
```

---


## Model Development Details
The water_quality_model.ipynb notebook covers the training process:

- **Data Cleaning**: Renamed columns (e.g., fixed pH typo), handled missing values with Median Imputation.

- **EDA**: Analyzed correlations and distributions.

- **Preprocessing**: Applied Standard Scaling to normalize features.

- **Model Selection**: Compared `Logistic Regression`, `Random Forest`, and `Gradient Boosting`.

- **Tuning**: Utilized `GridSearchCV` to optimize Random Forest hyperparameters.

- **Export**: Serialized the best model and scalers using joblib.

---

## Troubleshooting

### Docker Build Fails on Network:
If the build fails due to "ReadTimeout" or "Hash Mismatch", simply run the `docker build` command again. The `Dockerfile` is optimized to cache progress, so it will resume where it left off.

### File Not Found (`Dockerfile`):
Ensure your `Dockerfile` is named exactly `Dockerfile` with no file extension (e.g., it should not be `Dockerfile.txt`).