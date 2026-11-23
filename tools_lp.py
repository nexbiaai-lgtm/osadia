#!/usr/bin/env python3
"""Genera las páginas de aterrizaje para Google Ads (sin menú, formulario en 2 pasos) y la página de gracias."""
import re, json

LOGO = open('/home/claude/out/crecemia/logo/crecemia-logo-color.svg').read()
LOGO = re.sub(r'width="\d+" height="\d+"', '', LOGO, count=1).replace('<svg', '<svg class="lp-logo" role="img" aria-label="Crecemia"', 1)
WA = 'https://wa.me/34620762842'
TEL = '+34620762842'

PAGES = {
    'lp-agencia-ia': dict(
        title='Agencia de IA en Granada | Consultoría gratis · Crecemia',
        h1='Agencia de IA en Granada: <span>más clientes, menos tareas</span>',
        sub='Atendemos tus llamadas y WhatsApps con IA, te hacemos una web que capta clientes y automatizamos el papeleo. Empezamos con una consultoría gratis de 15 minutos.',
        bullets=['Chatbots de WhatsApp que responden y dan citas 24/7', 'Recepcionista de voz con IA que no deja una llamada sin coger', 'Webs que captan clientes, desde 199 €', 'Sin permanencia y nos vemos en persona en Granada'],
        pre=''),
    'lp-web': dict(
        title='Diseño web en Granada desde 199 € | Crecemia',
        h1='Diseño web en Granada <span>desde 199 €</span>',
        sub='Una web rápida, clara y pensada para que te escriban: formulario corto, botón de WhatsApp y reservas. Preparada para salir en Google y en ChatGPT.',
        bullets=['Lista para captar contactos desde el primer día', 'WhatsApp, llamada y reservas a un toque en el móvil', 'SEO local para salir en Google en Granada', 'Sin permanencia; nos vemos en persona si lo prefieres'],
        pre='Una página web'),
    'lp-chatbot-whatsapp': dict(
        title='Chatbot para WhatsApp desde 99 €/mes | Crecemia',
        h1='Tu WhatsApp <span>responde y da citas solo</span>',
        sub='Un asistente con IA contesta en segundos, resuelve dudas y reserva citas con tus horarios y precios, también a las 11 de la noche. Desde 99 €/mes.',
        bullets=['Responde en segundos, a cualquier hora', 'Agenda citas sin que toques el móvil', 'Te avisa cuando hace falta una persona', 'Sin permanencia: si no te sirve, lo quitamos'],
        pre='Chatbot de WhatsApp'),
    'lp-recepcionista-voz': dict(
        title='Recepcionista virtual con IA | Crecemia Granada',
        h1='Recepcionista virtual con IA: <span>nunca pierdas una llamada</span>',
        sub='Un asistente de voz natural en español atiende el teléfono, informa y agenda citas cuando tú no puedes coger. Ideal para clínicas, laboratorios y negocios con muchas llamadas.',
        bullets=['Atiende 24/7, también si estás comunicando', 'Voz natural, nada de «pulse 1»', 'Agenda la cita y te deja el resumen', 'Pruébalo ahora: llama al 936 94 09 26 (demo de una clínica)'],
        pre='Recepcionista de voz'),
}
NEEDS = ['Una página web', 'Chatbot de WhatsApp', 'Recepcionista de voz', 'Salir en Google (SEO)', 'Automatizar tareas', 'No lo sé, asesoradme']
LOGOS = [('bhd-vintage.jpg', 'BHD Vintage'), ('jj-mayoni.jpg', 'Pescados y Mariscos J.J. Mayoni'), ('n-digital-law.jpg', 'N Digital Law'),
         ('rydalca.jpg', 'Rydalca'), ('lock-wash.jpg', 'Lock & Wash Experience'), ('dentalproff.jpg', 'DentalProff'), ('sba.jpg', 'SmartBook AI')]

