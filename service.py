from sqlalchemy import text
import math


# 🔹 truncar a 1 decimal (SIN redondear)
def truncar_1_decimal(valor):
    return math.floor(valor * 10) / 10


# 🔹 obtener densidad (tabla 2)
def obtener_densidad(db, api):
    row = db.execute(text("""
        SELECT densidad_kg_gal
        FROM densidad_api
        WHERE api_observado = :api
    """), {"api": api}).fetchone()

    if not row:
        return None

    return float(row[0])  # 🔥 CLAVE


# 🔹 obtener factor (tabla 1)
def obtener_factor(db, temp):
    row = db.execute(text("""
        SELECT factor
        FROM factor_conversion
        WHERE temperatura_f = :temp
    """), {"temp": temp}).fetchone()

    if not row:
        return None

    return float(row[0])  # 🔥 CORRECCIÓN


# 🔥 FUNCIÓN FINAL (100% SEGÚN TU PDF)
def calcular_densidad(db, api, temperatura):
    # 1. obtener factor
    factor = obtener_factor(db, temperatura)

    if factor is None:
        return None

    # 2. sumar API + factor
    api_corregido = api + factor

    # 3. truncar (NO redondear)
    api_tabla = truncar_1_decimal(api_corregido)

    # 4. buscar densidad exacta
    densidad = obtener_densidad(db, api_tabla)

    if densidad is None:
        return None

    return {
    "api_original": api,
    "temperatura": temperatura,
    "factor": factor,
    "api_corregido": round(api_corregido, 3),
    "api_tabla": api_tabla,

    # 🔥 DENSIDAD EN VARIAS UNIDADES
    "densidad": {
        "kg_gal": round(densidad, 3),
        "kg_m3": round(densidad * 264.172, 2),
        "g_cm3": round(densidad * 0.264172, 4),
        "lb_gal": round(densidad * 2.20462, 3)
    }
}