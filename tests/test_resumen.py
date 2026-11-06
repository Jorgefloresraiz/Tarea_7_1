import pytest
from resumen_datos import resumir


def test_resumen_dataset():
    r = resumir()
    assert (r['filas'], r['columnas']) == (1000, 21)
    assert r['clases'] == {'bad': 300, 'good': 700}
    assert r['nulos'] == 0


def test_rechaza_etiqueta_desconocida(tmp_path):
    f = tmp_path / 'datos.csv'
    f.write_text('edad,clase\n25,desconocida\n')
    with pytest.raises(ValueError, match='good/bad'):
        resumir(f)


def test_cuenta_nulos_y_duplicados(tmp_path):
    f = tmp_path / 'datos.csv'
    f.write_text('edad,clase\n25,good\n25,good\n,bad\n')
    r = resumir(f)
    assert r['duplicados'] == 1
    assert r['nulos'] == 1
