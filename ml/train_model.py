import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from sklearn.preprocessing import LabelEncoder


def train_model():

    file_path = 'datasets/clean_clinical_dataset.csv'

    df = pd.read_csv(file_path)

    # =========================
    # VARIABLES
    # =========================

    features = [
        'edad',
        'IMC',
        'glucosa',
        'colesterol',
        'presión_sistólica',
        'frecuencia_cardiaca'
    ]

    target = 'riesgo_calculado'

    # =========================
    # LIMPIAR NULOS
    # =========================

    df = df.dropna(subset=features)

    # =========================
    # X & Y
    # =========================

    X = df[features]

    y = df[target]

    # =========================
    # ENCODE TARGET
    # =========================

    encoder = LabelEncoder()

    y_encoded = encoder.fit_transform(y)

    joblib.dump(
    encoder,
    'ml/label_encoder.pkl'
)

    # =========================
    # TRAIN TEST SPLIT
    # =========================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.2,
        random_state=42
    )

    # =========================
    # MODEL
    # =========================

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    # =========================
    # GUARDAR MODELO
    # =========================

    joblib.dump(model, 'ml/risk_model.pkl')

    print("\nModelo guardado correctamente")

    # =========================
    # PREDICCIONES
    # =========================

    y_pred = model.predict(X_test)

    # =========================
    # MÉTRICAS
    # =========================

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        average='weighted'
    )

    recall = recall_score(
        y_test,
        y_pred,
        average='weighted'
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average='weighted'
    )

    matrix = confusion_matrix(y_test, y_pred)

    print("\n===== MACHINE LEARNING =====")

    print(f"\nAccuracy: {accuracy:.4f}")

    print(f"Precision: {precision:.4f}")

    print(f"Recall: {recall:.4f}")

    print(f"F1 Score: {f1:.4f}")

    print("\nMATRIZ DE CONFUSIÓN")
    print(matrix)

    print("\nREPORTE")
    print(
        classification_report(
            y_test,
            y_pred
        )
    )


if __name__ == "__main__":
    train_model()