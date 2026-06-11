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
| Recharts | Visualizaciones (Pie, Bar) |
| react-icons | Iconografía (Feather Icons) |
| Create React App | Build tool |

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
├── authentication/           # Autenticación JWT + perfiles de usuario
│   ├── models.py             # UserProfile (rol: administrador/medico/analista)
│   ├── permissions.py        # Permisos por rol (IsAnalista, IsMedicoOrAnalista, etc.)
│   ├── serializers.py
│   ├── views.py              # Register, Profile, List users, Change rol
│   └── urls.py
│
├── dashboard/                # App de dashboard (endpoints)
│
├── analytics/                # Módulo de analítica estadística
│   ├── views.py              # Estadísticas · KPIs · Segmentación · Críticos · Pacientes por filtro
│   └── urls.py
│
├── frontend/                 # React 19
│   └── src/
│       ├── App.js            # Dashboard completo (7 secciones, roles, polling)
│       ├── App.css           # Estilos dark glassmorphism con gradientes
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
| GET | `/api/auth/me/` | Obtener perfil del usuario autenticado |
| POST | `/api/auth/register/` | Registrar nuevo usuario (Admin) |
| GET | `/api/auth/users/` | Listar todos los usuarios (Admin) |
| PUT | `/api/auth/users/{id}/rol/` | Cambiar rol de usuario (Admin) |

**Body login:**
```json
{ "username": "admin", "password": "tu_password" }
```

**Roles disponibles:**
- `administrador` — Acceso total al sistema, gestión de usuarios
- `medico` — Solo visualización (Dashboard, Pacientes, Analytics, Reportes). Sin ETL, ML ni exportación CSV
- `analista` — Ejecución ETL y ML, más todos los módulos de visualización

---



### 👥 Pacientes

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/patients/` | Listar todos los pacientes |
| POST | `/api/patients/` | Crear paciente (Admin) |
| GET | `/api/patients/{id}/` | Detalle de un paciente |
| PUT | `/api/patients/{id}/` | Actualizar paciente (Admin) |
| DELETE | `/api/patients/{id}/` | Eliminar paciente (Admin) |
| GET | `/api/patients/export/csv/` | Exportar todos los pacientes a CSV con BOM UTF-8 |

---

### 📊 Dashboard

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/dashboard/kpis/` | 7 KPIs principales |
| GET | `/api/dashboard/charts/` | Datos para gráficas |
| GET | `/api/reportes/` | Reporte general (usado en sección Reportes) |
| GET | `/api/patients/export/csv/` | Exportar CSV con BOM UTF-8 y quoting |

**Respuesta `/api/dashboard/kpis/`:**
```json
{
  "total_patients": 1792,
  "critical_patients": 1043,
  "high_risk": 419,
  "medium_risk": 198,
  "low_risk": 132,
  "average_glucose": 207.61,
  "average_bmi": 29.06
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
  "generos_corregidos": 183,
  "registros_cargados": 1792,
  "tiempo_ejecucion": 0.8
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
| GET | `/api/analytics/pacientes-por-filtro/?filtro=<filtro>` | Pacientes que cumplen un filtro médico (hipertensos, diabeticos, etc.) |

**Respuesta `/api/analytics/kpis/`:**
```json
{
  "total_pacientes": 1792,
  "hipertensos":       { "cantidad": 936,  "porcentaje": 52.2 },
  "diabeticos":        { "cantidad": 1415, "porcentaje": 79.0 },
  "fumadores":         { "cantidad": 900,  "porcentaje": 50.2 },
  "con_antecedentes":  { "cantidad": 883,  "porcentaje": 49.3 },
  "alcoholismo":       { "cantidad": 870,  "porcentaje": 48.5 },
  "obesidad":          { "cantidad": 791,  "porcentaje": 44.1 },
  "saturacion_baja":   { "cantidad": 1035, "porcentaje": 57.8 },
  "promedios": {
    "glucosa": 207.61,
    "imc": 29.06,
    "edad": 54.8,
    "colesterol": 234.81,
    "presion_sistolica": 144.3
  }
}
```

**Filtros disponibles para `pacientes-por-filtro/`:** `hipertensos`, `diabeticos`, `fumadores`, `con_antecedentes`, `alcoholismo`, `obesidad`, `saturacion_baja`

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
          ├── Corregir género por nombre → detecta nombres femeninos/masculinos y corrige sexo
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

### Roles y permisos

El sistema tiene 3 roles con diferentes niveles de acceso:

| Sección | Administrador | Médico | Analista |
|---|---|---|---|
| Dashboard | ✅ | ✅ | ✅ |
| Pacientes | ✅ CRUD | ✅ Solo lectura | ✅ Solo lectura |
| ETL | ✅ | ❌ Oculto | ✅ |
| Analytics | ✅ | ✅ | ✅ |
| Machine Learning | ✅ | ❌ Oculto | ✅ |
| Reportes | ✅ (CSV+PDF) | ✅ (solo PDF) | ✅ (CSV+PDF) |
| Usuarios | ✅ | ❌ | ❌ |

### 1. Login

1. Abrir `http://localhost:3000/`
2. Ingresar usuario y contraseña
3. Hacer clic en **Ingresar**

