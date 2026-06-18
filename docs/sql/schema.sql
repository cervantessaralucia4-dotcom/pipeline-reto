-- ══════════════════════════════════════════════════════════════
--  HealthAnalytics IPS — Esquema de Base de Datos
--  Motor: PostgreSQL (Neon Cloud)
--  Generado a partir de modelos Django
-- ══════════════════════════════════════════════════════════════

-- ── Extensión UUID (opcional) ───────────────────────────────
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ══════════════════════════════════════════════════════════════
--  TABLA: auth_user (Django — Usuarios del sistema)
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS auth_user (
    id              SERIAL PRIMARY KEY,
    password        VARCHAR(128) NOT NULL,
    last_login      TIMESTAMPTZ,
    is_superuser    BOOLEAN NOT NULL DEFAULT FALSE,
    username        VARCHAR(150) NOT NULL UNIQUE,
    first_name      VARCHAR(150) NOT NULL DEFAULT '',
    last_name       VARCHAR(150) NOT NULL DEFAULT '',
    email           VARCHAR(254) NOT NULL DEFAULT '',
    is_staff        BOOLEAN NOT NULL DEFAULT FALSE,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined     TIMESTAMPTZ NOT NULL
);

-- ══════════════════════════════════════════════════════════════
--  TABLA: authentication_userprofile (Perfiles con rol)
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS authentication_userprofile (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    rol         VARCHAR(20) NOT NULL DEFAULT 'medico'
                CHECK (rol IN ('administrador', 'medico', 'analista')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ══════════════════════════════════════════════════════════════
--  TABLA: patients_patient (Pacientes clínicos)
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS patients_patient (
    id                      SERIAL PRIMARY KEY,
    first_name              VARCHAR(100) NOT NULL,
    last_name               VARCHAR(100) NOT NULL,
    age                     INTEGER NOT NULL,
    sex                     VARCHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
    weight                  DOUBLE PRECISION NOT NULL,
    height                  DOUBLE PRECISION NOT NULL,
    bmi                     DOUBLE PRECISION NULL,
    systolic_pressure       INTEGER NOT NULL,
    diastolic_pressure      INTEGER NOT NULL,
    heart_rate              INTEGER NOT NULL,
    glucose                 DOUBLE PRECISION NOT NULL,
    cholesterol             DOUBLE PRECISION NOT NULL,
    oxygen_saturation       DOUBLE PRECISION NOT NULL,
    temperature             DOUBLE PRECISION NOT NULL,
    family_history          BOOLEAN NOT NULL DEFAULT FALSE,
    smoker                  BOOLEAN NOT NULL DEFAULT FALSE,
    alcohol_consumption     BOOLEAN NOT NULL DEFAULT FALSE,
    physical_activity       VARCHAR(20) NOT NULL CHECK (physical_activity IN ('Baja', 'Media', 'Alta')),
    preliminary_diagnosis   VARCHAR(255) NOT NULL,
    disease_risk            VARCHAR(20) NOT NULL CHECK (disease_risk IN ('Bajo', 'Medio', 'Alto', 'Crítico')),
    consultation_date       DATE NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_patient_risk     ON patients_patient(disease_risk);
CREATE INDEX IF NOT EXISTS idx_patient_name     ON patients_patient(first_name, last_name);
CREATE INDEX IF NOT EXISTS idx_patient_glucose  ON patients_patient(glucose);
CREATE INDEX IF NOT EXISTS idx_patient_age      ON patients_patient(age);

-- ══════════════════════════════════════════════════════════════
--  TABLA: etl_etllog (Historial de ejecuciones ETL)
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS etl_etllog (
    id                      SERIAL PRIMARY KEY,
    usuario_id              INTEGER NULL REFERENCES auth_user(id) ON DELETE SET NULL,
    fecha_inicio            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_fin               TIMESTAMPTZ NULL,
    tiempo_ejecucion        DOUBLE PRECISION NULL,
    registros_extraidos     INTEGER NOT NULL DEFAULT 0,
    registros_duplicados    INTEGER NOT NULL DEFAULT 0,
    registros_nulos         INTEGER NOT NULL DEFAULT 0,
    registros_fuera_rango   INTEGER NOT NULL DEFAULT 0,
    registros_cargados      INTEGER NOT NULL DEFAULT 0,
    estado                  VARCHAR(20) NOT NULL DEFAULT 'en_proceso'
                            CHECK (estado IN ('exitoso', 'fallido', 'en_proceso')),
    mensaje                 TEXT NOT NULL DEFAULT '',
    archivo_fuente          VARCHAR(255) NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_etllog_fecha ON etl_etllog(fecha_inicio DESC);

-- ══════════════════════════════════════════════════════════════
--  TABLA: ml_mlmetrics (Métricas de entrenamiento ML)
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS ml_mlmetrics (
    id                      SERIAL PRIMARY KEY,
    fecha_entrenamiento     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    usuario_id              INTEGER NULL REFERENCES auth_user(id) ON DELETE SET NULL,
    accuracy                DOUBLE PRECISION NOT NULL,
    precision               DOUBLE PRECISION NOT NULL,
    recall                  DOUBLE PRECISION NOT NULL,
    f1_score                DOUBLE PRECISION NOT NULL,
    confusion_matrix        JSONB NOT NULL,
    total_registros         INTEGER NOT NULL DEFAULT 0,
    registros_train         INTEGER NOT NULL DEFAULT 0,
    registros_test          INTEGER NOT NULL DEFAULT 0,
    modelo                  VARCHAR(100) NOT NULL DEFAULT 'RandomForestClassifier',
    features                JSONB NOT NULL DEFAULT '[]',
    importancia             JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_mlmetrics_fecha ON ml_mlmetrics(fecha_entrenamiento DESC);

-- ══════════════════════════════════════════════════════════════
--  DATOS INICIALES: Usuarios por defecto
--  Contraseñas hasheadas con PBKDF2 (Django)
-- ══════════════════════════════════════════════════════════════
-- NOTA: Ejecutar `python manage.py migrate` para crear los usuarios
-- o insertarlos manualmente con contraseñas hasheadas.
--
-- Usuarios preconfigurados (creados vía data migration 0002):
--   admin_ips    / Admin2026*    → administrador
--   medico_ips   / Medico2026*   → medico
--   analista_ips / Analista2026* → analista
