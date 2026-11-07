"""Paso 4 · Verificar la capa generativa: que el texto no afirme nada que el modelo no sustente."""
import re


def _numeros(texto):
    """Todos los números que aparecen en un texto, como conjunto de floats."""
    return {float(n.replace(",", ".")) for n in re.findall(r"\d+(?:[.,]\d+)?", texto)}


def verificar_numeros(texto, datos, prob):
    """Devuelve una lista de problemas: números del texto que no vienen de los datos ni del modelo."""
    permitidos = _numeros(" ".join(str(v) for v in datos.values())) | {float(round(prob * 100))}
    return [f"número no sustentado: {n:g}" for n in sorted(_numeros(texto) - permitidos)]


def verificar_tono(texto, prob):
    """Devuelve una lista de problemas: el tono no coincide con la probabilidad, o hay afirmaciones absolutas."""
    t = texto.lower()
    problemas = []
    if prob < 0.30 and "alto" in t:
        problemas.append("dice que el riesgo es alto, pero la probabilidad es baja")
    if prob > 0.60 and "bajo" in t:
        problemas.append("dice que el riesgo es bajo, pero la probabilidad es alta")
    for absoluta in ("garantiza", "garantizado", "sin riesgo", "seguro que", "imposible", "nunca", "siempre"):
        if absoluta in t:
            problemas.append(f"afirmación absoluta: '{absoluta}'")
    return problemas


def explicacion_segura(datos, prob):
    """Texto de respaldo, armado solo con datos y la probabilidad. No usa el modelo de lenguaje."""
    nivel = "bajo" if prob < 0.30 else ("medio" if prob <= 0.60 else "alto")
    detalle = ", ".join(f"{k}: {v}" for k, v in datos.items())
    return f"El modelo estima una probabilidad de {prob:.0%} de que el crédito sea malo (riesgo {nivel}). Datos: {detalle}."


def verificar_datos(texto, datos):
    """Contrasta afirmaciones explícitas de cuenta y vivienda; no infiere causas."""
    t = texto.lower()
    problemas = []
    if 'sin saldo negativo' in t and datos.get('cuenta corriente') == 'saldo negativo':
        problemas.append('dato contradictorio: niega el saldo negativo registrado')
    opciones = {'cuenta corriente': ['saldo negativo', 'saldo entre 0 y 200', 'saldo de 200 o más', 'sin cuenta corriente'],
                'vivienda': ['propia', 'alquilada', 'sin costo']}
    for campo, valores in opciones.items():
        for valor in valores:
            patron = re.escape(valor) if campo == 'cuenta corriente' else r'vivienda\s+' + re.escape(valor)
            for m in re.finditer(patron, t):
                # Negaciones simples no afirman que el atributo esté presente.
                previo = t[max(0, m.start()-25):m.start()]
                if re.search(r'(?:\bsin\s+|\bno\s+(?:tiene\s+|presenta\s+|es\s+)?(?:un[ao]?\s+)?)$', previo):
                    continue
                if datos.get(campo) != valor:
                    problemas.append(f"dato contradictorio: {campo} afirma '{valor}', dato '{datos.get(campo)}'")
    return problemas


def verificar_tono_medio(texto, prob):
    """En [30%,60%], detecta extremos expresados explícitamente como riesgo."""
    if not .30 <= prob <= .60:
        return []
    t = texto.lower()
    patron = r'\b(?:riesgo\s+(?:(?:es|muy|de crédito|crediticio)\s+)*|lo cual es\s+)(alto|bajo|elevado|mínimo)\b'
    problemas = []
    for m in re.finditer(patron, t):
        previo=t[max(0,m.start()-10):m.start()]
        if re.search(r'\bno\s+(?:es\s+)?$', previo):
            continue
        problemas.append('tono incoherente: riesgo extremo en probabilidad intermedia')
    return problemas


def verificar_explicacion(texto, datos, prob):
    return (verificar_numeros(texto, datos, prob) + verificar_tono(texto, prob)
            + verificar_datos(texto, datos) + verificar_tono_medio(texto, prob))
