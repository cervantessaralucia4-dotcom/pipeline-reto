import pandas as pd
import numpy as np


def clean_diagnosis(value):

    value = str(value).lower().strip()

    replacements = {
        'hipertencion': 'hipertensión',
        'hipertensíon': 'hipertensión',
        'hipertension': 'hipertensión',
    }

    return replacements.get(value, value)


def classify_risk(row):

    if (
        row['glucosa'] > 300 or
        row['presión_sistólica'] > 180 or
        row['saturación_oxígeno'] < 85
    ):
        return 'Crítico'

    elif (
        row['glucosa'] > 200 or
        row['presión_sistólica'] > 160
    ):
        return 'Alto'

    elif (
        row['glucosa'] > 140 or
        row['presión_sistólica'] > 140
    ):
        return 'Medio'

    return 'Bajo'


def run_etl():

    file_path = 'datasets/dataset_clinico_etl_1800_registros.xlsx'

    df = pd.read_excel(file_path)

    print("\nDATASET ORIGINAL")
    print(df.shape)

    # =========================
    # ELIMINAR DUPLICADOS
    # =========================

    duplicates_before = df.duplicated().sum()

    df = df.drop_duplicates()

    duplicates_after = df.duplicated().sum()

    print(f"\nDuplicados eliminados: {duplicates_before}")
    print(f"Duplicados restantes: {duplicates_after}")

    # =========================
    # CONVERTIR TIPOS
    # =========================

    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')

    df['presión_sistólica'] = pd.to_numeric(
        df['presión_sistólica'],
        errors='coerce'
    )

    # =========================
    # TRATAMIENTO NULOS
    # =========================

    df['peso'] = df['peso'].fillna(df['peso'].median())

    df['glucosa'] = df['glucosa'].fillna(df['glucosa'].mean())

    df['colesterol'] = df['colesterol'].fillna(
        df['colesterol'].mean()
    )

    df['temperatura'] = df['temperatura'].fillna(
        df['temperatura'].median()
    )

    df['edad'] = df['edad'].fillna(
    df['edad'].median()
)

    df['presión_sistólica'] = df[
    'presión_sistólica'
    ].fillna(
        df['presión_sistólica'].median()
)

    # =========================
    # LIMPIAR DIAGNÓSTICOS
    # =========================

    df['diagnóstico_preliminar'] = df[
        'diagnóstico_preliminar'
    ].apply(clean_diagnosis)

    # =========================
    # VALIDAR RANGOS
    # =========================

    df = df[
        (df['peso'] > 30) &
        (df['peso'] < 250)
    ]

    df = df[
        (df['temperatura'] > 34) &
        (df['temperatura'] < 42)
    ]

    # =========================
    # RECALCULAR IMC
    # =========================

    df['IMC'] = round(
        df['peso'] / (df['altura'] ** 2),
        2
    )

    # =========================
    # CLASIFICAR RIESGO
    # =========================

    df['riesgo_calculado'] = df.apply(
        classify_risk,
        axis=1
    )

    # =========================
    # RESULTADO FINAL
    # =========================

    print("\nDATASET LIMPIO")
    print(df.head())

    print("\nTIPOS FINALES")
    print(df.dtypes)

    print("\nNULOS FINALES")
    print(df.isnull().sum())

    print("\nSHAPE FINAL")
    print(df.shape)

    # =========================
    # EXPORTAR CSV LIMPIO
    # =========================

    df.to_csv(
        'datasets/clean_clinical_dataset.csv',
        index=False
    )

    print("\nCSV limpio exportado correctamente")


if __name__ == "__main__":
    run_etl()