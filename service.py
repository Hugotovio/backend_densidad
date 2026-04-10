from sqlalchemy import text

def interpolar(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))


def obtener_densidad(db, api):
    menor = db.execute(text("""
        SELECT api_observado, densidad_kg_gal
        FROM densidad_api
        WHERE api_observado <= :api
        ORDER BY api_observado DESC
        LIMIT 1
    """), {"api": api}).fetchone()

    mayor = db.execute(text("""
        SELECT api_observado, densidad_kg_gal
        FROM densidad_api
        WHERE api_observado >= :api
        ORDER BY api_observado ASC
        LIMIT 1
    """), {"api": api}).fetchone()

    if not menor or not mayor:
        return None

    # Si coincide exacto
    if menor[0] == mayor[0]:
        return menor[1]

    # Interpolación
    return interpolar(api, menor[0], mayor[0], menor[1], mayor[1])


def obtener_factor(db, temp):
    menor = db.execute(text("""
        SELECT temperatura_f, factor
        FROM factor_conversion
        WHERE temperatura_f <= :temp
        ORDER BY temperatura_f DESC
        LIMIT 1
    """), {"temp": temp}).fetchone()

    mayor = db.execute(text("""
        SELECT temperatura_f, factor
        FROM factor_conversion
        WHERE temperatura_f >= :temp
        ORDER BY temperatura_f ASC
        LIMIT 1
    """), {"temp": temp}).fetchone()

    if not menor or not mayor:
        return None

    # Si coincide exacto
    if menor[0] == mayor[0]:
        return menor[1]

    # Interpolación
    return interpolar(temp, menor[0], mayor[0], menor[1], mayor[1])


def calcular_densidad(db, api, temperatura):
    densidad = obtener_densidad(db, api)
    factor = obtener_factor(db, temperatura)

    if densidad is None or factor is None:
        return None

    return {
        "api": api,
        "temperatura": temperatura,
        "densidad_base": densidad,
        "factor": factor,
        "densidad_corregida": densidad * factor
    }