# Tarea 7.2 Aplicación híbrida con verificación

Comparación sobre 200 solicitudes reservadas y verificación antes/después de 20 explicaciones reales de Qwen2.5-0.5B-Instruct. Se parte del commit 4bbce5d de la Tarea 7.1; la rama principal conserva esa entrega.

## Reproducir

Python 3.12. Crear un entorno virtual e instalar `pip install -r requirements72.lock` (versiones observadas en macOS ARM; otras plataformas pueden requerir ajustes).

```
python experimento72.py
python experimento72.py --generar
python evaluar72.py
python auditar_textos72.py
python -m pytest -q
```

La primera generación descarga Qwen (requiere red). El CSV y las solicitudes no se envían a un servicio generativo: la inferencia es local. `HF_HOME` permite seleccionar la caché. El experimento conserva cada resultado en `resultados72/generaciones.jsonl` y reanuda por número de solicitud. Para un experimento nuevo, usar otra copia del proyecto y apartar los resultados anteriores; no mezclar generaciones de distintas versiones.

`python main.py` ejecuta la aplicación sobre 20 solicitudes y muestra texto generado, veredicto y respaldo. La medición controlada utiliza `evaluar72.py` para aplicar ambos verificadores a los mismos textos conservados, sin introducir diferencias por regeneración.

## Evidencia

- `resultados72/modelos.json`: índices de prueba, exactitudes, capas, pesos, sesgos, tiempos y hash del CSV.
- `resultados72/generaciones.jsonl`: texto original y recortado, solicitud, probabilidad y veredicto original.
- `resultados72/rechazos.csv`: comparación por cada una de las 20 solicitudes.
- `resultados72/comparacion.json`: explicación finalmente mostrada, incluido respaldo.
- `resultados72/revision_semantica.json`: valoración asistida de cada texto y justificación; requiere revisión humana independiente antes de uso real.
- `resultados72/controles_correctos.json`: seis textos de control redactados para probar falsos positivos; no son generaciones de Qwen.
- `resultados72/pytest.txt`: 19 pruebas aprobadas, incluidas las cinco originales.
- `documentos72/`: informe y bitácora en Word.

## Resultados y alcance

Random Forest: 75%; MLP: 73,5%, en los mismos 200 casos. MLP 61–16–8–1: 1112 pesos y 25 sesgos. Rechazos: 7/20 antes, 14/20 después. Las nuevas reglas contrastan cuenta/vivienda y tono intermedio [0,30;0,60]. No corrigen la causalidad inventada, la asociación número–campo ni todas las paráfrasis. Las franjas de tono son convenciones didácticas, no umbrales bancarios validados.

La revisión asistida identificó un texto aceptable y 19 problemáticos; cero falsos positivos entre ese único texto aceptable y cero entre seis controles correctos. Persisten cinco textos problemáticos aceptados. Esta muestra sirvió para desarrollar reglas: no demuestra generalización ni validez bancaria. La exactitud no sustituye análisis de créditos malos, calibración ni equidad.

Los documentos y evidencias heredados en `documentos/` y `evidencia/` pertenecen a la 7.1. Para esta entrega consultar `documentos72/` y `resultados72/`.
