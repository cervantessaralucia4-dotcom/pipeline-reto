# ═══════════════════════════════════════════════════════════════
#  patients/predict.py
#  Carga el modelo entrenado y predice el riesgo de un paciente.
#  Usa el LabelEncoder para devolver la etiqueta correcta.
# ═══════════════════════════════════════════════════════════════
import os
import joblib
import pandas as pd

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH   = os.path.join(BASE_DIR, '..', 'ml', 'risk_model.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, '..', 'ml', 'label_encoder.pkl')

# Carga en módulo (una sola vez al iniciar el servidor)
try:
    _model   = joblib.load(MODEL_PATH)
    _encoder = joblib.load(ENCODER_PATH)
except Exception as e:
    _model   = None
    _encoder = None
    print(f"[WARN] No se pudo cargar el modelo ML: {e}")


def predict_risk(data: dict) -> dict:
    """
    Recibe un dict con los campos del paciente y retorna
    la predicción de riesgo con la probabilidad por clase.
    """
    if _model is None or _encoder is None:
        return {'error': 'Modelo no disponible. Ejecuta el entrenamiento primero.'}

    try:
        df = pd.DataFrame([{
            'edad':                data.get('edad', 0),
            'IMC':                 data.get('IMC', 0),
            'glucosa':             data.get('glucosa', 0),
            'colesterol':          data.get('colesterol', 0),
            'presión_sistólica':   data.get('presión_sistólica', 0),
            'frecuencia_cardiaca': data.get('frecuencia_cardiaca', 0),
        }])

        pred_enc   = _model.predict(df)[0]
        pred_label = _encoder.inverse_transform([pred_enc])[0]

        # Probabilidades por clase
        proba = _model.predict_proba(df)[0]
        prob_dict = {
            label: round(float(p), 4)
            for label, p in zip(_encoder.classes_, proba)
        }

        return {
            'riesgo_predicho': pred_label,
            'probabilidades':  prob_dict,
        }

    except Exception as e:
        return {'error': str(e)}