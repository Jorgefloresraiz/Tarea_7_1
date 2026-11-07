"""Evidencia reproducible: partición única, modelos y generaciones conservadas."""
import json, time, hashlib
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datos import cargar_datos, datos_legibles
from predictor import entrenar_predictor, probabilidad_malo
from red_neuronal import crear_red, describir_red

def preparar():
    out=Path('resultados72'); out.mkdir(exist_ok=True)
    X,y,cat,num=cargar_datos()
    a,b,c,d=train_test_split(X,y,test_size=.20,stratify=y,random_state=42)
    t=time.perf_counter(); rf,test,truth=entrenar_predictor(); tr=time.perf_counter()-t
    assert test.index.equals(b.index) and truth.equals(d)
    t=time.perf_counter(); red=crear_red(cat,num).fit(a,c); tn=time.perf_counter()-t
    mlp=red.named_steps['red']; capas,total=describir_red(red)
    result={'n_train':len(a),'n_test':len(b),'test_indices':list(map(int,b.index)), 'capas':capas,'pesos':sum(w.size for w in mlp.coefs_), 'sesgos':sum(w.size for w in mlp.intercepts_), 'parametros':total,'exactitud_rf':accuracy_score(d,rf.predict(b)),'exactitud_red':accuracy_score(d,red.predict(b)), 'segundos_rf':tr,'segundos_red':tn,'sha256_csv':hashlib.sha256(Path('datos/credit_g.csv').read_bytes()).hexdigest()}
    (out/'modelos.json').write_text(json.dumps(result,indent=2))
    casos=[{'solicitud':i+1,'indice':int(b.index[i]),'datos':datos_legibles(b.iloc[i]),'prob':probabilidad_malo(rf,b,i),'real':int(d.iloc[i])} for i in range(20)]
    (out/'solicitudes.json').write_text(json.dumps(casos,ensure_ascii=False,indent=2))
    print(json.dumps(result,indent=2),flush=True)

def generar():
    import torch
    from explicador import cargar_modelo_lenguaje, explicar, recortar_a_oracion
    from verificador_base import verificar_explicacion
    torch.set_num_threads(4)
    tok,model=cargar_modelo_lenguaje()
    out=Path('resultados72'); casos=json.loads((out/'solicitudes.json').read_text())
    target=out/'generaciones.jsonl'
    done={json.loads(s)['solicitud'] for s in target.read_text().splitlines()} if target.exists() else set()
    for c in casos:
        if c['solicitud'] in done: continue
        t=time.perf_counter(); raw=explicar(tok,model,c['datos'],c['prob'])
        c.update(texto_original=raw,texto=recortar_a_oracion(raw),segundos=time.perf_counter()-t)
        c['rechazo_base']=verificar_explicacion(c['texto'],c['datos'],c['prob'])
        with target.open('a') as f: f.write(json.dumps(c,ensure_ascii=False)+'\n')
        print(json.dumps(c,ensure_ascii=False),flush=True)
if __name__=='__main__':
    import sys
    generar() if '--generar' in sys.argv else preparar()
