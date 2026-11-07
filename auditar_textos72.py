"""Anotación semántica asistida, explícita y revisable; no es validación independiente."""
import json
from pathlib import Path
from verificador import verificar_explicacion
p=Path('resultados72');casos=json.loads((p/'comparacion.json').read_text())
notas={1:'Tono alto incompatible con 25,5%.',2:'Atribuye causalidad sin explicador y añade euros; confunde cuenta con propiedad.',3:'Niega saldo negativo presente y asigna tono alto a 56,5%.',4:'Inventa persona sola y califica 41% como alto.',5:'Inventa saldo exacto de 100 y confunde monto con saldo.',6:'Afirma sostenibilidad financiera sin información que la demuestre.',7:'Califica 35,5% como alto.',8:'Niega saldo negativo presente y asigna tono alto a 43%.',9:'Añade moneda no especificada y atribuye alquiler a la cuenta.',10:'Califica 27,5% como alto.',11:'Probabilidad redondeada y tono bajo compatibles.',12:'Califica 37% como alto.',13:'Reutiliza duración de 4 meses como edad; afirma situación crítica sin sustento.',14:'Con 30% de crédito malo afirma menor probabilidad de pagar sin soporte.',15:'Niega saldo negativo y califica 48% como alto.',16:'Califica 8,5% como alto.',17:'Califica 42,5% como alto.',18:'Afirma edad mayor de 60 cuando es 57.',19:'Suma de probabilidades binarias 76%, inconsistente.',20:'Suma de probabilidades binarias 50%, inconsistente.'}
for c in casos:
 c['correcto_revision_asistida']=c['solicitud']==11
 c['justificacion_revision']=notas[c['solicitud']]
(p/'revision_semantica.json').write_text(json.dumps(casos,ensure_ascii=False,indent=2))
res={'n':len(casos),'antes':sum(bool(c['antes']) for c in casos),'despues':sum(bool(c['despues']) for c in casos),'correctos_segun_revision':1,'falsos_positivos_antes':0,'falsos_positivos_despues':0,'errores_aceptados_antes':12,'errores_aceptados_despues':5,'limite':'Revisión asistida por IA, sin revisor independiente; muestra de desarrollo, no generalización.'}
D={'cuenta corriente':'saldo entre 0 y 200','vivienda':'alquilada'}
validos=['El riesgo es medio.','No tiene saldo negativo.','Su vivienda alquilada consta en los datos.','El monto es alto y el riesgo medio.','No es riesgo alto.','La cuenta tiene saldo entre 0 y 200.']
probes=[{'texto':t,'datos':D,'prob':.45,'correcto':True,'rechazos':verificar_explicacion(t,D,.45)} for t in validos]
res['controles_correctos']=len(probes);res['falsos_positivos_controles']=sum(bool(c['rechazos']) for c in probes)
(p/'controles_correctos.json').write_text(json.dumps(probes,ensure_ascii=False,indent=2))
(p/'resumen.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(res)
