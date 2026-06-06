# 🏥 Plataforma Inteligente de Analítica Clínica
### HealthAnalytics IPS — Reto Técnico FullStack + Data Analytics + ETL + Machine Learning

> Plataforma web capaz de procesar datos clínicos mediante procesos ETL, analítica estadística
> y modelos de Machine Learning para la detección de riesgo médico.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Tecnologías](#tecnologías)
3. [Arquitectura](#arquitectura)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Variables de Entorno](#variables-de-entorno)
7. [Ejecución](#ejecución)
8. [APIs REST](#apis-rest)
9. [Proceso ETL](#proceso-etl)
10. [Machine Learning](#machine-learning)
11. [Analítica de Datos](#analítica-de-datos)
12. [Dashboard Frontend](#dashboard-frontend)
13. [Diagrama ERD](#diagrama-erd)
14. [Manual de Usuario](#manual-de-usuario)

---

## Descripción General

El sistema automatiza el procesamiento de información médica y apoya la toma de decisiones
clínicas mediante analítica predictiva. Recibe datasets clínicos con inconsistencias reales,
los limpia y transforma mediante un pipeline ETL, entrena un modelo de clasificación de riesgo
y expone los resultados a través de un dashboard interactivo.

**Problemas que resuelve:**
- Mala calidad de datos clínicos (nulos, duplicados, errores ortográficos, tipos incorrectos)
- Falta de indicadores clínicos centralizados
- Dificultad para detectar pacientes de alto riesgo
- Ausencia de predicción automatizada de enfermedades

---

## Tecnologías

### Backend
| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.12+ | Lenguaje principal |
| Django | 6.0 | Framework web |
| Django REST Framework | 3.x | APIs REST |
| SimpleJWT | 5.x | Autenticación JWT |
| Pandas | 2.x | ETL y transformación |
| NumPy | 1.x | Cálculos numéricos |
| Scikit-learn | 1.x | Machine Learning |
| Joblib | 1.x | Serialización del modelo |
| psycopg2 | 2.x | Conector PostgreSQL |
| django-cors-headers | 4.x | CORS |
| python-dotenv | 1.x | Variables de entorno |

### Base de Datos
| Motor | Uso |
|---|---|
| PostgreSQL (Neon Cloud) | Base de datos principal |

### Frontend
| Tecnología | Uso |
|---|---|
| React 19 | UI principal |
| Axios | Consumo de APIs |
| Recharts | Visualizaciones |
| react-icons | Iconografía |

---

## Arquitectura

```
┌─────────────────────────────────────────┐
│           Frontend React 19             │
│    Dashboard · KPIs · Gráficas · ML     │
└──────────────────┬──────────────────────┘
                   │  REST API (JWT)
┌──────────────────▼──────────────────────┐
│           Django Backend                │
├─────────────────────────────────────────┤
│  patients/   → CRUD + KPIs + Charts     │
│  etl/        → Pipeline ETL + Logs      │
│  analytics/  → Estadísticas + KPIs+     │
│  ml/         → Entrenamiento + Predict  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│       PostgreSQL — Neon Cloud           │
│  patients · etl_logs · ml_metrics      │
└─────────────────────────────────────────┘
```

---

## Estructura del Proyecto

```
pipeline-reto/
│
├── backend/                  # Configuración Django
│   ├── settings.py
│   ├── urls.py               # URLs raíz (incluye todos los módulos)
│   └── wsgi.py
│
├── patients/                 # App principal de pacientes
│   ├── models.py             # Modelo Patient (22 campos clínicos)
│   ├── serializers.py
│   ├── views.py              # CRUD + KPIs + Charts + Reportes
│   ├── predict.py            # Predicción individual con el modelo ML
│   └── urls.py
│
├── etl/                      # Módulo ETL completo
│   ├── etl_process.py        # Pipeline: Extract → Transform → Load
│   ├── models.py             # ETLLog — historial de ejecuciones
│   ├── serializers.py
│   ├── views.py              # POST run · GET historial · GET detalle
│   ├── admin.py
│   └── urls.py
│
├── analytics/                # Módulo de analítica estadística
│   ├── views.py              # Estadísticas · KPIs · Segmentación · Críticos
│   └── urls.py
│
├── ml/                       # Módulo Machine Learning
│   ├── train_model.py        # Entrenamiento RandomForest + métricas
│   ├── models.py             # MLMetrics — historial de entrenamientos
│   ├── serializers.py
│   ├── views.py              # Train · Metrics · Historial · Predict
│   ├── admin.py
│   ├── urls.py
│   ├── risk_model.pkl        # Modelo entrenado
│   └── label_encoder.pkl     # Encoder de clases
│
├── authentication/           # App de autenticación (JWT)
│
├── dashboard/                # App de dashboard
│
├── frontend/                 # React 19
│   └── src/
│       ├── App.js            # Dashboard completo
│       ├── App.css           # Estilos tipo Power BI
│       └── index.css         # Fuentes globales
│
├── datasets/
│   ├── dataset_clinico_etl_1800_registros.xlsx  # Dataset original sucio
│   └── clean_clinical_dataset.csv               # Dataset limpio (post-ETL)
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env                      # Variables de entorno (NO subir a Git)
```

---

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/cervantessaralucia4-dotcom/pipeline-reto.git
cd pipeline-reto
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear el archivo `.env` en la raíz del proyecto (ver sección siguiente).

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

Backend disponible en: `http://127.0.0.1:8000/`

---

## Variables de Entorno

Crear el archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Django
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True

# Base de datos PostgreSQL
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=tu_password_aqui
DB_HOST=tu_host_neon.aws.neon.tech
DB_PORT=5432
```

> ⚠️ **Nunca subas el archivo `.env` a GitHub.** Asegúrate de que está en `.gitignore`.

El archivo `backend/settings.py` debe leer estas variables así:

```python
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.getenv('DB_NAME'),
        'USER':     os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST':     os.getenv('DB_HOST'),
        'PORT':     os.getenv('DB_PORT', '5432'),
        'OPTIONS':  {'sslmode': 'require'},
    }
}
```

---

## Ejecución

### Backend

```bash
# Servidor de desarrollo
python manage.py runserver

# Admin Django
http://127.0.0.1:8000/admin/
```

### Frontend

```bash
cd frontend
npm install
npm start
# http://localhost:3000/
```

### ETL (vía API)

```bash
# Requiere token JWT
curl -X POST http://127.0.0.1:8000/api/etl/run/ \
  -H "Authorization: Bearer TU_TOKEN"
```

### Entrenar modelo ML (vía API)

```bash
curl -X POST http://127.0.0.1:8000/api/ml/train/ \
  -H "Authorization: Bearer TU_TOKEN"
```

---

## APIs REST

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer <access_token>
```

### 🔐 Autenticación

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/token/` | Login — obtener access + refresh token |
| POST | `/api/token/refresh/` | Renovar access token |

**Body login:**
```json
{ "username": "admin", "password": "tu_password" }
```

---

### 👥 Pacientes

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/patients/` | Listar todos los pacientes |
| POST | `/api/patients/` | Crear paciente |
| GET | `/api/patients/{id}/` | Detalle de un paciente |
| PUT | `/api/patients/{id}/` | Actualizar paciente |
| DELETE | `/api/patients/{id}/` | Eliminar paciente |

---

### 📊 Dashboard

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/dashboard/kpis/` | 7 KPIs principales |
| GET | `/api/dashboard/charts/` | Datos para gráficas |
| GET | `/api/reportes/` | Reporte general |

**Respuesta `/api/dashboard/kpis/`:**
```json
{
  "total_patients": 1792,
  "critical_patients": 120,
  "high_risk": 450,
  "medium_risk": 780,
  "low_risk": 442,
  "average_glucose": 207.61,
  "average_bmi": 27.2
}
```

---

### 🔄 ETL

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/etl/run/` | Ejecutar pipeline ETL completo |
| GET | `/api/etl/historial/` | Historial de ejecuciones |
| GET | `/api/etl/historial/{id}/` | Detalle de una ejecución |

**Respuesta `/api/etl/run/`:**
```json
{
  "estado": "exitoso",
  "log_id": 1,
  "registros_extraidos": 1850,
  "registros_duplicados": 48,
  "registros_nulos": 183,
  "registros_fuera_rango": 10,
  "registros_cargados": 1792,
  "tiempo_ejecucion": 0.63
}
```

---

### 📈 Analytics

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/analytics/estadisticas/` | Media, mediana, moda, desv. estándar de 9 variables |
| GET | `/api/analytics/kpis/` | KPIs médicos: hipertensos, diabéticos, fumadores, etc. |
| GET | `/api/analytics/segmentacion/` | Por riesgo, sexo, edad, IMC, diagnóstico |
| GET | `/api/analytics/criticos/` | Alertas y listado de pacientes críticos |

**Respuesta `/api/analytics/kpis/`:**
```json
{
  "total_pacientes": 1792,
  "hipertensos":   { "cantidad": 936,  "porcentaje": 52.2 },
  "diabeticos":    { "cantidad": 1415, "porcentaje": 79.0 },
  "fumadores":     { "cantidad": 900,  "porcentaje": 50.2 },
  "obesidad":      { "cantidad": 791,  "porcentaje": 44.1 },
  "promedios": {
    "glucosa": 207.61,
    "imc": 27.2,
    "edad": 49.3
  }
}
```

---

### 🤖 Machine Learning

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/ml/train/` | Entrenar modelo y guardar métricas |
| GET | `/api/ml/metrics/` | Métricas del último entrenamiento |
| GET | `/api/ml/historial/` | Historial de entrenamientos |
| POST | `/api/ml/predict/` | Predicción individual |

**Body `/api/ml/predict/`:**
```json
{
  "edad": 55,
  "IMC": 32.1,
  "glucosa": 320.0,
  "colesterol": 240.0,
  "presión_sistólica": 185,
  "frecuencia_cardiaca": 95
}
```

**Respuesta:**
```json
{
  "riesgo_predicho": "Crítico",
  "probabilidades": {
    "Alto": 0.0,
    "Bajo": 0.0,
    "Crítico": 1.0,
    "Medio": 0.0
  }
}
```

**Métricas del modelo (RandomForest — 1792 registros):**
```
Accuracy:  66.57%
Precision: 66.83%
Recall:    66.57%
F1 Score:  66.54%
```

**Importancia de variables:**
```
glucosa              33.8%  ████████████
presión_sistólica    25.8%  █████████
IMC                  10.9%  ████
colesterol           10.6%  ███
frecuencia_cardiaca   9.9%  ███
edad                  8.9%  ███
```

---

## Proceso ETL

### Flujo completo

```
dataset_clinico_etl_1800_registros.xlsx
              │
        1. EXTRACT
         └── Leer Excel (1850 registros)
              │
        2. TRANSFORM
         ├── Eliminar duplicados        → -48 registros
         ├── Convertir tipos de datos   (edad='Treinta' → 30)
         ├── Tratar nulos               → media/mediana/moda
         ├── Validar rangos clínicos    → -10 registros
         ├── Normalizar sexo            (m/f/Femenino → M/F)
         ├── Normalizar diagnósticos    (hipertencion → Hipertensión)
         ├── Recalcular IMC             (peso / altura²)
         └── Clasificar riesgo          (reglas clínicas)
              │
        3. LOAD
         ├── Guardar en PostgreSQL      (1792 pacientes)
         ├── Exportar CSV limpio
         └── Registrar ETLLog           (trazabilidad completa)
```

### Reglas de clasificación de riesgo

| Condición | Nivel |
|---|---|
| Glucosa > 300 ó Presión > 180 ó Saturación < 85 | Crítico |
| Glucosa > 200 ó Presión > 160 | Alto |
| Glucosa > 140 ó Presión > 140 | Medio |
| Sin condiciones anteriores | Bajo |

### Clasificación IMC

| IMC | Clasificación |
|---|---|
| < 18.5 | Bajo peso |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Sobrepeso |
| ≥ 30 | Obesidad |

---

## Machine Learning

### Modelo: Random Forest Classifier

```
Dataset limpio (1792 registros)
        │
  Preprocesamiento
  └── LabelEncoder para target
        │
  Train/Test Split  (80% / 20%)
  └── 1433 train · 359 test
        │
  Entrenamiento
  └── RandomForestClassifier(n_estimators=100, random_state=42)
        │
  Evaluación
  ├── Accuracy:  66.57%
  ├── Precision: 66.83%
  ├── Recall:    66.57%
  └── F1 Score:  66.54%
        │
  Guardar
  ├── ml/risk_model.pkl
  └── ml/label_encoder.pkl
```

### Variables predictoras

- `edad` — Edad del paciente
- `IMC` — Índice de masa corporal
- `glucosa` — Nivel de glucosa
- `colesterol` — Nivel de colesterol
- `presión_sistólica` — Presión sistólica
- `frecuencia_cardiaca` — Frecuencia cardíaca

### Clases predichas

`Bajo` · `Medio` · `Alto` · `Crítico`

---

## Diagrama ERD

```
┌─────────────────────────────────────────────┐
│                  Patient                    │
├─────────────────────────────────────────────┤
│ PK  id                    BigInt           │
│     first_name            Varchar(100)     │
│     last_name             Varchar(100)     │
│     age                   Integer          │
│     sex                   Char(1) M/F      │
│     weight                Float            │
│     height                Float            │
│     bmi                   Float            │
│     systolic_pressure     Integer          │
│     diastolic_pressure    Integer          │
│     heart_rate            Integer          │
│     glucose               Float            │
│     cholesterol           Float            │
│     oxygen_saturation     Float            │
│     temperature           Float            │
│     family_history        Boolean          │
│     smoker                Boolean          │
│     alcohol_consumption   Boolean          │
│     physical_activity     Varchar(20)      │
│     preliminary_diagnosis Varchar(255)     │
│     disease_risk          Varchar(20)      │
│     consultation_date     Date             │
│     created_at            DateTime         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│                  ETLLog                     │
├─────────────────────────────────────────────┤
│ PK  id                    BigInt           │
│ FK  usuario               → auth_user      │
│     fecha_inicio          DateTime         │
│     fecha_fin             DateTime         │
│     tiempo_ejecucion      Float            │
│     registros_extraidos   Integer          │
│     registros_duplicados  Integer          │
│     registros_nulos       Integer          │
│     registros_fuera_rango Integer          │
│     registros_cargados    Integer          │
│     estado                Varchar(20)      │
│     mensaje               Text             │
│     archivo_fuente        Varchar(255)     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│                MLMetrics                    │
├─────────────────────────────────────────────┤
│ PK  id                    BigInt           │
│ FK  usuario               → auth_user      │
│     fecha_entrenamiento   DateTime         │
│     accuracy              Float            │
│     precision             Float            │
│     recall                Float            │
│     f1_score              Float            │
│     confusion_matrix      JSON             │
│     total_registros       Integer          │
│     registros_train       Integer          │
│     registros_test        Integer          │
│     modelo                Varchar(100)     │
│     features              JSON             │
│     importancia           JSON             │
└─────────────────────────────────────────────┘
```

---

## Manual de Usuario

### 1. Login

1. Abrir `http://localhost:3000/`
2. Ingresar usuario y contraseña del superusuario creado con `createsuperuser`
3. Hacer clic en **Ingresar**

### 2. Dashboard principal

El dashboard muestra automáticamente al iniciar sesión:
- **7 KPI cards** — Total pacientes, Críticos, Riesgo Alto/Medio/Bajo, Glucosa promedio, IMC promedio
- **Gráfica de distribución** — Pie chart con porcentajes de riesgo
- **Gráfica de barras** — Pacientes por nivel de riesgo
- **Indicadores clínicos** — Glucosa e IMC con porcentajes de críticos y riesgo alto
- **Tabla de pacientes** — Con búsqueda, ordenamiento por columna y paginación

### 3. Ejecutar el ETL

```
POST /api/etl/run/
Authorization: Bearer <token>
```

El ETL procesa el archivo `datasets/dataset_clinico_etl_1800_registros.xlsx`,
limpia los datos y carga 1792 pacientes en la base de datos.

Puedes ver el historial en `GET /api/etl/historial/`

### 4. Entrenar el modelo ML

```
POST /api/ml/train/
Authorization: Bearer <token>
```

Reentrena el modelo con los datos limpios más recientes y guarda las métricas.

### 5. Predecir riesgo de un paciente

```
POST /api/ml/predict/
Authorization: Bearer <token>

{
  "edad": 45,
  "IMC": 28.5,
  "glucosa": 180.0,
  "colesterol": 220.0,
  "presión_sistólica": 150,
  "frecuencia_cardiaca": 88
}
```

### 6. Ver analítica estadística

```
GET /api/analytics/estadisticas/   → Media, mediana, moda, desv. estándar
GET /api/analytics/kpis/           → Hipertensos, diabéticos, fumadores
GET /api/analytics/segmentacion/   → Por edad, sexo, IMC, diagnóstico
GET /api/analytics/criticos/       → Pacientes en estado crítico
```

### 7. Logout

Clic en el botón **Logout** en la esquina superior derecha del dashboard.

---

## Docker (Opcional)

```bash
# Construir y levantar los servicios
docker-compose up --build

# Backend: http://localhost:8000/
# Frontend: http://localhost:3000/
```

---

## Autora

**Sara Lucía Cervantes**
Tecnologo en Análisis y Desarrollo de Software — SENA
Reto Técnico HealthAnalytics IPS · Junio 2026

---

## Licencia

Proyecto educativo y de portafolio — SENA 2026