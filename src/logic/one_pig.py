import numpy as np
import pandas as pd
import streamlit as st
from pandas import DataFrame
from scipy.interpolate import BarycentricInterpolator


def one_pig(df: DataFrame, x_p: float, out=None):
    print(df)
    """Predice ΔL, Δa, Δb a la concentración x_p y LO MUESTRA en el contenedor 'out'."""
    # Usa el contenedor pasado; si no, crea uno (pero lo ideal es pasarlo desde main)
    cont = out if out is not None else st.container()
    cont.empty()  # limpia resultados anteriores en ese espacio

    # --- Validación y limpieza ---
    req = ["concentración", "DL", "DA", "DB"]
    if any(c not in df.columns for c in req):
        cont.error(f"Faltan columnas: {req}")
        return

    clean = df.copy()
    for c in req:
        clean[c] = pd.to_numeric(clean[c], errors="coerce")
    clean = clean.dropna(subset=req)
    if clean.empty:
        cont.warning("No hay datos numéricos válidos.")
        return

    # Promedia duplicados y ordena por concentración
    agg = (
        clean.groupby("concentración", as_index=False)
        .mean(numeric_only=True)
        .sort_values("concentración")
        .reset_index(drop=True)
    )

    x = agg["concentración"].to_numpy(float)
    dL = agg["DL"].to_numpy(float)
    da = agg["DA"].to_numpy(float)
    db = agg["DB"].to_numpy(float)

    if len(x) < 2:
        cont.error("Se requieren al menos 2 puntos para interpolar.")
        return

    # --- Interpolación (con respaldo) ---
    try:
        fL = BarycentricInterpolator(x, dL)
        fa = BarycentricInterpolator(x, da)
        fb = BarycentricInterpolator(x, db)
        yL, ya, yb = float(fL(x_p)), float(fa(x_p)), float(fb(x_p))
        metodo = "Lagrange (barycentric)"
        deg = len(x) - 1
    except Exception:
        deg = int(min(2, max(1, len(x) - 1)))
        yL = float(np.poly1d(np.polyfit(x, dL, deg))(x_p))
        ya = float(np.poly1d(np.polyfit(x, da, deg))(x_p))
        yb = float(np.poly1d(np.polyfit(x, db, deg))(x_p))
        metodo = f"Respaldo: polyfit grado {deg}"

    # --- Render en el contenedor anclado ---
    with cont:
        st.markdown(f"**Concentración evaluada:** {x_p:.3f}  \n_Método:_ {metodo}")
        c1, c2, c3 = st.columns(3)
        c1.metric("ΔL pred.", f"{yL:.3f}")
        c2.metric("Δa pred.", f"{ya:.3f}")
        c3.metric("Δb pred.", f"{yb:.3f}")

        xmin, xmax = float(x.min()), float(x.max())
        if not (xmin <= x_p <= xmax):
            st.warning(f"⚠️ Extrapolación (fuera de [{xmin:.3f}, {xmax:.3f}]).")

        # if xmin <= x_p <= xmax:
        #     i_left = np.searchsorted(x, x_p, side="right") - 1
        #     i_right = np.searchsorted(x, x_p, side="left")
        #     i_left = max(i_left, 0)
        #     i_right = min(i_right, len(x) - 1)
        #     # st.caption("Puntos cercanos usados (vecinos):")
        #     # st.dataframe(
        #     #     agg.iloc[sorted(set([i_left, i_right]))],
        #     #     hide_index=True,
        #     #     use_container_width=True,
        #     # )

    return {
        "x": float(x_p),
        "dL": yL,
        "da": ya,
        "db": yb,
        "metodo": metodo,
        "grado": deg,
    }
