# ═══════════════════════════════════════════════════════════════
#  etl/etl_process.py
#  Pipeline ETL completo para el dataset clínico.
#  Retorna un dict con estadísticas para guardarlo en ETLLog.
# ═══════════════════════════════════════════════════════════════
import time
import pandas as pd
import numpy as np


# ── Mapas de normalización ────────────────────────────────────

SEXO_MAP = {
    'm': 'M', 'masculino': 'M', 'Masculino': 'M',
    'f': 'F', 'femenino':  'F', 'Femenino':  'F',
}

DIAGNOSTICO_MAP = {
    'hipertencion':  'Hipertensión',
    'hipertensíon':  'Hipertensión',
    'hipertension':  'Hipertensión',
    'hipertensión':  'Hipertensión',
    'diabetes tipo 2': 'Diabetes Tipo 2',
    'paciente sano':   'Paciente sano',
    'riesgo cardiovascular': 'Riesgo cardiovascular',
    'obesidad':        'Obesidad',
    'prehipertensión': 'Prehipertensión',
    'cardiopatía':     'Cardiopatía',
    'prehipertension': 'Prehipertensión',
}

ACTIVIDAD_MAP = {
    'sedentario': 'Baja',
    'baja':       'Baja',
    'media':      'Media',
    'alta':       'Alta',
}


# ── Funciones auxiliares ──────────────────────────────────────

def normalizar_sexo(valor):
    if pd.isna(valor):
        return 'M'
    return SEXO_MAP.get(str(valor).strip(), str(valor).strip().upper()[:1])


def normalizar_diagnostico(valor):
    if pd.isna(valor):
        return 'Sin diagnóstico'
    v = str(valor).strip().lower()
    return DIAGNOSTICO_MAP.get(v, str(valor).strip().capitalize())


def normalizar_actividad(valor):
    if pd.isna(valor):
        return 'Media'
    v = str(valor).strip().lower()
    return ACTIVIDAD_MAP.get(v, str(valor).strip().capitalize())


def calcular_imc(peso, altura):
    try:
        if altura and altura > 0:
            return round(float(peso) / (float(altura) ** 2), 2)
    except Exception:
        pass
    return None


def clasificar_riesgo(row):
    """Reglas clínicas para clasificar nivel de riesgo."""
    try:
        glucosa  = float(row['glucosa'])
        pres_sis = float(row['presión_sistólica'])
        sat_o2   = float(row['saturación_oxígeno'])

        if glucosa > 300 or pres_sis > 180 or sat_o2 < 85:
            return 'Crítico'
        if glucosa > 200 or pres_sis > 160:
            return 'Alto'
        if glucosa > 140 or pres_sis > 140:
            return 'Medio'
        return 'Bajo'
    except Exception:
        return 'Bajo'


# ── Pipeline principal ────────────────────────────────────────