**Usuarios de prueba preconfigurados:**
- `admin` / `admin123` — Superusuario (todos los permisos)
- `analista_ips` / `analista123` — Rol Analista
- `medico_ips` / `medico123` — Rol Médico
- `admin_ips` / `admin123` — Rol Administrador

### 2. Dashboard principal

El dashboard se actualiza automáticamente cada 30 segundos. Muestra:
- **7 KPI cards** — Total pacientes, Críticos, Riesgo Alto/Medio/Bajo, Glucosa promedio, IMC promedio
- **Gráfica de distribución** — Pie chart con porcentajes de riesgo (con centro donut)
- **Gráfica de barras** — Pacientes por nivel de riesgo
- **Indicadores clínicos** — Glucosa, IMC, % Críticos, % Riesgo alto
- **Tabla de pacientes** — Con búsqueda en vivo, ordenamiento por columna (ID, Nombre, Edad, Riesgo) y paginación

### 3. Sección Pacientes

- Lista completa de pacientes con paginación (10 por página)
- Búsqueda por nombre, riesgo o ID
- Ordenamiento ascendente/descendente por columnas
- Los datos se refrescan automáticamente cada 30 segundos (ideal para ver cambios post-ETL)

### 4. Ejecutar el ETL (Analista/Admin)

1. Navegar a la sección **ETL**
2. Hacer clic en **Ejecutar ETL ahora**
3. El pipeline procesa el archivo Excel, elimina duplicados, corrige nulos, valida rangos, **corrige género según el nombre**, y carga los pacientes
4. Se muestran estadísticas: extraídos, duplicados, nulos, fuera de rango, géneros corregidos, cargados
5. El historial de ejecuciones queda registrado con trazabilidad

```
POST /api/etl/run/
Authorization: Bearer <token>
```

### 5. Sección Analytics

- **KPIs médicos interactivos:** Hipertensos, Diabéticos, Fumadores, Con antecedentes, Alcoholismo, Obesidad, Saturación baja
- Cada tarjeta KPI es cliqueable → abre un modal con la lista de pacientes que cumplen ese criterio
- El modal incluye búsqueda en vivo dentro de los resultados filtrados
- **Estadística descriptiva:** Media, mediana, moda, desv. estándar, mínimo y máximo de 9 variables clínicas
- **Segmentación:** Por nivel de riesgo, grupo de edad y clasificación IMC (con barras de progreso)
- **Alertas clínicas:** Presión sistólica > 180, Glucosa > 300, Saturación < 85%

### 6. Entrenar el modelo ML (Analista/Admin)

1. Navegar a la sección **Machine Learning**
2. Hacer clic en **Reentrenar modelo**
3. Se muestran métricas: Accuracy, Precision, Recall, F1 Score
4. **Predicción individual:** Ingresar datos clínicos del paciente y obtener riesgo predicho con probabilidades

### 7. Reportes

- **Exportar CSV:** Descarga todos los pacientes en formato CSV con UTF-8 BOM y quoting (compatible con Excel)
- **Exportar PDF/Imprimir:** Vista optimizada para impresión (oculta sidebar, botones y elementos no esenciales)

### 8. Gestión de Usuarios (Admin)

- Listado de todos los usuarios del sistema
- Crear nuevos usuarios con selección de rol
- Cambiar rol de usuarios existes desde la misma tabla

### 9. Logout

Clic en el botón **Cerrar sesión** en la parte inferior de la barra lateral.

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