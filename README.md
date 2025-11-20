# 🐟 Water Quality Prediction API

A machine learning–powered REST API for predicting **water quality classes** using physicochemical parameters.
This project includes the **full pipeline**: data exploration, model training, serialization, and a fully containerized Flask API deployed using Docker and Render.

---

## Project Overview

* **Objective:** Predict water quality class (0, 1, or 2) from water physicochemical properties such as pH, turbidity, dissolved oxygen, etc.
* **Dataset:** `WQD.xlsx - Final_Data.csv`
* **Model:** Random Forest Classifier (optimized using GridSearchCV)
* **Deployment:** Flask API + Docker + Render cloud hosting

---

## 📁 Project Structure

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

## Prerequisites

* **Docker Desktop** (required to run the API container)
* **Python 3.9+** (optional if running locally without Docker)

---

## Quick Start with Docker

Running this API is easiest using Docker.

### 1. Build the Docker Image

```bash
docker build -t water-quality-api .
```

### 2. Run the Container

Expose API on port **5000**:

```bash
docker run -p 5000:5000 -d --name water-api water-quality-api
```

### 3. Test the API (Local)

**Using cURL (Mac/Linux):**

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

**Using PowerShell (Windows):**

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"Temp\": 67.4, \"Turbidity (cm)\": 10.1, \"DO(mg/L)\": 0.2, \"BOD (mg/L)\": 7.4, \"CO2\": 10.1, \"pH\": 4.7, \"Alkalinity (mg L-1 )\": 218.3, \"Hardness (mg L-1 )\": 300.1, \"Calcium (mg L-1 )\": 337.1, \"Ammonia (mg L-1 )\": 0.2, \"Nitrite (mg L-1 )\": 4.3, \"Phosphorus (mg L-1 )\": 0.005, \"H2S (mg L-1 )\": 0.06, \"Plankton (No. L-1)\": 6069.6}"
```

---

## Cloud Deployment (Render)

This API is deployed on **Render.com** and publicly accessible.

---

### 1. Push Your Project to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
```

---

### 2. Deploy via Render Dashboard

1. Visit **Render.com**
2. Click **New + → Web Service**
3. Connect your GitHub repo
4. **Runtime:** Docker
5. **Instance Type:** Free (or upgrade for performance)
6. Click **Create Web Service**

Render will automatically build and deploy your Dockerized API.

---

### 3. Test the Live API

```bash
curl -X POST https://catfish-water-quality-prediction.onrender.com/predict \
-H "Content-Type: application/json" \
-d '{"Temp": 67.4, "Turbidity (cm)": 10.1, "DO(mg/L)": 0.2, "BOD (mg/L)": 7.4, "CO2": 10.1, "pH": 4.7, "Alkalinity (mg L-1 )": 218.3, "Hardness (mg L-1 )": 300.1, "Calcium (mg L-1 )": 337.1, "Ammonia (mg L-1 )": 0.2, "Nitrite (mg L-1 )": 4.3, "Phosphorus (mg L-1 )": 0.005, "H2S (mg L-1 )": 0.06, "Plankton (No. L-1)": 6069.6}'
```

---

## Model Development Summary

The notebook (`water_quality_model.ipynb`) documents the complete workflow:

### 🔧 Data Preparation

* Cleaned and renamed inconsistent columns
* Used **Median Imputation** for missing values

### 📊 Exploratory Data Analysis

* Distribution inspection
* Correlation heatmaps
* Outlier checks

### 🏗️ Preprocessing

* StandardScaler applied to numeric features
* Stored `model_columns.pkl` for strict feature order

### 🤖 Model Training

Models evaluated:

* Logistic Regression
* Gradient Boosting
* **Random Forest (best performance)**

### 🔍 Hyperparameter Tuning

Used **GridSearchCV** to optimize:

* n_estimators
* max_depth
* min_samples_split

### 🗂️ Serialization

Exported:

* `water_quality_model.pkl`
* `scaler.pkl`
* `model_columns.pkl`

---

##  Troubleshooting

### ❗ Docker Build Network Errors

If you see:

* `ReadTimeout`
* `Hash mismatch`
* `Connection reset`

Simply rerun:

```bash
docker build -t water-quality-api .
```

Docker caching will resume the build from the last successful layer.

---

### ❗ “Dockerfile Not Found”

Ensure the file is named exactly:

```
Dockerfile
```

**Not**:

```
Dockerfile.txt
Dockerfile.docx
```

---
