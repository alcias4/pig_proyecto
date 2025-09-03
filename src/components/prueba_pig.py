import streamlit as st
from ..logic.parse_float import parse_float
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def prueba_pig(id: str, titulo: str):
    st.header(titulo)
    base = f"pig-{id}"

    # ---- Estado persistente ----
    if base not in st.session_state:
        st.session_state[base] = {
            "datos": {
                "Concentración": [],
                "DL": [],
                "DA": [],
                "DB": [],
            }
        }

    st.markdown("##### Agregar puntos para predción")
    with st.form(key=f"{base}-form", clear_on_submit=False):
        con, dl, da, db = st.columns(4)
        with con:
            c = st.text_input("Concentración", placeholder="Ej: 1,3..", key=f"{base}-c")
        with dl:
            dl_dato = st.text_input("DL", placeholder="Ej: 0.70", key=f"{base}-dl")
        with da:
            da_dato = st.text_input("DA", placeholder="Ej: -0.90", key=f"{base}-da")
        with db:
            db_dato = st.text_input("DB", placeholder="Ej: 0.10", key=f"{base}-db")

        agregado = st.form_submit_button("Agregar datos", width="stretch")

    # ---- Lógica de agregado una vez se pulsa el botón del form ----
    if agregado:
        if c and dl_dato and da_dato and db_dato:
            S = st.session_state[base]["datos"]
            S["Concentración"].append(parse_float(c))
            S["DL"].append(parse_float(dl_dato))
            S["DA"].append(parse_float(da_dato))
            S["DB"].append(parse_float(db_dato))
        else:
            st.warning("Completa todos los campos antes de agregar.")

    # ---- DataFrame desde el estado ----
    df = pd.DataFrame(st.session_state[base]["datos"])
    df = df.sort_values(by="Concentración")
    st.dataframe(df, hide_index=True, width="stretch", key=f"{base}-df")
    grado_x = 0
    if not df.empty:
        # Pasar a formato "largo" para Plotly
        df_long = df.melt(
            id_vars="Concentración",
            value_vars=["DL", "DA", "DB"],
            var_name="Variable",
            value_name="Valor",
        )

        # Crear figura
        fig = px.line(
            df_long,
            x="Concentración",
            y="Valor",
            color="Variable",  # cada variable una línea
            markers=True,
            title="Concentración vs DL, DA, DB",
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False,  # oculta toda la barra
                "displaylogo": False,  # (opcional) quita el logo de Plotly
            },
            key=f"{base}-line",
        )

        if len(df["Concentración"]) > 1:
            st.header("Gráfico de comportamiento")
            # Selección de variable
            var = st.selectbox(
                "Variable a ajustar", ["DL", "DA", "DB"], index=0, key=f"{base}-sel"
            )

            # 🔹 Ingreso libre del grado
            grado = st.number_input(
                "Orden del polinomio",
                min_value=1,
                max_value=10,
                value=len(df["Concentración"]) - 1,
                step=1,
                key=f"{base}-grado",
            )
            grado_x = grado
            # Datos
            x = df["Concentración"].to_numpy(dtype=float)
            y = df[var].to_numpy(dtype=float)
            mask = np.isfinite(x) & np.isfinite(y)
            x, y = x[mask], y[mask]

            # Ajuste polinomial
            coef = np.polyfit(x, y, grado)
            p = np.poly1d(coef)

            # Curva suave
            x_line = np.linspace(float(np.min(x)), float(np.max(x)), 200)
            y_line = p(x_line)

            # R^2
            y_pred = p(x)
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2) if len(y) > 1 else 0.0
            r2 = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan

            # Figura
            fig = go.Figure()

            # Puntos medidos
            fig.add_trace(
                go.Scatter(
                    x=x, y=y, mode="markers", name=f"Datos {var}", marker=dict(size=10)
                )
            )

            # Curva ajustada
            fig.add_trace(
                go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode="lines",
                    name=f"Ajuste grado {grado} (R²={r2:.3f})",
                    hovertemplate=f"Coef: {coef}<extra></extra>",
                )
            )

            fig.update_layout(
                title=f"Concentración vs {var} — Ajuste polinomial (grado {grado})",
                xaxis_title="Concentración",
                yaxis_title=var,
            )

            # Mostrar sin barra de herramientas
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False, "displaylogo": False},
                key=f"{base}-rege",
            )
    # ---- Botones de acción ----

    click_cal = st.button(
        "Calcular", key=f"{base}-btn-cal", width="stretch", type="primary"
    )

    x_nuevo = st.number_input(
        "Concentración a predecir", min_value=0.0, step=0.1, key=f"{base}-preidc-n"
    )

    if click_cal:
        if grado_x != 0:
            predicciones = cal_cielba(df, grado_x, x_nuevo)

            # # 🔹 Mostrar como texto
            st.write(f"### Predicciones para concentración {x_nuevo}")
            # st.write(predicciones)

            # 🔹 O más bonito como tabla
            st.dataframe(
                pd.DataFrame(predicciones), key=f"{base}-resul", hide_index=True
            )


def cal_cielba(df, grado, x_nuevo):
    x = df["Concentración"].to_numpy(dtype=float)

    # Ajuste polinomial por variable
    modelos = {}
    for var in ["DL", "DA", "DB"]:
        y = df[var].to_numpy(dtype=float)
        coef = np.polyfit(x, y, grado)
        modelos[var] = np.poly1d(coef)

    # Predicción base
    base = {v: float(modelos[v](x_nuevo)) for v in ["DL", "DA", "DB"]}
    conc_txt = f"x={x_nuevo:g}"

    valor = 0.08
    # Filas (redondeo a 3 decimales). ±8% relativo sobre |valor|
    fila_pred = {
        "con": conc_txt,
        "dl": round(base["DL"], 3),
        "da": round(base["DA"], 3),
        "db": round(base["DB"], 3),
    }
    fila_mas = {
        "con": "mas 8% ajuste de error hacia abajo",
        "dl": round(base["DL"] + valor * abs(base["DL"]), 3),
        "da": round(base["DA"] + valor * abs(base["DA"]), 3),
        "db": round(base["DB"] + valor * abs(base["DB"]), 3),
    }
    fila_menos = {
        "con": "ajuste de error hacia arriba",
        "dl": round(base["DL"] - valor * abs(base["DL"]), 3),
        "da": round(base["DA"] - valor * abs(base["DA"]), 3),
        "db": round(base["DB"] - valor * abs(base["DB"]), 3),
    }

    # DataFrame exactamente con columnas con, dl, da, db
    out = pd.DataFrame(
        [fila_pred, fila_mas, fila_menos], columns=["con", "dl", "da", "db"]
    )
    return out
