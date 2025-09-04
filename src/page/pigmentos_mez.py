import streamlit as st


def page_pigmentos_mezclas():
    st.markdown("""
# Informe de Estandarización de Matizadas

## Objetivo
Estandarizar el procedimiento de arreglos por pigmentos para **minimizar intentos** y **asegurar reprocesos exitosos**, corrigiendo los desfases observados entre **laboratorio** y **planta**.

---

## Hallazgos (junio–agosto)
- **Arrastre en ramas:** variabilidad ~**10%** semana a semana y **5–12%** entre **orillos** y **centro**.  
  En **laboratorio** es estable (variaciones **<5%** entre orillos y centro). *(Ver Figuras 1, 2 y 3).*
- **Temperatura de acabado:** la temperatura final en **ramas** no siempre coincide con la usada en **laboratorio**.
- **Preparación del baño:**
  - **Laboratorio:** pigmentos **diluidos al 0,5%**.
  - **Ramas:** productos **puros** → exige mayor exactitud al dosificar.
- **Lotes de pigmento diferentes** entre ramas y laboratorio → **matices distintos** al validar reproducibilidad.

> Se han mejorado los puntos **2, 3 y 4** alineando condiciones entre laboratorio y ramas.

---

## Estándar de arrastre propuesto
- Literatura para acabados: **arrastre 70–100%**.  
  *Advertencia:* arrastres muy altos favorecen **desigualdad** por evaporación: la solución migra hacia el exterior, dejando **mayor concentración** en superficie y **menor** en el interior.
- **Recomendación:** trabajar con **70%** de arrastre objetivo para minimizar el fenómeno.  
  Dado lo observado (Fig. 1–2), fijar **rango 70–80%** y **máxima diferencia 5%** entre **orillos** y **centro**.

---

## Estudio de caso (Ref. 100575, color U425613)
Se realizaron varias muestras para evaluar el **comportamiento del matiz** al incrementar la **concentración** de pigmento.

- Se evidenció un **comportamiento fuertemente lineal**.
- Es posible **estimar la concentración requerida** en teñidos con pigmento.
- Se implementó **interpolación polinómica de Lagrange** como **modelo predictivo**, útil cuando solo se tienen **mediciones puntuales** de **Concentración** y **DL\\***, **Da\\***, **Db\\***, construyendo una **curva continua** para predecir valores **intermedios**.

**Interfaz:**  
https://pigproyecto-fuvqtszco5ow2dgyahutdx.streamlit.app/

---

## Consideraciones y limitaciones
- **Rango válido del modelo:** funciona hasta **15 g** de pigmento (**3 g** de pigmento al **0,5%**).  
  Por encima de ese valor **cambia el modelo** y pueden aparecer diferencias al matizar.
- **Secado en rama (laboratorio):** mínimo **90 s** (equivale a velocidad **12–14 m/s**).
- **Flujo de validación:**
  1. Montajes y modelamiento con **pigmentos de laboratorio**.  
  2. Confirmación con **baño preparado en ramas** del montaje aprobado.  
  3. Si hay ajustes de pigmento, realizarlos con los de laboratorio y **revalidar** con baño de ramas.
- **Datos mínimos para predicción:**
  - **1 pigmento:** al menos **3 puntos** (Lote, **7,5 g**, **15 g**).  
  - **2 pigmentos:** **4 puntos** (Lote, **15 g** del pigmento 1, **15 g** del pigmento 2, y **5 g + 5 g**).

---

## Recomendaciones y advertencias
- **Suministros:**
  - Preparar **semanalmente** los pigmentos diluidos.  
  - Traer **mensualmente** nuevas muestras de **pigmento puro** de estampación para homogenizar **ramas** y **laboratorio**.
- **Limpieza de foulard:** usar **detergente** después de matizar con **PIG-00004, PIG-00016, PIG-00034, PIG-00056, PIG-00059**.
- **Diagnóstico de lecturas atípicas:** pueden deberse a **foulard contaminado**, **pigmento en mal estado** o **calibración** del **Datacolor**.
- **Termocromismo:** colores **beige** y **chocolates**, y telas de **alto gramaje**, muestran cambio de matiz tras matizar.  
  → **Enfriar 1 hora** antes de leer en **Datacolor**.
- **Volumen mínimo en ramas:** **≥ 50 L** para tomar muestra y desarrollar en laboratorio.  
  Volúmenes inferiores **no garantizan reproducibilidad**.
- **Muestreo de la pieza:** tomar muestra **previa** para conocer lecturas actuales; la tela puede diferir del desarrollo de laboratorio y requerir **ajustes** de cantidad y **color** del pigmento.
- **Incidencias:** en **Ref. 301172 (MYD)** se observaron **precipitaciones** durante matizada en ramas.  
  → **Parar**, **reemplazar filtro** y **limpiar foulard**.
- **Trazabilidad de matices:** almacenar **DL\\***, **Da\\***, **Db\\*** del **lote sin matizar** y del **montaje aprobado** para:
  - usar en predicciones futuras,
  - habilitar **modelos más elaborados** (p. ej., **redes neuronales**) que reduzcan montajes y mejoren la comprensión **pigmento–tela**.

---

## Resumen ejecutivo
- **Normalizar arrastre** a **70–80%** con **≤ 5%** de diferencia orillos–centro.  
- **Alinear condiciones** entre laboratorio y ramas (temperatura, preparación, lotes).  
- **Usar modelos predictivos** (Lagrange) dentro del rango de **hasta 15 g** para reducir intentos.  
- **Mantener disciplina operativa** (limpieza, volúmenes, muestreo, control de lotes) para asegurar **reproducibilidad**.
""")
