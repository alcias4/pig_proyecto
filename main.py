import pandas as pd
import streamlit as st

from src.logic.one_pig import one_pig


# --- Util: parsea "1.23" o "1,23" a float; None si está vacío o mal ---
def parse_float(s: str):
    if s is None:
        return None
    s = str(s).strip()
    if s == "":
        return None
    try:
        return float(s.replace(",", "."))
    except Exception:
        return None


def main():
    st.set_page_config(
        page_title="Cálculo de pruebas de lab",
        page_icon="🧪",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.title("Cálculo de pruebas de lab")

    # ---- Estado global ----
    if "pruebas" not in st.session_state:
        st.session_state.pruebas = {}  # id -> {"P": {...}}

    # Inputs de texto y estado de predicción
    defaults = {
        "con_t": "",
        "dl_t": "",
        "da_t": "",
        "db_t": "",
        "predics_t": "",
        "pred_ready": False,
        "pred_x": None,
        "_last_error": None,
        "_last_prueba": None,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

    # ---- Nombre de prueba ----
    st.markdown("**Nombre de prueba**")
    nueva_prueba = st.text_input(
        "Nombre de prueba",
        placeholder="Ej: num demanda",
        label_visibility="collapsed",
        key="id_prueba",
    )
    st.divider()

    if not nueva_prueba:
        st.info("Escribe un nombre de prueba para comenzar.")
        return

    # Si cambiaste de prueba, limpia predicción previa
    if st.session_state._last_prueba != nueva_prueba:
        st.session_state.pred_ready = False
        st.session_state.pred_x = None
        st.session_state._last_prueba = nueva_prueba

    st.header(nueva_prueba)

    # Crear bucket una sola vez por id
    st.session_state.pruebas.setdefault(
        nueva_prueba, {"P": {"concentración": [], "DL": [], "DA": [], "DB": []}}
    )

    # ---- Callbacks ----
    def agregar_resultado():
        c = parse_float(st.session_state.con_t)
        dl = parse_float(st.session_state.dl_t)
        da = parse_float(st.session_state.da_t)
        db = parse_float(st.session_state.db_t)
        if c is None or c < 0 or dl is None or da is None or db is None:
            st.session_state["_last_error"] = (
                "Valores inválidos. Revisa que concentración ≥ 0 y Δ* sean numéricos."
            )
            return
        P = st.session_state.pruebas[st.session_state.id_prueba]["P"]
        P["concentración"].append(float(c))
        P["DL"].append(float(dl))
        P["DA"].append(float(da))
        P["DB"].append(float(db))
        # reset inputs de texto
        st.session_state.con_t = st.session_state.dl_t = ""
        st.session_state.da_t = st.session_state.db_t = ""

    def limpiar_todo():
        st.session_state.pruebas[st.session_state.id_prueba]["P"] = {
            "concentración": [],
            "DL": [],
            "DA": [],
            "DB": [],
        }
        st.session_state.con_t = st.session_state.dl_t = ""
        st.session_state.da_t = st.session_state.db_t = ""
        # limpiar predicción también
        st.session_state.pred_ready = False
        st.session_state.pred_x = None

    def trigger_pred():
        x = parse_float(st.session_state.predics_t)
        if x is None or x < 0:
            st.session_state["_last_error"] = (
                "La concentración para predecir debe ser numérica y ≥ 0."
            )
            return
        st.session_state.pred_x = float(x)
        st.session_state.pred_ready = True  # marcar que hay predicción

    # ---- Entradas (TEXTO) ----
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.text_input("Concentración (g/mL)", key="con_t", placeholder="ej: 0.80")
    with c2:
        st.text_input("ΔL", key="dl_t", placeholder="ej: -0.70")
    with c3:
        st.text_input("Δa", key="da_t", placeholder="ej: 0.45")
    with c4:
        st.text_input("Δb", key="db_t", placeholder="ej: -0.79")

    # Habilitar/Deshabilitar botón Agregar según validación rápida
    conc_v = parse_float(st.session_state.con_t)
    dl_v = parse_float(st.session_state.dl_t)
    da_v = parse_float(st.session_state.da_t)
    db_v = parse_float(st.session_state.db_t)
    can_add = (
        (conc_v is not None and conc_v >= 0)
        and (dl_v is not None)
        and (da_v is not None)
        and (db_v is not None)
    )

    col_add, col_clear = st.columns(2)
    with col_add:
        st.button(
            "Agregar Resultado",
            use_container_width=True,
            type="primary",
            on_click=agregar_resultado,
            key="btn_agregar",
            disabled=not can_add,
        )
    with col_clear:
        st.button(
            "Limpiar tabla",
            use_container_width=True,
            on_click=limpiar_todo,
            key="btn_limpiar",
        )

    # Mensajes de error (si los hay)
    if st.session_state["_last_error"]:
        st.error(st.session_state["_last_error"])
        st.session_state["_last_error"] = None  # consumir mensaje

    # ---- Tabla acumulada ----
    df = pd.DataFrame(st.session_state.pruebas[nueva_prueba]["P"])
    st.dataframe(df, hide_index=True, use_container_width=True)

    # ---- Predicción persistente debajo del botón ----
    st.subheader("Predicción con una concentración")
    st.text_input(
        "Concentración para predecir", key="predics_t", placeholder="ej: 1,20"
    )

    pred_v = parse_float(st.session_state.predics_t)
    st.button(
        "Calcular predicción",
        use_container_width=True,
        key="btn_pred",
        disabled=not (pred_v is not None and pred_v >= 0),
        on_click=trigger_pred,
    )

    # Contenedor fijo para el resultado (permanece en cada rerun)
    pred_out = st.container()

    if st.session_state.pred_ready and st.session_state.pred_x is not None:
        df_local = pd.DataFrame(
            st.session_state.pruebas[st.session_state.id_prueba]["P"]
        )

        # Ideal: tu one_pig debe aceptar 'out=' para pintar aquí
        try:
            one_pig(df_local, st.session_state.pred_x, out=pred_out)
        except TypeError:
            # Compatibilidad si aún no aceptas 'out'
            with pred_out:
                one_pig(df_local, st.session_state.pred_x)


if __name__ == "__main__":
    main()