CSS = '''
*{box-sizing:border-box}html,body{margin:0}body{font-family:Inter,system-ui,sans-serif;color:#1D0E45;background:#FBF9FF;line-height:1.5}
a{color:#4B3AA6}.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.lp-top{display:flex;align-items:center;justify-content:space-between;padding:16px 0}
.lp-logo{height:34px;width:auto;display:block}
.lp-call{font-weight:700;text-decoration:none;color:#4B3AA6;border:1.5px solid #CDBBFF;border-radius:999px;padding:8px 16px;white-space:nowrap}
.hero{display:grid;grid-template-columns:1.1fr .9fr;grid-template-areas:'head card' 'details card';column-gap:40px;align-items:start;padding:24px 0 48px}.head{grid-area:head}.details{grid-area:details}.card{grid-area:card}
h1{font-family:Sora,Inter,sans-serif;font-weight:800;font-size:clamp(30px,4.4vw,50px);line-height:1.08;letter-spacing:-.02em;margin:8px 0 16px}
h1 span{color:#6A3DD8}.sub{font-size:18px;color:#4A3D6B;margin:0 0 22px}
.ticks{list-style:none;padding:0;margin:0 0 24px;display:grid;gap:10px}
.ticks li{padding-left:32px;position:relative;font-weight:600}
.ticks li:before{content:"";position:absolute;left:0;top:2px;width:22px;height:22px;border-radius:50%;background:#EDE6FF url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 12.5l4 4 8-9' fill='none' stroke='%236A3DD8' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/14px no-repeat}
.trust{display:flex;flex-wrap:wrap;gap:8px}.trust span{background:#fff;border:1px solid #E7DCFF;border-radius:999px;padding:6px 12px;font-size:14px;font-weight:600;color:#4B3AA6}
.card{background:#fff;border-radius:22px;box-shadow:0 24px 60px rgba(45,25,110,.14);padding:26px;position:sticky;top:16px}
.card h2{font-family:Sora,Inter,sans-serif;font-size:22px;margin:0 0 4px}.card .step{font-size:13px;font-weight:700;color:#6A3DD8;text-transform:uppercase;letter-spacing:.06em}
.chips{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0 4px}
.chips button{font:600 15px Inter,sans-serif;padding:14px 12px;border-radius:14px;border:1.5px solid #E1D6FA;background:#FBF9FF;color:#1D0E45;cursor:pointer;text-align:left}
.chips button:hover,.chips button[aria-pressed=true]{border-color:#6A3DD8;background:#F3EDFF}
.field{display:block;margin:14px 0 0}.field span{display:block;font-size:14px;font-weight:600;margin-bottom:6px}
.field input{width:100%;font:16px Inter,sans-serif;padding:14px 14px;border-radius:12px;border:1.5px solid #E1D6FA;background:#fff}
.field input:focus{outline:none;border-color:#6A3DD8;box-shadow:0 0 0 4px #EDE6FF}
.go{width:100%;margin-top:18px;font:700 17px Inter,sans-serif;background:#4B3AA6;color:#fff;border:0;border-radius:999px;padding:16px;cursor:pointer;box-shadow:0 10px 24px rgba(75,58,166,.3)}
.go:disabled{opacity:.7;cursor:wait}.back{background:none;border:0;color:#6B5F8A;font:600 14px Inter,sans-serif;cursor:pointer;padding:8px 0;margin-top:6px}
.err{color:#B3261E;font-size:14px;margin:10px 0 0}.legal{font-size:12px;color:#6B5F8A;margin:14px 0 0}
.chosen{font-size:14px;color:#4A3D6B;background:#F7F3FF;border-radius:10px;padding:8px 12px;margin-top:12px}
.hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}
.or{font-size:14px;color:#6B5F8A;text-align:center;margin:14px 0 0}
.logos{padding:28px 0 40px;text-align:center}.logos p{font-size:14px;font-weight:700;color:#6B5F8A;text-transform:uppercase;letter-spacing:.08em;margin:0 0 16px}
.logos div{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:22px}.logos img{height:46px;width:auto;filter:grayscale(1);opacity:.75}
.how{background:#fff;padding:44px 0}.how h2{font-family:Sora,Inter,sans-serif;text-align:center;font-size:28px;margin:0 0 24px}
.steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.steps3 div{background:#FBF9FF;border-radius:18px;padding:20px}
.steps3 b{display:block;font-family:Sora,Inter,sans-serif;font-size:18px;margin-bottom:4px}.steps3 i{font-style:normal;color:#6A3DD8;font-weight:800}
footer{padding:24px 0 110px;font-size:13px;color:#6B5F8A;text-align:center}
.sticky{display:none}
@media (max-width:860px){.hero{grid-template-columns:1fr;grid-template-areas:'head' 'card' 'details';row-gap:22px;padding-top:8px}.sub{font-size:16px;margin-bottom:0}h1{margin-top:0}.card{position:static}.steps3{grid-template-columns:1fr}
 .sticky{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:50;gap:10px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:#fff;box-shadow:0 -8px 24px rgba(45,25,110,.12)}
 .sticky a{flex:1;text-align:center;text-decoration:none;font-weight:700;border-radius:999px;padding:14px 8px}
 .sticky .c{background:#4B3AA6;color:#fff}.sticky .w{background:#E9FBF1;color:#0E7A43}.lp-call{display:none}}
'''

