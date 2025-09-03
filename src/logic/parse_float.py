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
