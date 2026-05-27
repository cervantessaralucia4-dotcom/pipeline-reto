# README — Healthcare ETL Platform

## 📌 Descripción del Proyecto

Healthcare ETL Platform es una plataforma clínica desarrollada con:

* Django REST Framework
* PostgreSQL
* React
* Pandas
* Machine Learning (Random Forest)

El sistema permite:

✅ Procesar datasets clínicos
✅ Limpiar y transformar datos médicos
✅ Cargar información a PostgreSQL
✅ Exponer APIs REST
✅ Entrenar modelos de IA médica
✅ Visualizar estadísticas clínicas en un dashboard

---

# 🏗 Arquitectura

```text
React Frontend
       ↓
Django REST API
       ↓
PostgreSQL
       ↓
ETL + Machine Learning
```

---

# 🚀 Tecnologías Utilizadas

## Backend

* Python
* Django
* Django REST Framework

## Base de Datos

* PostgreSQL

## ETL y Ciencia de Datos

* Pandas
* NumPy

## Machine Learning

* Scikit-learn

## Frontend

* React
* Axios
* Chart.js

---

# ⚙ Requisitos Previos

Instalar:

## 1. Python

[Python Oficial](https://www.python.org/downloads/?utm_source=chatgpt.com)

⚠ IMPORTANTE:
Durante la instalación marcar:

```text
Add Python to PATH
```

---

## 2. Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com/?utm_source=chatgpt.com)

---

## 3. Git

[Git Oficial](https://git-scm.com/downloads?utm_source=chatgpt.com)

---

## 4. PostgreSQL

[PostgreSQL Oficial](https://www.postgresql.org/download/?utm_source=chatgpt.com)

Guardar:

* usuario
* contraseña
* puerto

---

# 📥 Clonar Proyecto

```bash
git clone https://github.com/cervantessaralucia4-dotcom/pipeline-reto.git
```

Entrar al proyecto:

```bash
cd pipeline-reto
```

---

# 🐍 Configuración Backend

# 1. Crear entorno virtual

```bash
python -m venv venv
```

---

# 2. Activar entorno virtual

## Windows

```bash
venv\Scripts\activate
```

---

# 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# 📦 Librerías Principales

El proyecto utiliza:

* Django
* djangorestframework
* pandas
* numpy
* scikit-learn
* psycopg2-binary
* python-dotenv
* matplotlib
* openpyxl

---

# 🗄 Configurar Base de Datos

Verificar configuración en:

```text
backend/settings.py
```

Ejemplo PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'healthcare_db',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

# 🔥 Migraciones

Crear tablas:

```bash
python manage.py makemigrations
```

Aplicar migraciones:

```bash
python manage.py migrate
```

---

# 👤 Crear Superusuario

```bash
python manage.py createsuperuser
```

---

# ▶ Ejecutar Backend

```bash
python manage.py runserver
```

Backend disponible en:

```text
http://127.0.0.1:8000
```

---

# ⚛ Configuración Frontend

Entrar al frontend:

```bash
cd frontend
```

---

# Instalar dependencias React

```bash
npm install
```

Instalar librerías adicionales:

```bash
npm install axios
```

```bash
npm install chart.js react-chartjs-2
```

---

# ▶ Ejecutar Frontend

```bash
npm start
```

Frontend disponible en:

```text
http://localhost:3000
```

---

# 🔄 ETL (Extract Transform Load)

## Ejecutar limpieza de datos

```bash
python etl/etl_process.py
```

Esto:

✅ limpia nulos
✅ elimina duplicados
✅ corrige diagnósticos
✅ recalcula IMC
✅ genera CSV limpio

---

# 📥 Cargar pacientes

```bash
python manage.py load_patients
```

---

# 🤖 Machine Learning

Entrenar modelo:

```bash
python ml/train_model.py
```

Métricas generadas:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

---

# 🔗 API REST

Endpoint principal:

```text
http://127.0.0.1:8000/api/patients/
```

---

# 📊 Dashboard

Frontend React consume APIs Django y muestra:

✅ estadísticas clínicas
✅ pacientes críticos
✅ KPIs médicos
✅ gráficas clínicas

---

# 🧠 Modelo Machine Learning

Se utiliza:

```text
Random Forest Classifier
```

Variables utilizadas:

* edad
* IMC
* glucosa
* colesterol
* presión sistólica
* frecuencia cardíaca

---

# 📁 Estructura del Proyecto

```text
pipeline-reto/
│
├── backend/
├── patients/
├── etl/
├── ml/
├── frontend/
├── datasets/
├── manage.py
├── requirements.txt
└── README.md
```

---

# 📌 Comandos Importantes

## Activar entorno

```bash
venv\Scripts\activate
```

---

## Backend

```bash
python manage.py runserver
```

---

## Frontend

```bash
npm start
```

---

## Migraciones

```bash
python manage.py migrate
```

---

## ETL

```bash
python etl/etl_process.py
```

---

## ML

```bash
python ml/train_model.py
```

---

# ✅ Estado del Proyecto

* [x] Backend Django
* [x] PostgreSQL
* [x] APIs REST
* [x] ETL clínico
* [x] Machine Learning
* [ ] Dashboard avanzado
* [ ] Deployment

---

# 👨‍💻 Autor

Sara Cervantes