JS = '''
(function(){
  var FORM_URL = 'https://script.google.com/macros/s/AKfycbwBwdnmp4AiEegJpMe1Bm5X-_4w2oKefZ5P_nXAc6L6V8eXDIES44zWcyA5Tt35Fbkx/exec';
  var s1 = document.getElementById('s1'), s2 = document.getElementById('s2');
  var need = document.body.getAttribute('data-pre') || '';
  function toStep2(){ document.getElementById('chosen').textContent = 'Te interesa: ' + need; s1.hidden = true; s2.hidden = false; document.getElementById('fName').focus(); }
  [].forEach.call(document.querySelectorAll('.chips button'), function(b){
    b.addEventListener('click', function(){
      [].forEach.call(document.querySelectorAll('.chips button'), function(x){ x.setAttribute('aria-pressed','false'); });
      b.setAttribute('aria-pressed','true'); need = b.textContent; toStep2();
    });
  });
  document.getElementById('back').addEventListener('click', function(){ s2.hidden = true; s1.hidden = false; });
  var form = document.getElementById('lead');
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var name = form.nombre.value.trim(), tel = form.telefono.value.replace(/[^0-9+]/g,''), err = document.getElementById('err');
    if (!name || tel.replace(/\\D/g,'').length < 9){ err.textContent = 'Pon tu nombre y un teléfono para poder llamarte.'; err.hidden = false; return; }
    err.hidden = true;
    var btn = document.getElementById('go'); btn.disabled = true; btn.textContent = 'Enviando…';
    var q = new URLSearchParams(location.search);
    var data = { tipo: 'Landing Google Ads', nombre: name, empresa: '', contacto: tel, email: '', sitio: '', dia: '', franja: '',
      servicio: need, pagina: location.pathname.split('/').pop(), url_trap: form.url_trap.value,
      utm: [q.get('utm_campaign'), q.get('utm_term'), q.get('gclid') ? 'gclid' : ''].filter(Boolean).join(' | ') };
    function go(){
      try { if (window.nexbiaConversion) window.nexbiaConversion('landing'); } catch(e) {}
      try { sessionStorage.setItem('crecemia-lead', name.split(' ')[0]); } catch(e) {}
      setTimeout(function(){ location.href = 'gracias.html'; }, 400);
    }
    function fail(){
      btn.disabled = false; btn.textContent = 'Quiero que me llaméis →';
      err.innerHTML = 'No se ha podido enviar. <a href="https://wa.me/34620762842?text=' + encodeURIComponent('Hola, soy ' + name + '. Me interesa: ' + need + '. Mi teléfono: ' + tel) + '" target="_blank" rel="noopener"><b>Escríbenos por WhatsApp →</b></a>';
      err.hidden = false;
    }
    fetch(FORM_URL, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(data) }).then(go).catch(fail);
  });
  if (need) { /* página con servicio ya elegido: se puede saltar el paso 1 */ }
})();
'''


def page(slug, p):
    chips = ''.join(f'<button type="button" aria-pressed="false">{n}</button>' for n in NEEDS)
    ticks = ''.join(f'<li>{b}</li>' for b in p['bullets'])
    logos = ''.join(f'<img loading="lazy" src="logos/{f}" alt="Logo de {a}">' for f, a in LOGOS)
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{p['title']}</title>
<meta name="description" content="{re.sub('<[^>]+>','',p['sub'])}">
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="https://www.crecemia.es/{slug}.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#4B3AA6">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script src="consent.js?v=3"></script>
</head>
<body data-pre="{p['pre']}">
<div class="wrap">
  <div class="lp-top">{LOGO}<a class="lp-call" href="tel:{TEL}">Llamar · 620 76 28 42</a></div>
  <main class="hero">
    <section class="head">
      <h1>{p['h1']}</h1>
      <p class="sub">{p['sub']}</p>
    </section>
    <section class="details">
      <ul class="ticks">{ticks}</ul>
      <div class="trust"><span>Consultoría gratis de 15 min</span><span>Sin permanencia</span><span>Equipo en Granada</span><span>Te llamamos hoy</span></div>
    </section>
    <aside class="card" aria-labelledby="ft">
      <div id="s1">
        <div class="step">Paso 1 de 2</div>
        <h2 id="ft">¿Qué necesitas?</h2>
        <div class="chips">{chips}</div>
        <p class="or">o llámanos al <a href="tel:{TEL}"><b>620 76 28 42</b></a></p>
      </div>
      <div id="s2" hidden>
        <div class="step">Paso 2 de 2</div>
        <h2>¿A qué número te llamamos?</h2>
        <div class="chosen" id="chosen"></div>
        <form id="lead" novalidate>
          <label class="field"><span>Tu nombre</span><input name="nombre" id="fName" autocomplete="name" required></label>
          <label class="field"><span>Teléfono o WhatsApp</span><input name="telefono" type="tel" inputmode="tel" autocomplete="tel" placeholder="6XX XX XX XX" required></label>
          <input class="hp" name="url_trap" tabindex="-1" autocomplete="off" aria-hidden="true">
          <button class="go" id="go" type="submit">Quiero que me llaméis →</button>
          <p class="err" id="err" hidden></p>
          <button class="back" id="back" type="button">← Cambiar lo que necesito</button>
          <p class="legal">Responsable: Daniel Mata Jiménez (Crecemia). Usamos tu nombre y teléfono solo para llamarte por esta consulta. Puedes ejercer tus derechos escribiendo a info@nexbia.es. <a href="privacidad.html">Política de privacidad</a>.</p>
        </form>
      </div>
    </aside>
  </main>
