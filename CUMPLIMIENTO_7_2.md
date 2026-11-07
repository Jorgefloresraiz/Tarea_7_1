# Correspondencia con la consigna

| Requisito | Evidencia |
|---|---|
| Capas, pesos y comparación sobre 200 solicitudes idénticas | resultados72/modelos.json; experimento72.py; informe p. 2 |
| 10 o más solicitudes, rechazos y dos ejemplos reales | 20 generaciones en resultados72/generaciones.jsonl; informe p. 3, casos 1 y 19 |
| Afirmación falsa aceptada por el original | caso 3, saldo negativo negado; informe p. 3 |
| Regla texto contra datos y tono 30–60 % | verificador.py |
| Pruebas de ambas reglas y originales | tests/test_reglas72.py; tests/test_hibrido.py; resultados72/pytest.txt |
| Comparación antes/después y falsos positivos | resultados72/rechazos.csv, revision_semantica.json, controles_correctos.json; informe p. 4 |
| Límites y recomendación bancaria | informe p. 4; README_7_2.md |
| Bitácora e informe de tres páginas APA | documentos72/; informe con portada y referencias adicionales |

Las valoraciones de corrección semántica son asistidas y revisables, no una evaluación humana independiente. El experimento es de desarrollo: no se afirma generalización de las reglas.
