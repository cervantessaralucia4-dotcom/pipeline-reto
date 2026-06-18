# Evidencias — Machine Learning

## 1. Dataset de Entrenamiento

**Archivo:** `datasets/clean_clinical_dataset.csv`

Dataset limpio generado por el pipeline ETL con **1792 registros** y **22 columnas** clínicas.

### Variables Predictoras (Features)

| Variable | Tipo | Descripción | Rango |
|---|---|---|---|
| `edad` | numérica | Edad del paciente | 18-85 años |
| `IMC` | numérica | Índice de Masa Corporal | 14.5-42.3 |
| `glucosa` | numérica | Nivel de glucosa (mg/dL) | 50-400 |
| `colesterol` | numérica | Colesterol total (mg/dL) | 100-350 |
| `presión_sistólica` | numérica | Presión sistólica (mmHg) | 80-220 |
| `frecuencia_cardiaca` | numérica | Frecuencia cardíaca (lpm) | 40-130 |

### Variable Target

| Variable | Tipo | Clases |
|---|---|---|
| `disease_risk` | categórica | Bajo, Medio, Alto, Crítico |

### Distribución de Clases

| Clase | Cantidad | Porcentaje |
|---|---|---|
| Crítico | 1,043 | 58.2% |
| Alto | 419 | 23.4% |
| Medio | 198 | 11.0% |
| Bajo | 132 | 7.4% |

## 2. Modelo

**Algoritmo:** Random Forest Classifier

**Configuración:**
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)
```

### Split de Datos

| Conjunto | Registros | Porcentaje |
|---|---|---|
| Entrenamiento | 1,433 | 80% |
| Prueba | 359 | 20% |
| **Total** | **1,792** | **100%** |

## 3. Métricas de Desempeño

| Métrica | Valor |
|---|---|
| **Accuracy** | **66.57%** |
| **Precision** | **66.83%** |
| **Recall** | **66.57%** |
| **F1 Score** | **66.54%** |

### Matriz de Confusión

```
          ┌──────────────────────────────────┐
          │       Valor Real                 │
          │  Bajo  Medio  Alto  Crítico      │
┌─────────┼──────────────────────────────────┤
│  Bajo   │   8     3      2      3     │  16 │
│  Medio  │   2    17      6      8     │  33 │
│  Alto   │   2     8     57     21     │  88 │
│Crítico  │   4     9     35    174     │ 222 │
├─────────┼──────────────────────────────────┤
│         │  16    37    100    206    │ 359 │
└─────────┴──────────────────────────────────┘
```

## 4. Importancia de Variables

| Variable | Importancia | Ponderación |
|---|---|---|
| **glucosa** | **33.8%** | ████████████ |
| **presión_sistólica** | **25.8%** | █████████ |
| **IMC** | **10.9%** | ████ |
| **colesterol** | **10.6%** | ███ |
| **frecuencia_cardiaca** | **9.9%** | ███ |
| **edad** | **8.9%** | ███ |

## 5. Predicción Individual — Ejemplos

### Ejemplo 1: Paciente Crítico
```json
{
  "edad": 72,
  "IMC": 35.2,
  "glucosa": 380.5,
  "colesterol": 265.0,
  "presión_sistólica": 195,
  "frecuencia_cardiaca": 102
}
```
**Resultado:**
```json
{
  "riesgo_predicho": "Crítico",
  "probabilidades": {
    "Bajo": 0.0,
    "Medio": 0.0,
    "Alto": 0.05,
    "Crítico": 0.95
  }
}
```

### Ejemplo 2: Paciente Riesgo Bajo
```json
{
  "edad": 28,
  "IMC": 21.5,
  "glucosa": 95.0,
  "colesterol": 160.0,
  "presión_sistólica": 110,
  "frecuencia_cardiaca": 72
}
```
**Resultado:**
```json
{
  "riesgo_predicho": "Bajo",
  "probabilidades": {
    "Bajo": 0.82,
    "Medio": 0.12,
    "Alto": 0.04,
    "Crítico": 0.02
  }
}
```

## 6. Archivos Generados

| Archivo | Descripción | Tamaño |
|---|---|---|
| `ml/risk_model.pkl` | Modelo RandomForest serializado | ~4.7 MB |
| `ml/label_encoder.pkl` | LabelEncoder para decodificar clases | ~506 B |

## 7. Historial de Entrenamiento

Cada entrenamiento queda registrado en la tabla `ml_mlmetrics`:
- Fecha y hora
- Usuario que ejecutó
- Métricas (accuracy, precision, recall, f1_score)
- Matriz de confusión (JSON)
- Importancia de variables (JSON)
- Configuración del modelo
- Tamaño de datasets (train/test)
