# ═══════════════════════════════════════════════════════════════
#  ml/train_model.py
#  Entrena el modelo RandomForest, guarda el .pkl
#  y retorna un dict con todas las métricas.
# ═══════════════════════════════════════════════════════════════
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score,
    recall_score, f1_score,
    confusion_matrix, classification_report,
)
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH   = os.path.join(BASE_DIR, 'risk_model.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'label_encoder.pkl')
DATASET_PATH = os.path.join(BASE_DIR, '..', 'datasets', 'clean_clinical_dataset.csv')

FEATURES = [
    'edad', 'IMC', 'glucosa',
    'colesterol', 'presión_sistólica', 'frecuencia_cardiaca',
]
TARGET = 'riesgo_calculado'


def train_model():
    """
    Entrena RandomForest con el dataset limpio.
    Guarda el modelo y el encoder como .pkl.
    Retorna un dict con métricas completas.
    """
    # ── 1. Cargar datos ───────────────────────────────────────
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna(subset=FEATURES)

    X = df[FEATURES]
    y = df[TARGET]

    # ── 2. Encode target ──────────────────────────────────────
    encoder = LabelEncoder()
    y_enc   = encoder.fit_transform(y)
    joblib.dump(encoder, ENCODER_PATH)

    # ── 3. Split ──────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42
    )

    # ── 4. Entrenar ───────────────────────────────────────────
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)

    # ── 5. Evaluar ────────────────────────────────────────────
    y_pred = model.predict(X_test)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1   = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    cm   = confusion_matrix(y_test, y_pred).tolist()

    importancia = {
        feat: round(float(imp), 4)
        for feat, imp in zip(FEATURES, model.feature_importances_)
    }

    reporte_dict = {}
    reporte_str  = classification_report(
        y_test, y_pred,
        target_names=list(encoder.classes_),
        zero_division=0,
    )

    return {
        'accuracy':        round(acc,  4),
        'precision':       round(prec, 4),
        'recall':          round(rec,  4),
        'f1_score':        round(f1,   4),
        'confusion_matrix': cm,
        'clases':          list(encoder.classes_),
        'features':        FEATURES,
        'importancia':     importancia,
        'reporte':         reporte_str,
        'total_registros': len(df),
        'registros_train': len(X_train),
        'registros_test':  len(X_test),
        'modelo':          'RandomForestClassifier',
    }


if __name__ == '__main__':
    resultado = train_model()
    print(f"Accuracy:  {resultado['accuracy']}")
    print(f"Precision: {resultado['precision']}")
    print(f"Recall:    {resultado['recall']}")
    print(f"F1 Score:  {resultado['f1_score']}")
    print("\nImportancia de features:")
    for k, v in resultado['importancia'].items():
        print(f"  {k}: {v}")