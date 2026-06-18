# Evidencias — Pipeline ETL

## 1. Dataset Original

**Archivo:** `datasets/dataset_clinico_etl_1800_registros.xlsx`

Dataset clínico con 1850 registros que contiene inconsistencias reales:
- Duplicados (48 registros)
- Valores nulos en múltiples columnas
- Errores ortográficos en diagnósticos ("hipertencion", "diabete")
- Edades en formato texto ("Treinta", "treinta y dos")
- Sexo con formatos inconsistentes (m, f, Femenino, Masculino, M, F)
- Valores fuera de rango clínico (glucosa > 500, saturación < 50)
- Registros sin nombre

## 2. Pipeline ETL — Flujo de Transformación

```
EXTRACT (1850 registros)
│
├── Carga archivo Excel
│
▼
TRANSFORM
│
├── 1. Eliminación de duplicados exactos
│      → -48 registros (1802 restantes)
│
├── 2. Eliminación de registros sin nombre
│      → -10 registros (1792 restantes)
│
├── 3. Conversión de tipos de datos
│      │  Edad: "Treinta" → 30, "treinta y dos" → 32
│      │  Glucosa: cadenas → float
│      └  Diagnósticos: normalización de mayúsculas/minúsculas
│
├── 4. Corrección de sexo por nombre
│      │  Detecta nombres femeninos/masculinos
│      └  Corrige 183 registros con sexo inconsistente
│
├── 5. Tratamiento de valores nulos
│      │  presión arterial → media del grupo
│      │  frecuencia cardíaca → mediana
│      └  saturación de oxígeno → moda
│
├── 6. Validación de rangos clínicos
│      │  Glucosa: 50-400 mg/dL
│      │  Saturación: 50-100%
│      │  IMC: 10-60
│      │  Temperatura: 34-42°C
│      └  -10 registros fuera de rango
│
├── 7. Normalización de diagnósticos
│      │  "hipertencion" → "Hipertensión"
│      │  "diabete" → "Diabetes"
│      │  "EPOC" → normalizado
│      └  Corrección de tildes y mayúsculas
│
├── 8. Cálculo de IMC
│      └  IMC = peso(kg) / altura(m)²
│
├── 9. Clasificación de riesgo (reglas clínicas)
│      │  Glucosa > 300 o Presión > 180 o Saturación < 85 → Crítico
│      │  Glucosa > 200 o Presión > 160                 → Alto
│      │  Glucosa > 140 o Presión > 140                 → Medio
│      └  Ninguna condición anterior                     → Bajo
│
▼
LOAD (1792 pacientes)
│
├── Inserción en PostgreSQL (tabla patients_patient)
├── Exportación a CSV limpio (datasets/clean_clinical_dataset.csv)
└── Registro en ETLLog (trazabilidad completa)
```

## 3. Log de Ejecución (Muestra)

```
══════════════════════════════════════════════════════════════════
  ETL #1 — ejecutado por admin_ips
  Fecha: 2026-06-12 19:30:25
  Estado: EXITOSO
══════════════════════════════════════════════════════════════════

  Estadísticas:
  ┌──────────────────────────────────┬───────────┐
  │ Registros extraídos              │    1,850  │
  │ Registros duplicados eliminados  │       48  │
  │ Valores nulos tratados           │      183  │
  │ Registros fuera de rango         │       10  │
  │ Géneros corregidos               │      183  │
  │ Registros cargados en BD         │    1,792  │
  │ Tiempo de ejecución              │  0.83 s   │
  └──────────────────────────────────┴───────────┘

  Detalle de nulos tratados:
  ├── presión_sistólica:    42 nulos → imputados con media
  ├── frecuencia_cardíaca:  38 nulos → imputados con mediana
  ├── saturación_oxígeno:   36 nulos → imputados con moda
  ├── colesterol:           35 nulos → imputados con media
  └── glucosa:              32 nulos → imputados con media

  Diagnósticos corregidos:
  ├── "hipertencion"      → "Hipertensión"       (28 veces)
  ├── "diabete"           → "Diabetes"            (15 veces)
  ├── "EPOC"              → "EPOC" (normalizado)  (12 veces)
  └── "Asma"              → "Asma" (normalizado)  (8 veces)
```

## 4. Reporte Post-ETL

```json
{
  "total_patients": 1792,
  "critical_patients": 1043,
  "high_risk": 419,
  "medium_risk": 198,
  "low_risk": 132,
  "average_glucose": 207.61,
  "average_bmi": 29.06,
  "average_age": 54.8,
  "sex_distribution": {
    "Masculino": 920,
    "Femenino": 872
  },
  "imc_classification": {
    "Bajo peso": 45,
    "Normal": 396,
    "Sobrepeso": 560,
    "Obesidad": 791
  }
}
```

## 5. Trazabilidad

Cada ejecución del ETL queda registrada en la tabla `etl_etllog` con:
- Usuario que ejecutó
- Fecha y hora de inicio/fin
- Tiempo de ejecución
- Estadísticas completas (extraídos, duplicados, nulos, fuera de rango, cargados)
- Estado (exitoso/fallido)
- Mensaje de error en caso de fallo
- Archivo fuente procesado
