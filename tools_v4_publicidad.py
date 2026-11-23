#!/usr/bin/env python3
"""Crea publicidad-online.html (Google Ads y Meta Ads) con animaciones, y la añade al menú, pie, inicio y sitemap."""
import re, json, glob

s = open('web.html', encoding='utf-8').read()
head, rest = s.split('<main>', 1)
foot = rest.split('</main>', 1)[1]
TITLE = 'Publicidad en Google Ads y Meta Ads en Granada | Crecemia'
DESC = 'Campañas de Google Ads y Meta Ads (Facebook e Instagram) para negocios de Granada. Medimos llamadas, formularios y WhatsApp para que sepas cuánto te cuesta cada cliente.'
head = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', head)
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + DESC, head)
head = re.sub(r'(og:description" content=")[^"]*', lambda m: m.group(1) + DESC, head)
head = re.sub(r'(og:title" content=")[^"]*', lambda m: m.group(1) + TITLE, head)
head = head.replace('https://www.crecemia.es/web.html', 'https://www.crecemia.es/publicidad-online.html')
for typ in ('Service', 'FAQPage', 'BreadcrumbList'):
    head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "' + typ + r'".*?</script>', '', head, flags=re.S)
FAQ = [('¿Cuánto cuesta?', 'La gestión depende de la campaña: dónde te anuncias, cuántas campañas y qué hay que preparar. Te damos un precio cerrado en la llamada. Lo que inviertes en anuncios lo pagas directamente a Google o a Meta.'),
       ('¿Cuánto tengo que invertir en anuncios?', 'Lo decidimos contigo según tu objetivo y tu zona. Se puede empezar con poco, medir y subir solo cuando los números salen.'),
       ('¿Cuándo veré resultados?', 'Los anuncios empiezan a mostrarse en cuanto Google o Meta los aprueban. Las primeras semanas sirven para aprender qué funciona y ajustar.'),
       ('¿Google Ads o Meta Ads?', 'Google llega a quien ya está buscando lo que ofreces. Meta llega a gente que aún no te conoce, con imagen y vídeo. Muchas veces lo mejor es combinar las dos.'),
       ('¿Hay permanencia?', 'No. Trabajamos mes a mes.')]
