# Tarea 7.1 — Automatización y extensión del entorno

Jorge Josué Flores González · MAI 540 · Atlantis University

Extiende el kit docente `Demo_Hibrido_incompleto` con el comando `resumir`, un
hook pre-commit y el plugin `control-datos-credito`. Conserva el kit original en
el primer commit. Los bloques de práctica están implementados; la evidencia de
esta entrega corresponde a la automatización, al predictor y a la verificación.
No se ejecutó el modelo de lenguaje Qwen ni se presenta una prueba generativa.

## Reproducción

Python 3.12 y Git. Desde la raíz del repositorio:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-automatizacion.txt
python instalar_hook.py
python tareas.py resumir
python tareas.py probar
python verificar_extension.py
```

En Windows se activa con `.venv\Scripts\Activate.ps1`. El hook se debe instalar
en cada clon; Git no distribuye `.git/hooks`. Para el componente generativo del
kit se necesitan además las dependencias de `requirements.txt` y la descarga de
Qwen. Esa ejecución no forma parte de la evidencia de Tarea 7.1.

## Comando propio

`python tareas.py resumir` informa filas, columnas, clases, nulos, duplicados y
SHA-256 del CSV, sin entrenar ni cambiar datos. Reduce la repetición del perfilado
manual. El hash permite comparar versiones, pero no certifica autenticidad ni
ausencia de sesgo. Resultado: 1,000 filas, 21 columnas, 700 good y 300 bad; cero
nulos y duplicados. El conjunto es el German Credit suministrado en clase.

## Hook y demostraciones

El hook ejecuta pytest y, si pasa, `verificar_extension.py` y una comprobación de
presencia del agente propio. Un código distinto de cero cancela el commit.

| Registro en evidencia/ | Resultado real |
|---|---|
| 01_commit_aceptado.txt | 8 pruebas pasan; commit 49e1550 aceptado |
| 02_commit_rechazado_pytest.txt | Umbral 0.30 cambiado a 0.99; 1 falla y 7 pasan; commit rechazado |
| 03_commit_rechazado_extension.txt | Sin description en manifiesto; pytest pasa y extensión bloquea el commit |
| 04_extension.txt | Manifiesto, comando y agente válidos |
| 05_resumen.txt | Perfil y hash del CSV |
| 06_pytest_final.txt | Código restaurado; 8 pruebas pasan |
| 09_reproduccion_limpia.txt | Mismos controles desde un clon limpio usando el entorno Python ya instalado |

Las capturas muestran estos registros originales en la terminal de VS Code;
no son terminales recreadas. Los archivos alterados se restauraron y HEAD no
cambió en los dos intentos rechazados. Para reproducir los fallos, modificar
solo los elementos indicados, intentar el commit y restaurarlos inmediatamente.

## Extensión

- `extension/.claude-plugin/plugin.json`: manifiesto y versión.
- `commands/resumir-datos.md`: ejecuta el perfil y solicita una interpretación breve.
- `agents/revisor-de-controles.md`: revisión de cobertura por archivo/línea, con
  herramientas de lectura; no modifica archivos ni ejecuta órdenes.

La validación estructural pasó sin líneas FALTA. Se probaron en Claude Code el comando y el agente con `--plugin-dir extension`; ambas consultas finalizaron con éxito. Las respuestas originales están en `evidencia/10_claude_comando.json` y `11_claude_agente.json`, y su captura en `71_claude.png`.

La revisión humana detectó dos límites: el comando llamó características a las 21 columnas (son 20 predictores y una etiqueta), y el agente cuestionó la evidencia sin consultar los registros conservados. Una respuesta exitosa no implica exactitud de todas sus afirmaciones.

Para repetir: activa el entorno y ejecuta `claude --plugin-dir extension`. Invoca `/control-datos-credito:resumir-datos` y pide al agente `revisor-de-controles` revisar la cobertura del hook.

## Riesgos y límites

El comando no detecta fuga de información ni asegura representatividad. El hook
no protege cuando se omite con `--no-verify`, no está instalado o una regla no
tiene pruebas. Comprueba el directorio de trabajo, no una exportación aislada del
índice: preparar cambios parciales exige revisar `git diff --cached`. La extensión
uniforma instrucciones, pero pasar el verificador no certifica la calidad de una
respuesta del agente ni la seguridad completa del modelo. No debe emplearse la
demostración para conceder o denegar créditos reales.

## Referencias

Atlantis University. (2026). *Tarea 7.1: Automatización y extensión del entorno* [Consigna de curso].

Git. (s. f.). *githooks*. https://git-scm.com/docs/githooks
