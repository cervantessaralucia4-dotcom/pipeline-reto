import joblib
import pandas as pd

# =========================
# CARGAR MODELO
# =========================

model = joblib.load('ml/risk_model.pkl')

# =========================
# PREDICCIÓN
# =========================

def predict_risk(data):

    input_data = pd.DataFrame([{
        'edad': data['edad'],
        'IMC': data['IMC'],
        'glucosa': data['glucosa'],
        'colesterol': data['colesterol'],
        'presión_sistólica': data['presión_sistólica'],
        'frecuencia_cardiaca': data['frecuencia_cardiaca']
    }])

    prediction = model.predict(input_data)

    labels = {
        0: 'Alto',
        1: 'Bajo',
        2: 'Crítico',
        3: 'Medio'
    }

    return labels[prediction[0]]