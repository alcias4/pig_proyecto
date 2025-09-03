import streamlit as st
from ..components.prueba_pig import prueba_pig


def page_pigmento_one():
    st.header("Cálculo simulado con un solo pigmento")

    # ---- Estado persistente de la página ----
    ss = st.session_state
    if "contador" not in ss:
        ss.contador = 0
    if "pruebas" not in ss:
        ss.pruebas = []  # lista de IDs únicos de cada tarjeta
    if "titulos" not in ss:
        ss.titulos = []  # títulos visibles

    # ---- Crear nueva prueba ----
    id_prueba = st.text_input(
        "Nombre de la prueba",
        placeholder="Ejemplo: Número de demanda",
        key="nombre-prueba",
    )

    if st.button(
        "Ingresar prueba", use_container_width=True, key="btn-ingresar-prueba"
    ):
        ss.contador += 1
        base_id = (id_prueba or "Prueba").strip()
        prueba_id = f"{base_id}-{ss.contador}-pig_1"
        ss.titulos.append(base_id)
        ss.pruebas.append(prueba_id)
        st.rerun()

    # ---- Renderizar todas las pruebas creadas ----

    if len(ss.pruebas) >= 1:
        for i, prueba_id in enumerate(ss.pruebas):
            st.divider()

            st.button(
                "Eliminar prueba",
                key=f"btn-eliminar-{i}",
                type="tertiary",
                on_click=_eliminar_por_indice,
                args=(i,),
            )

            prueba_pig(id=prueba_id, titulo=ss.titulos[i])
    else:
        st.info("Agrega una prueba")


def _eliminar_por_indice(idx: int):
    ss = st.session_state

    """Callback que elimina la tarjeta idx de las listas en session_state."""
    if 0 <= idx < len(ss.pruebas):
        ss.pruebas.pop(idx)
        ss.titulos.pop(idx)
