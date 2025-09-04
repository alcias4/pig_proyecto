import numpy as np
import pandas as pd


# ---------- utilidades polinomio 2D (grado total) ----------
def _terms_total_degree(deg: int):
    return [(i, j) for i in range(deg + 1) for j in range(deg + 1 - i)]


def _design_matrix(x, y, terms):
    x = np.asarray(x, float).ravel()
    y = np.asarray(y, float).ravel()
    return np.column_stack([(x**i) * (y**j) for (i, j) in terms])


def polyfit2d(x, y, z, deg=1):
    terms = _terms_total_degree(deg)
    Phi = _design_matrix(x, y, terms)
    c, *_ = np.linalg.lstsq(Phi, np.asarray(z, float).ravel(), rcond=None)
    return c, terms


def polyval2d(x, y, coefs, terms):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    out = 0.0
    for a, (i, j) in zip(coefs, terms):
        out += a * (x**i) * (y**j)
    return out


def _n_terms(deg: int) -> int:
    # número de términos de grado total <= deg en 2D
    return (deg + 1) * (deg + 2) // 2


# ---------- capa DL/DA/DB con autocap del grado ----------
def fit_models_2d(
    df: pd.DataFrame, deg=1, xcol="P1", ycol="P2", targets=("DL", "DA", "DB")
):
    n = len(df)
    # auto-limita: requiere al menos n_terms puntos
    while _n_terms(deg) > n and deg > 0:
        deg -= 1
    if _n_terms(deg) > n:
        raise ValueError("No hay puntos suficientes ni para deg=0.")

    models = {}
    x = df[xcol].to_numpy(float)
    y = df[ycol].to_numpy(float)
    for t in targets:
        z = df[t].to_numpy(float)
        coefs, terms = polyfit2d(x, y, z, deg=deg)
        models[t] = (coefs, terms)
    return models, deg


def predict_table_2d(models: dict, x_new: float, y_new: float, pct=0.08):
    base = {t: float(polyval2d(x_new, y_new, *models[t])) for t in models.keys()}
    row_base = {
        "x": round(x_new, 3),
        "y": round(y_new, 3),
        **{t: round(v, 3) for t, v in base.items()},
    }
    row_plus = {
        "x": "mas",
        "y": "",
        **{t: round(v + pct * abs(v), 3) for t, v in base.items()},
    }
    row_minus = {
        "x": "menos",
        "y": "",
        **{t: round(v - pct * abs(v), 3) for t, v in base.items()},
    }
    return pd.DataFrame(
        [row_base, row_plus, row_minus], columns=["x", "y", "DL", "DA", "DB"]
    )


# ---------- EJEMPLO con SOLO 4 mezclas ----------
df = pd.DataFrame(
    {
        "P1": [0, 1, 3, 0],
        "P2": [3, 1, 0, 0],
        "DL": [0.8, 0.2, -0.3, 0.0],
        "DA": [-0.5, -0.1, 0.4, 0.0],
        "DB": [0.9, 0.3, -0.2, 0.0],
    }
)

models, used_deg = fit_models_2d(
    df, deg=1, xcol="P1", ycol="P2"
)  # con 4 puntos => deg=1
tabla = predict_table_2d(models, x_new=1.2, y_new=0.8, pct=0.08)
print(f"Grado usado: {used_deg}")
print(tabla)
