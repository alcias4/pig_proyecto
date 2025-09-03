import pandas as pd
import streamlit as st


from src.page.pigmento_one import page_pigmento_one
from src.page.pigmentos_mez import page_pigmentos_mezclas


def main():
    st.title("Cálculo de CIELAB")

    st.set_page_config(page_title="Protela CIELAB", layout="centered")

    tabs = st.tabs(["🧪 un solo  pigmento", "🧪🧪  Pruebas Mezcla"])

    with tabs[0]:
        page_pigmento_one()

    with tabs[1]:
        page_pigmentos_mezclas()


if __name__ == "__main__":
    main()
