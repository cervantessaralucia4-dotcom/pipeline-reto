````md
# 🏥 Healthcare ETL & AI Platform

Full Stack Healthcare Analytics Platform built with:

- Django REST Framework
- React
- PostgreSQL
- Machine Learning
- Random Forest
- JWT Authentication
- ETL Pipeline

---

# 📌 Project Overview

This project was developed as a complete healthcare analytics solution capable of:

- Processing clinical datasets
- Cleaning and transforming healthcare data
- Storing information in PostgreSQL
- Exposing REST APIs
- Visualizing KPIs and analytics
- Predicting disease risk using Artificial Intelligence
- Protecting endpoints with JWT authentication

---

# 🚀 Main Features

## ✅ ETL Pipeline

Implemented complete ETL processing:

### Extraction
- Excel dataset loading
- CSV generation

### Transformation
- Duplicate removal
- Null handling
- Text normalization
- Feature engineering
- Risk calculation
- Data standardization

### Load
- PostgreSQL integration
- Clean dataset export

---

# 🤖 Machine Learning

Random Forest model implemented for disease risk prediction.

## Clinical Variables Used

- Edad
- IMC
- Glucosa
- Colesterol
- Presión sistólica
- Frecuencia cardíaca

## Predictions

The AI predicts:

- Bajo
- Medio
- Alto
- Crítico

## Metrics Implemented

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

# 🔐 JWT Authentication

Authentication implemented using:

```bash
djangorestframework-simplejwt
```

Features:

- Login endpoint
- JWT tokens
- Protected routes
- Session management
- Role-ready architecture

---

# 📊 Dashboard & Analytics

React dashboard includes:

- KPIs
- Patient analytics
- AI prediction form
- Charts
- Risk distribution
- Critical alerts
- Protected dashboard
- JWT authentication

---

# 🧠 AI Prediction System

The platform includes real-time AI predictions using a trained Random Forest model.

## AI Workflow

```text
User Input → React → Django API → ML Model → Prediction
```

---

# 🛠️ Technologies

## Backend

- Python
- Django
- Django REST Framework
- PostgreSQL

## Frontend

- React
- Axios
- Chart.js

## Data Engineering & AI

- Pandas
- NumPy
- Scikit-learn
- Joblib

## Security

- JWT Authentication

---

# 🗄️ Database

Database engine:

```text
PostgreSQL
```

Main table:

```text
Patients
```

---

# 📂 Project Structure

```bash
pipeline-reto/
│
├── backend/
├── frontend/
├── patients/
├── etl/
├── ml/
├── datasets/
├── manage.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Environment Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/cervantessaralucia4-dotcom/pipeline-reto.git
```

---

## 2️⃣ Enter Project

```bash
cd pipeline-reto
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 4️⃣ Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

## Install all requirements

```bash
pip install -r requirements.txt
```

## Main Libraries

```bash
pip install django
pip install djangorestframework
pip install psycopg2-binary
pip install pandas
pip install numpy
pip install scikit-learn
pip install joblib
pip install python-dotenv
pip install djangorestframework-simplejwt
```

---

# 🗄️ PostgreSQL Configuration

## Create database

```sql
CREATE DATABASE healthcare_db;
```

---

## Update backend/settings.py

Configure:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'healthcare_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

# ▶️ Run Backend

## Apply migrations

```bash
python manage.py migrate
```

---

## Create admin user

```bash
python manage.py createsuperuser
```

---

## Run Django server

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000/
```

---

# ▶️ Run Frontend

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run React:

```bash
npm start
```

Frontend:

```text
http://localhost:3000/
```

---

# 🔄 ETL Execution

Run ETL pipeline:

```bash
python etl/etl_process.py
```

Features:

- Cleans dataset
- Removes duplicates
- Handles null values
- Generates clean dataset

---

# 🤖 Train Machine Learning Model

```bash
python ml/train_model.py
```

Generated model:

```text
ml/risk_model.pkl
```

---

# 🔥 API Endpoints

## Authentication

| Endpoint | Method | Description |
|---|---|---|
| /api/token/ | POST | JWT Login |
| /api/token/refresh/ | POST | Refresh Token |

---

## Patients

| Endpoint | Method | Description |
|---|---|---|
| /api/patients/ | GET | List patients |
| /api/patients/ | POST | Create patient |

---

## AI Prediction

| Endpoint | Method | Description |
|---|---|---|
| /api/predict/ | POST | Predict disease risk |

---

## Dashboard APIs

| Endpoint | Method | Description |
|---|---|---|
| /api/dashboard/kpis/ | GET | Dashboard KPIs |
| /api/dashboard/charts/ | GET | Charts data |

---

## Reports

| Endpoint | Method | Description |
|---|---|---|
| /api/reportes/ | GET | Analytics reports |

---

## ETL

| Endpoint | Method | Description |
|---|---|---|
| /api/etl/run/ | POST | Execute ETL |

---

# 🔐 Protected APIs

Protected endpoints require:

```bash
Authorization: Bearer TOKEN
```

---

# 📈 KPIs Implemented

- Total patients
- Critical patients
- High risk patients
- Average glucose
- Average BMI
- Risk distribution

---

# 🔥 Current Project Status

## ✅ Completed

- ETL Pipeline
- PostgreSQL Integration
- Django REST APIs
- React Dashboard
- Machine Learning
- Random Forest
- JWT Authentication
- Protected Routes
- AI Prediction
- Analytics APIs
- Reports APIs
- ETL API

---

# 🚀 Future Improvements

- Docker
- Deployment
- Role permissions
- Advanced analytics
- Real-time monitoring
- CI/CD pipelines

---

# 👨‍💻 Author

Sara Cervantes

---

# 📄 License

Educational & Portfolio Project
````
