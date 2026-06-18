# Diagrama Entidad-Relación (ERD)

## Modelo Relacional

```
┌──────────────────────────────────────────────────────────────┐
│                     auth_user                                │
├──────────────────────────────────────────────────────────────┤
│ PK │ id                    │ SERIAL                          │
│    │ username              │ VARCHAR(150) UNIQUE             │
│    │ password              │ VARCHAR(128)                    │
│    │ email                 │ VARCHAR(254)                    │
│    │ first_name            │ VARCHAR(150)                    │
│    │ last_name             │ VARCHAR(150)                    │
│    │ is_superuser          │ BOOLEAN                         │
│    │ is_staff              │ BOOLEAN                         │
│    │ is_active             │ BOOLEAN                         │
│    │ date_joined           │ TIMESTAMPTZ                     │
└──────────┬───────────────────────────────────────────────────┘
           │ 1
           │
           │ 1
┌──────────▼───────────────────────────────────────────────────┐
│              authentication_userprofile                      │
├──────────────────────────────────────────────────────────────┤
│ PK │ id                    │ SERIAL                          │
│ FK │ user_id               │ → auth_user.id (CASCADE)       │
│    │ rol                   │ VARCHAR(20)                     │
│    │                       │ (administrador|medico|analista)  │
│    │ created_at            │ TIMESTAMPTZ                     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    patients_patient                          │
├──────────────────────────────────────────────────────────────┤
│ PK │ id                    │ SERIAL                          │
│    │ first_name            │ VARCHAR(100)                    │
│    │ last_name             │ VARCHAR(100)                    │
│    │ age                   │ INTEGER                         │
│    │ sex                   │ CHAR(1) (M|F)                   │
│    │ weight                │ DOUBLE PRECISION                │
│    │ height                │ DOUBLE PRECISION                │
│    │ bmi                   │ DOUBLE PRECISION NULL           │
│    │ systolic_pressure     │ INTEGER                         │
│    │ diastolic_pressure    │ INTEGER                         │
│    │ heart_rate            │ INTEGER                         │
│    │ glucose               │ DOUBLE PRECISION                │
│    │ cholesterol           │ DOUBLE PRECISION                │
│    │ oxygen_saturation     │ DOUBLE PRECISION                │
│    │ temperature           │ DOUBLE PRECISION                │
│    │ family_history        │ BOOLEAN                         │
│    │ smoker                │ BOOLEAN                         │
│    │ alcohol_consumption   │ BOOLEAN                         │
│    │ physical_activity     │ VARCHAR(20)                     │
│    │ preliminary_diagnosis │ VARCHAR(255)                    │
│    │ disease_risk          │ VARCHAR(20)                     │
│    │ consultation_date     │ DATE                            │
│    │ created_at            │ TIMESTAMPTZ                     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      etl_etllog                              │
├──────────────────────────────────────────────────────────────┤
│ PK │ id                    │ SERIAL                          │
│ FK │ usuario_id            │ → auth_user.id (SET NULL)      │
│    │ fecha_inicio          │ TIMESTAMPTZ                     │
│    │ fecha_fin             │ TIMESTAMPTZ NULL                │
│    │ tiempo_ejecucion      │ DOUBLE PRECISION NULL           │
│    │ registros_extraidos   │ INTEGER                         │
│    │ registros_duplicados  │ INTEGER                         │
│    │ registros_nulos       │ INTEGER                         │
│    │ registros_fuera_rango │ INTEGER                         │
│    │ registros_cargados    │ INTEGER                         │
│    │ estado                │ VARCHAR(20)                     │
│    │ mensaje               │ TEXT                            │
│    │ archivo_fuente        │ VARCHAR(255)                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      ml_mlmetrics                            │
├──────────────────────────────────────────────────────────────┤
│ PK │ id                    │ SERIAL                          │
│ FK │ usuario_id            │ → auth_user.id (SET NULL)      │
│    │ fecha_entrenamiento   │ TIMESTAMPTZ                     │
│    │ accuracy              │ DOUBLE PRECISION                │
│    │ precision             │ DOUBLE PRECISION                │
│    │ recall                │ DOUBLE PRECISION                │
│    │ f1_score              │ DOUBLE PRECISION                │
│    │ confusion_matrix      │ JSONB                           │
│    │ total_registros       │ INTEGER                         │
│    │ registros_train       │ INTEGER                         │
│    │ registros_test        │ INTEGER                         │
│    │ modelo                │ VARCHAR(100)                    │
│    │ features              │ JSONB                           │
│    │ importancia           │ JSONB                           │
└──────────────────────────────────────────────────────────────┘
```

## Relaciones

| Desde | Hacia | Tipo | Descripción |
|---|---|---|---|
| `authentication_userprofile` | `auth_user` | 1:1 | Cada usuario tiene un perfil con rol |
| `etl_etllog` | `auth_user` | N:1 | Un usuario ejecuta múltiples ETL |
| `ml_mlmetrics` | `auth_user` | N:1 | Un usuario entrena múltiples modelos |

## Convenciones

- **PK**: Primary Key (Clave primaria)
- **FK**: Foreign Key (Clave foránea)
- **JSONB**: Datos semiestructurados (matriz de confusión, importancia de variables)
- **CASCADE**: Eliminación en cascada del perfil al eliminar usuario
- **SET NULL**: Al eliminar un usuario, los logs ETL y métricas ML conservan el registro con usuario nulo