ld = [{"@context": "https://schema.org", "@type": "Service", "name": "Publicidad online (Google Ads y Meta Ads)", "serviceType": "Gestión de campañas de publicidad online",
       "url": "https://www.crecemia.es/publicidad-online.html", "provider": {"@id": "https://www.crecemia.es/#organization"}, "areaServed": [{"@type": "City", "name": "Granada"}]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.crecemia.es/"},
       {"@type": "ListItem", "position": 2, "name": "Publicidad online", "item": "https://www.crecemia.es/publicidad-online.html"}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
head = head.replace('</head>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld) + '\n</head>', 1)
head = head.replace('<a href="web.html" class="active" aria-current="page">', '<a href="web.html">')
foot = foot.replace('<a href="web.html" class="active" aria-current="page">', '<a href="web.html">')

INCLUYE = [('Google Ads', 'Anuncios en el buscador, en Google Maps, en YouTube y campañas de máximo rendimiento. Salimos cuando alguien busca lo que vendes en tu zona.'),
           ('Meta Ads', 'Anuncios en Instagram y Facebook con imagen y vídeo. Formularios dentro de la app y mensajes directos a tu WhatsApp.'),
           ('Medición de verdad', 'Contamos llamadas, formularios y WhatsApp como conversiones. Así sabes cuánto te cuesta cada cliente, no solo cada clic.'),
           ('Página de aterrizaje', 'Si hace falta, preparamos una página solo para la campaña, con un formulario corto que convierte mejor que la web general.'),
           ('Ajustes cada semana', 'Quitamos lo que no funciona, subimos lo que sí, probamos anuncios nuevos y cuidamos que no pagues clics inútiles.'),
           ('Informe mensual claro', 'Cuánto has invertido, cuántos contactos has tenido y qué haremos el mes siguiente. Sin jerga.')]
STEPS = [('Hablamos 15 minutos', 'Tu negocio, tu cliente ideal, tu zona y cuánto quieres invertir.'),
         ('Preparamos la campaña', 'Palabras clave o públicos, anuncios, página de destino y medición de conversiones.'),
         ('Lanzamos y medimos', 'Las primeras semanas vemos qué anuncios y búsquedas traen contactos.'),
         ('Optimizamos', 'Ajustamos cada semana y subimos la inversión solo donde los números salen.')]

def card(t, p, n=None):
    num = f'<span class="rs-num">{n:02d}</span>' if n else ''
    return f'<div class="rs-card">{num}<h3>{t}</h3><p>{p}</p></div>'

DASH = '''<div class="ad-dash" data-anim>
  <div class="ad-dash-top"><span class="ad-dot"></span><b>Panel de campaña</b><span class="ad-tag">Datos de ejemplo</span></div>
  <div class="ad-kpis">
    <div><span>Impresiones</span><b data-count="52480">0</b></div>
    <div><span>Clics</span><b data-count="4410">0</b></div>
    <div class="hl"><span>Clics por impresión</span><b data-count="8.4" data-dec="1" data-suf=" %">0</b></div>
    <div class="hl"><span>Conversión</span><b data-count="11.2" data-dec="1" data-suf=" %">0</b></div>
  </div>
  <svg class="ad-chart" viewBox="0 0 400 140" preserveAspectRatio="none" aria-hidden="true">
    <defs><linearGradient id="adg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#7A4FD1" stop-opacity=".35"/><stop offset="1" stop-color="#7A4FD1" stop-opacity="0"/></linearGradient></defs>
    <path class="ad-area" d="M0,120 L40,112 L80,104 L120,98 L160,84 L200,78 L240,62 L280,50 L320,40 L360,26 L400,14 L400,140 L0,140 Z" fill="url(#adg)"/>
    <path class="ad-line" d="M0,120 L40,112 L80,104 L120,98 L160,84 L200,78 L240,62 L280,50 L320,40 L360,26 L400,14" fill="none" stroke="#7A4FD1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  <div class="ad-legend"><span>Contactos por semana</span><span class="up">▲ subiendo</span></div>
  <p class="ad-note">Ejemplo para enseñarte cómo verás tu panel. No son resultados de un cliente.</p>
</div>'''

FUNNEL = '''<div class="ad-funnel" data-anim>
  <div class="fn" style="--w:100%"><span>Personas que ven tu anuncio</span><b data-count="52480">0</b></div>
  <div class="fn" style="--w:72%"><span>Hacen clic</span><b data-count="4410">0</b></div>
  <div class="fn" style="--w:46%"><span>Te llaman o te escriben</span><b data-count="496">0</b></div>
  <div class="fn" style="--w:26%"><span>Se convierten en clientes</span><b data-count="148">0</b></div>
  <p class="ad-note">Ejemplo ilustrativo. Cada negocio y cada sector tiene sus propios números: los medimos desde el primer día.</p>
</div>'''

BENCH = '''<div class="ad-bench" data-anim>
  <div class="bc"><span class="pl g">Google Ads · búsqueda</span>
    <div class="bar"><i style="--v:66%"></i></div><p><b data-count="6.64" data-dec="2" data-suf=" %">0</b> clics por impresión</p>
    <div class="bar"><i style="--v:82%"></i></div><p><b data-count="8.18" data-dec="2" data-suf=" %">0</b> de clics que se convierten</p></div>
  <div class="bc"><span class="pl m">Meta Ads · captación</span>
    <div class="bar"><i style="--v:27%"></i></div><p><b data-count="2.70" data-dec="2" data-suf=" %">0</b> clics por impresión</p>
    <div class="bar"><i style="--v:85%"></i></div><p><b data-count="8.54" data-dec="2" data-suf=" %">0</b> de clics que se convierten</p></div>
  <p class="ad-note">Medias de 2026 en Estados Unidos según WordStream by LocaliQ (<a href="https://www.searchenginejournal.com/what-a-good-ctr-for-google-ads/492785/" target="_blank" rel="noopener">Google</a>, <a href="https://searchengineland.com/facebook-ad-costs-fall-as-traffic-and-lead-performance-improvements-report-488433" target="_blank" rel="noopener">Meta</a>). Nuestro objetivo es superarlas.</p>
</div>'''

CALC = '''<div class="ad-calc" data-calc>
  <label>Inversión mensual en anuncios <output data-o="b">300 €</output><input type="range" min="100" max="3000" step="50" value="300" data-i="b"></label>
  <label>Coste por clic estimado <output data-o="c">1,20 €</output><input type="range" min="0.3" max="5" step="0.1" value="1.2" data-i="c"></label>
  <label>Conversión de la web <output data-o="r">8 %</output><input type="range" min="2" max="20" step="1" value="8" data-i="r"></label>
  <div class="ad-calc-out"><div><span>Clics al mes</span><b data-r="k">250</b></div><div class="hl"><span>Contactos al mes</span><b data-r="l">20</b></div><div><span>Coste por contacto</span><b data-r="p">15 €</b></div></div>
  <p class="ad-note">Cálculo orientativo. El coste por clic real depende de tu sector, tu zona y la competencia.</p>
</div>'''

JS = '''<script>(function(){
var rm=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
function fmt(v,d){return v.toLocaleString("es-ES",{minimumFractionDigits:d,maximumFractionDigits:d})}
function run(el){el.classList.add("on");el.querySelectorAll("[data-count]").forEach(function(b){var t=parseFloat(b.dataset.count),d=+(b.dataset.dec||0),s=b.dataset.suf||"";if(rm){b.textContent=fmt(t,d)+s;return}var t0=null;function st(ts){if(!t0)t0=ts;var p=Math.min((ts-t0)/1600,1),e=1-Math.pow(1-p,3);b.textContent=fmt(t*e,d)+s;if(p<1)requestAnimationFrame(st)}requestAnimationFrame(st)})}
var io="IntersectionObserver" in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){run(e.target);io.unobserve(e.target)}})},{threshold:.3}):null;
document.querySelectorAll("[data-anim]").forEach(function(el){io?io.observe(el):run(el)});
var c=document.querySelector("[data-calc]");if(c){function u(){var b=+c.querySelector("[data-i=b]").value,cp=+c.querySelector("[data-i=c]").value,r=+c.querySelector("[data-i=r]").value;var k=Math.round(b/cp),l=Math.max(1,Math.round(k*r/100));c.querySelector("[data-o=b]").textContent=fmt(b,0)+" €";c.querySelector("[data-o=c]").textContent=fmt(cp,2)+" €";c.querySelector("[data-o=r]").textContent=r+" %";c.querySelector("[data-r=k]").textContent=fmt(k,0);c.querySelector("[data-r=l]").textContent=fmt(l,0);c.querySelector("[data-r=p]").textContent=fmt(b/l,0)+" €"}c.addEventListener("input",u);u()}
})();</script>'''

main = f'''<main>
<div class="wrap page-hero">
  <div class="breadcrumb"><a href="index.html">Inicio</a><span>/</span><span>Publicidad online</span></div>
  <div class="ad-hero"><div><h1>Publicidad en Google y en redes sociales: <span class="hl-hand">anuncios que te traen clientes</span></h1>
  <p class="lead">Montamos y llevamos tus campañas de Google Ads y Meta Ads (Facebook e Instagram) en Granada. Cada mes ves cuánto has invertido, cuántos te han llamado o escrito y cuánto te ha costado cada cliente.</p>
  <div class="cta-row" style="margin-top:22px;">
    <a class="btn btn-accent btn-cta" href="contacto.html">Quiero anunciarme</a>
    <a class="btn btn-ghost" href="https://wa.me/34620762842?text=Hola%2C%20me%20interesa%20la%20publicidad%20en%20Google%20y%20Meta" target="_blank" rel="noopener">Escribir por WhatsApp</a>
  </div>
  <p class="ad-price">Precio según campaña · Sin permanencia</p></div>
  {DASH}</div>
</div>
<section>
  <div class="wrap">
    <div class="section-head"><h2>De quien ve tu anuncio a quien te compra</h2><p>Lo que importa no son los clics, sino cuántos acaban llamándote. Así lo medimos.</p></div>
    {FUNNEL}
  </div>
</section>
<section class="band-light">
  <div class="wrap">
    <div class="section-head"><h2>Qué incluye</h2></div>
    <div class="rs-grid">{''.join(card(t, p) for t, p in INCLUYE)}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><h2>Las referencias que queremos superar</h2><p>Así rinden de media los anuncios en 2026.</p></div>
    {BENCH}
  </div>
</section>
<section class="band-light">
  <div class="wrap">
    <div class="section-head"><h2>Calcula cuántos contactos podrías tener</h2><p>Mueve los controles para hacerte una idea antes de hablar con nosotros.</p></div>
    {CALC}
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><h2>Así trabajamos</h2></div>
    <div class="rs-grid" style="grid-template-columns:repeat(4,1fr)">{''.join(card(t, p, i + 1) for i, (t, p) in enumerate(STEPS))}</div>
  </div>
</section>
<section class="band-light">
  <div class="wrap">
    <div class="section-head"><h2>¿Cuánto cuesta?</h2><p>Cada campaña es distinta, por eso el precio también.</p></div>
    <div class="rs-plans">
      <div class="rs-plan"><h3>Gestión de la campaña</h3><p class="rs-price">Según campaña</p><ul><li>Depende de dónde te anuncias y cuántas campañas</li><li>Precio cerrado antes de empezar</li><li>Sin permanencia</li></ul></div>
      <div class="rs-plan hl"><h3>Lo que inviertes en anuncios</h3><p class="rs-price">Tú decides</p><ul><li>Lo pagas directamente a Google o a Meta</li><li>Lo ajustamos según los resultados</li><li>Ves cada euro en tu propia cuenta</li></ul></div>
      <div class="rs-plan"><h3>Google + Meta + redes</h3><p class="rs-price">Pack a medida</p><ul><li>Anuncios y gestión de redes juntos</li><li>Los vídeos que funcionan, impulsados</li><li>Un solo informe al mes</li></ul></div>
    </div>
    <div class="cta-row" style="justify-content:center;margin-top:24px;"><a class="btn btn-primary btn-lg btn-cta" href="contacto.html">Pedir precio de mi campaña</a></div>
  </div>
</section>
<section id="faq">
  <div class="wrap">
    <div class="section-head"><h2>Preguntas frecuentes</h2></div>
    <div class="rs-grid" style="grid-template-columns:repeat(2,1fr)">{''.join(card(q, a) for q, a in FAQ)}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="final-cta">
      <h2>¿Lanzamos tu primera campaña?</h2>
      <p>En 15 minutos vemos qué te conviene más, Google o Meta, y cuánto costaría.</p>
      <div class="cta-row" style="justify-content:center;">
        <a class="btn btn-accent btn-cta" href="contacto.html">Reservar llamada gratis</a>
        <a class="btn btn-ghost" style="border-color:rgba(255,255,255,0.35);color:#fff;" href="https://wa.me/34620762842" target="_blank" rel="noopener">Escribir por WhatsApp</a>
      </div>
    </div>
  </div>
</section>
</main>{JS}'''
open('publicidad-online.html', 'w', encoding='utf-8').write(head + main + foot)

# Menú, pie, inicio, sitemap, llms
for f in glob.glob('*.html'):
    x = open(f, encoding='utf-8').read(); o = x
    hdr = x.split('</header>')[0]
    if 'publicidad-online.html' not in hdr and 'id="menu-servicios"' in hdr:
        x = re.sub(r'(<a href="redes-sociales.html"[^>]*>Redes sociales</a>\n)(</div>)', r'\1<a href="publicidad-online.html">Publicidad online</a>\n\2', x, count=1)
    if '<li><a href="publicidad-online.html">' not in x:
        x = x.replace('<li><a href="redes-sociales.html">Redes sociales</a></li>', '<li><a href="redes-sociales.html">Redes sociales</a></li><li><a href="publicidad-online.html">Publicidad online</a></li>')
    if f == 'publicidad-online.html':
        x = x.replace('<a href="publicidad-online.html">Publicidad online</a>\n</div>', '<a href="publicidad-online.html" class="active" aria-current="page">Publicidad online</a>\n</div>', 1)
    if x != o: open(f, 'w', encoding='utf-8').write(x)

h = open('index.html', encoding='utf-8').read()
if 'href="publicidad-online.html"><span class="sg-svc">' not in h:
    ADS = ('<a class="sg-card" href="publicidad-online.html"><span class="sg-svc">Publicidad online</span><h3>Pagas anuncios y no sabes qué te traen</h3>'
           '<p>Campañas en Google y en Instagram y Facebook, midiendo cuántos te llaman o escriben y cuánto te cuesta cada cliente.</p>'
           '<span class="sg-foot"><b>Según campaña</b><span>Ver cómo funciona →</span></span></a>')
    h = h.replace('<div class="sg-calc o1-final" id="calculadora">', ADS + '<div class="sg-calc o1-final" id="calculadora">', 1)
    open('index.html', 'w', encoding='utf-8').write(h)
sm = open('sitemap.xml').read()
if 'publicidad-online' not in sm:
    sm = sm.replace('</urlset>', '  <url><loc>https://www.crecemia.es/publicidad-online.html</loc><lastmod>2026-11-24</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
    open('sitemap.xml', 'w').write(sm)
ll = open('llms.txt', encoding='utf-8').read()
if 'publicidad-online' not in ll:
    ll = ll.replace('- [Redes sociales](https://www.crecemia.es/redes-sociales.html): gestión de Instagram, TikTok y Facebook.',
                    '- [Redes sociales](https://www.crecemia.es/redes-sociales.html): gestión de Instagram, TikTok y Facebook, desde 99 €/mes.\n- [Publicidad online](https://www.crecemia.es/publicidad-online.html): campañas de Google Ads y Meta Ads.')
    open('llms.txt', 'w', encoding='utf-8').write(ll)
print('ok')
