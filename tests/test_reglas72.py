import pytest
from verificador import verificar_explicacion, verificar_datos, verificar_tono_medio
from verificador_base import verificar_explicacion as base
D={'cuenta corriente':'saldo entre 0 y 200','vivienda':'alquilada'}

def test_cuenta_contradictoria_escapaba_a_base():
    t='El solicitante presenta saldo negativo.'
    assert base(t,D,.45)==[]
    assert any('dato contradictorio' in x for x in verificar_explicacion(t,D,.45))

def test_tono_medio_escapaba_a_base():
    t='El riesgo es alto.'
    assert base(t,D,.45)==[]
    assert verificar_explicacion(t,D,.45)

@pytest.mark.parametrize('p',[.30,.45,.60])
def test_limites_inclusivos(p):
    assert verificar_tono_medio('Riesgo bajo.',p)

@pytest.mark.parametrize('t',['No tiene saldo negativo.','Su vivienda alquilada consta en los datos.','El monto es alto y el riesgo medio.','No es riesgo alto.'])
def test_evitar_falsos_positivos(t):
    assert verificar_datos(t,D)+verificar_tono_medio(t,.45)==[]

def test_vivienda_contradictoria():
    assert verificar_datos('Tiene vivienda propia.',D)

def test_negacion_del_saldo_real_y_tono_generados():
    datos={'cuenta corriente':'saldo negativo','vivienda':'propia'}
    texto='Probabilidad 56%, lo cual es alto; cuenta corriente sin saldo negativo.'
    assert base(texto,datos,.565)==[]
    problemas=verificar_explicacion(texto,datos,.565)
    assert any('niega el saldo' in x for x in problemas)
    assert any('tono incoherente' in x for x in problemas)