</div>
<section class="logos"><div class="wrap"><p>Negocios que ya trabajan con nosotros</p><div>{logos}</div></div></section>
<section class="how"><div class="wrap"><h2>Cómo empezamos</h2><div class="steps3">
  <div><i>1</i><b>Nos dices qué necesitas</b>Dos clics y tu teléfono. Nada más.</div>
  <div><i>2</i><b>Te llamamos</b>En horario laboral, normalmente en minutos. Son 15 minutos y es gratis.</div>
  <div><i>3</i><b>Te decimos qué hacer primero</b>Con precio cerrado y sin permanencia. Si no te encaja, no pasa nada.</div>
</div></div></section>
<footer><div class="wrap">Crecemia · Agencia de IA y marketing en Granada · <a href="index.html">crecemia.es</a> · <a href="aviso-legal.html">Aviso legal</a> · <a href="privacidad.html">Privacidad</a> · <a href="cookies.html">Cookies</a></div></footer>
<nav class="sticky" aria-label="Contacto rápido"><a class="c" href="tel:{TEL}">Llamar</a><a class="w" href="{WA}?text={'Hola%2C%20me%20interesa%20' + (p['pre'] or 'una%20consultor%C3%ADa').replace(' ','%20')}" target="_blank" rel="noopener">WhatsApp</a></nav>
<script>{JS}</script>
</body>
</html>
'''


GRACIAS = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>¡Recibido! Te llamamos enseguida | Crecemia</title><meta name="robots" content="noindex,nofollow">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}
.ok{{max-width:640px;margin:40px auto;text-align:center;background:#fff;border-radius:24px;box-shadow:0 24px 60px rgba(45,25,110,.14);padding:36px 26px}}
.ok .tick{{width:72px;height:72px;border-radius:50%;background:#E9FBF1;margin:0 auto 16px;display:grid;place-items:center;font-size:36px;color:#0E7A43}}
.ok h1{{font-size:clamp(26px,4vw,38px)}}.ok .go{{display:block;text-decoration:none;max-width:360px;margin:20px auto 0}}</style>
<script src="consent.js?v=3"></script></head>
<body><div class="wrap"><div class="lp-top">{LOGO}</div>
<div class="ok"><div class="tick">✓</div><h1>¡Recibido<span id="nm"></span>! <span>Te llamamos en unos minutos</span></h1>
<p class="sub">Si escribes fuera de horario (L–V de 10 a 19 h), te llamamos a primera hora del siguiente día laborable. La llamada dura 15 minutos y es gratis.</p>
<a class="go" href="{WA}?text=Hola%2C%20acabo%20de%20pedir%20que%20me%20llam%C3%A9is" target="_blank" rel="noopener">¿Prefieres escribirnos ya por WhatsApp? →</a>
<p class="legal"><a href="index.html">Volver a crecemia.es</a></p></div></div>
<script>try{{var n=sessionStorage.getItem('crecemia-lead');if(n)document.getElementById('nm').textContent=', '+n;}}catch(e){{}}</script>
</body></html>
'''

if __name__ == '__main__':
    for slug, p in PAGES.items():
        open(f'{slug}.html', 'w').write(page(slug, p))
    open('gracias.html', 'w').write(GRACIAS)
    print('ok')
