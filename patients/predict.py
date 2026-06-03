import os
import joblib
import pandas as pd


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    'ml',
    'risk_model.pkl'
)

model = joblib.load(MODEL_PATH)


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

    return labels.get(prediction[0], 'Desconocido')