def run_etl(file_path='datasets/dataset_clinico_etl_1800_registros.xlsx'):
    """
    Ejecuta el pipeline ETL completo.
    Retorna un dict con estadísticas y el DataFrame limpio.
    """
    stats = {
        'archivo_fuente':       file_path,
        'registros_extraidos':  0,
        'registros_duplicados': 0,
        'registros_nulos':      0,
        'registros_fuera_rango': 0,
        'registros_cargados':   0,
        'mensaje':              '',
        'tiempo_ejecucion':     0,
        'df_limpio':            None,
    }

    t_inicio = time.time()

    # ══════════════════════════════════════
    # 1. EXTRACT
    # ══════════════════════════════════════
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
    except Exception as e:
        stats['mensaje'] = f'Error al leer el archivo: {e}'
        return stats

    stats['registros_extraidos'] = len(df)

    # ══════════════════════════════════════
    # 2. TRANSFORM
    # ══════════════════════════════════════

    # ── 2a. Eliminar duplicados ───────────
    antes = len(df)
    df = df.drop_duplicates()
    stats['registros_duplicados'] = antes - len(df)

    # ── 2b. Convertir tipos de datos ──────
    # edad: puede contener 'Treinta', 'cuarenta', etc.
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')

    # presión_sistólica: puede contener 'Alta', 'baja'
    df['presión_sistólica'] = pd.to_numeric(df['presión_sistólica'], errors='coerce')

    # Asegurar numéricos en el resto de columnas clínicas
    for col in ['peso', 'altura', 'IMC', 'presión_diastólica',
                'frecuencia_cardiaca', 'glucosa', 'colesterol',
                'saturación_oxígeno', 'temperatura']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # ── 2c. Tratar valores nulos ──────────
    nulos_antes = df.isnull().sum().sum()

    df['glucosa']           = df['glucosa'].fillna(df['glucosa'].mean())
    df['colesterol']        = df['colesterol'].fillna(df['colesterol'].mean())
    df['peso']              = df['peso'].fillna(df['peso'].median())
    df['temperatura']       = df['temperatura'].fillna(df['temperatura'].median())
    df['edad']              = df['edad'].fillna(df['edad'].median())
    df['presión_sistólica'] = df['presión_sistólica'].fillna(df['presión_sistólica'].median())

    # Booleanos: llenar con moda
    for col in ['antecedentes_familiares', 'fumador', 'consumo_alcohol']:
        df[col] = df[col].fillna(df[col].mode()[0])

    stats['registros_nulos'] = int(nulos_antes)

    # ── 2d. Validar rangos clínicos ────────
    fuera_rango = 0
    mask_peso  = ~((df['peso'] > 30) & (df['peso'] < 300))
    mask_temp  = ~((df['temperatura'] > 34) & (df['temperatura'] < 42))
    mask_glucosa = ~((df['glucosa'] >= 20) & (df['glucosa'] <= 600))
    fuera_rango = int(mask_peso.sum() + mask_temp.sum() + mask_glucosa.sum())
    stats['registros_fuera_rango'] = fuera_rango

    df = df[
        (df['peso'] > 30) & (df['peso'] < 300) &
        (df['temperatura'] > 34) & (df['temperatura'] < 42) &
        (df['glucosa'] >= 20) & (df['glucosa'] <= 600)
    ]

    # ── 2e. Normalizar variables categóricas
    df['sexo']                  = df['sexo'].apply(normalizar_sexo)
    df['diagnóstico_preliminar'] = df['diagnóstico_preliminar'].apply(normalizar_diagnostico)
    df['actividad_física']      = df['actividad_física'].apply(normalizar_actividad)

    # ── 2f. Recalcular IMC ─────────────────
    df['IMC'] = df.apply(
        lambda r: calcular_imc(r['peso'], r['altura']), axis=1
    )

    # ── 2g. Clasificar riesgo calculado ────
    df['riesgo_calculado'] = df.apply(clasificar_riesgo, axis=1)

    # ── 2h. Eliminar filas con nulos críticos
    df = df.dropna(subset=['nombres', 'apellidos', 'edad', 'sexo'])

    # ══════════════════════════════════════
    # 3. LOAD — exportar CSV limpio
    # ══════════════════════════════════════
    output_path = 'datasets/clean_clinical_dataset.csv'
    df.to_csv(output_path, index=False)

    stats['registros_cargados'] = len(df)
    stats['tiempo_ejecucion']   = round(time.time() - t_inicio, 2)
    stats['mensaje']            = (
        f"ETL completado. Extraídos: {stats['registros_extraidos']} | "
        f"Duplicados eliminados: {stats['registros_duplicados']} | "
        f"Nulos tratados: {stats['registros_nulos']} | "
        f"Fuera de rango: {stats['registros_fuera_rango']} | "
        f"Cargados: {stats['registros_cargados']} | "
        f"Tiempo: {stats['tiempo_ejecucion']}s"
    )
    stats['df_limpio'] = df

    return stats


if __name__ == '__main__':
    resultado = run_etl()
    print(resultado['mensaje'])