# Guía de Capturas de Pantalla para Evidencias

A continuación se listan las capturas recomendadas para documentar el funcionamiento del sistema.

## 1. Login

| # | Pantalla | Descripción |
|---|---|---|
| 1 | Login | Página de inicio de sesión con campos de usuario y contraseña |
| 2 | Login exitoso | Dashboard principal después de autenticarse con admin_ips |

## 2. Dashboard Principal

| # | Pantalla | Descripción |
|---|---|---|
| 3 | Dashboard | Vista completa con KPIs (7 tarjetas), gráfica de pastel, gráfica de barras e indicadores clínicos |
| 4 | Dashboard — KPIs | Acercamiento a las tarjetas de indicadores clave |

## 3. Pacientes

| # | Pantalla | Descripción |
|---|---|---|
| 5 | Lista de pacientes | Tabla con paginación, búsqueda y ordenamiento |
| 6 | Búsqueda | Resultados filtrados por nombre o riesgo |

## 4. ETL

| # | Pantalla | Descripción |
|---|---|---|
| 7 | ETL — antes de ejecutar | Sección ETL con botón "Ejecutar ETL ahora" |
| 8 | ETL — ejecutando | Estado "en_proceso" durante la ejecución |
| 9 | ETL — resultado exitoso | Estadísticas post-ejecución (extraídos, duplicados, nulos, etc.) |
| 10 | ETL — historial | Tabla con historial de ejecuciones previas |

## 5. Analytics

| # | Pantalla | Descripción |
|---|---|---|
| 11 | KPIs médicos | Tarjetas interactivas de hipertensos, diabéticos, fumadores, etc. |
| 12 | Modal de filtro | Pacientes que cumplen un criterio (ej: hipertensos) |
| 13 | Estadística descriptiva | Media, mediana, moda, desviación estándar de variables clínicas |
| 14 | Segmentación | Barras de progreso por riesgo, grupo de edad y clasificación IMC |
| 15 | Alertas clínicas | Tarjetas de pacientes críticos (presión > 180, glucosa > 300, saturación < 85%) |

## 6. Machine Learning

| # | Pantalla | Descripción |
|---|---|---|
| 16 | ML — métricas | Accuracy, Precision, Recall, F1 Score del modelo entrenado |
| 17 | ML — importancia | Barras de importancia de variables (glucosa, presión, IMC, etc.) |
| 18 | ML — predicción | Formulario de predicción individual con resultado |
| 19 | ML — historial | Tabla con entrenamientos previos |

## 7. Reportes

| # | Pantalla | Descripción |
|---|---|---|
| 20 | Reportes | Resumen ejecutivo con KPIs y botones de exportación |

## 8. Gestión de Usuarios (Admin)

| # | Pantalla | Descripción |
|---|---|---|
| 21 | Usuarios | Lista de usuarios con roles |
| 22 | Crear usuario | Modal de creación de nuevo usuario |

## 9. Diagramas (adicionales)

| # | Diagrama | Descripción |
|---|---|---|
| 23 | Arquitectura | Diagrama de arquitectura del sistema (backend, frontend, BD) |
| 24 | Flujo ETL | Diagrama de flujo del pipeline ETL |
| 25 | ERD | Diagrama entidad-relación de la base de datos |

---

## Herramientas sugeridas para capturas

- **Windows:** `Win + Shift + S` (Recorte y anotación)
- **Mac:** `Cmd + Shift + 4`
- **Browser:** Extensiones como "Full Page Screen Capture"
- **Diagramas:** Draw.io, LucidChart, o PlantUML
