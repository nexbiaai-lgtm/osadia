#!/usr/bin/env python3
"""Inicio v2: quita el vídeo del móvil y la animación de la línea; añade demo en directo, precios,
servicios en tarjetas fijas, 'Cómo empezamos' y barra fija de Llamar/WhatsApp en el móvil."""
import re,sys
sys.path.insert(0,'/home/claude/preview')
P='index.html'
s=open(P,encoding='utf-8').read()
assert 'home-v2' not in s, 'ya aplicado'
src=open('/home/claude/preview/build.py',encoding='utf-8').read()
ns={}
exec(src.split("for k,v in {'A':A")[0].replace("src=open('/home/claude/nexbia/index.html',encoding='utf-8').read()","src=S"),{'S':s,'re':re},ns)
base,CSS,A,B,C=ns['base'],ns['CSS'],ns['A'],ns['B'],ns['C']
C=C.replace('<div class="slot">','<div class="slot sg-steps"><div class="sg-head"><span class="eyebrow-inline">Cómo trabajamos</span><h2>Empezar es fácil</h2></div>',1)
slot=B+A.replace('<div class="slot">','<div class="slot" style="margin-top:18px">',1)
base=base.replace('@@SLOT@@',slot)
# 'Cómo empezamos' justo antes del bloque de llamada a la acción
k=base.find('<div class="o1-cta" data-o1box>'); assert k>0
base=base[:k]+C+base[k:]
STICKY='''<nav class="m-sticky" aria-label="Contacto rápido"><a class="c" href="tel:+34620762842">📞 Llamar</a><a class="w" href="https://wa.me/34620762842?text=Hola%2C%20me%20interesa%20una%20consultor%C3%ADa" target="_blank" rel="noopener">WhatsApp</a></nav>'''
EXTRA='''<style id="home-v2-m">
.m-sticky{display:none}
@media(max-width:640px){
 .m-sticky{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:60;gap:10px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:#fff;box-shadow:0 -8px 24px rgba(45,25,110,.12)}
 .m-sticky a{flex:1;text-align:center;text-decoration:none;font-weight:700;border-radius:999px;padding:14px 8px;font-family:Inter,sans-serif}
 .m-sticky .c{background:#4B3AA6;color:#fff}.m-sticky .w{background:#E9FBF1;color:#0E7A43}
 .whatsapp-fab{display:none!important} body{padding-bottom:76px}
 .optA{grid-template-columns:1fr 1fr}.optB{grid-template-columns:1fr}.optC{grid-template-columns:1fr}
 .demo{padding:24px}.demo h3{font-size:1.3rem}
}
</style>'''
base=base.replace('</head>',CSS.replace('<style>','<style id="home-v2">',1)+EXTRA+'</head>',1)
base=base.replace('</body>',STICKY+'</body>',1)
assert 'data-hv' not in base and 'data-o1journey' not in base and 'o1-line' not in base
open(P,'w',encoding='utf-8').write(base)
print('ok')
