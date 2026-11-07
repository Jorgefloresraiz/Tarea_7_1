"""Reaplica ambos verificadores a textos idénticos, sin regenerar."""
import csv,json
from pathlib import Path
from verificador import verificar_explicacion,explicacion_segura
from verificador_base import verificar_explicacion as base
p=Path('resultados72')
casos=[json.loads(s) for s in (p/'generaciones.jsonl').read_text().splitlines()]
assert len(casos)>=10
for c in casos:
 c['antes']=base(c['texto'],c['datos'],c['prob'])
 c['despues']=verificar_explicacion(c['texto'],c['datos'],c['prob'])
 c['texto_mostrado']=explicacion_segura(c['datos'],c['prob']) if c['despues'] else c['texto']
(p/'comparacion.json').write_text(json.dumps(casos,ensure_ascii=False,indent=2))
with (p/'rechazos.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['solicitud','indice','probabilidad','rechazo_antes','rechazo_despues','motivos_antes','motivos_despues'])
 for c in casos: w.writerow([c['solicitud'],c['indice'],c['prob'],bool(c['antes']),bool(c['despues']),'; '.join(c['antes']),'; '.join(c['despues'])])
print('n=',len(casos),'antes=',sum(bool(c['antes']) for c in casos),'despues=',sum(bool(c['despues']) for c in casos))
for c in casos: print(c['solicitud'],bool(c['antes']),bool(c['despues']),c['despues'])
