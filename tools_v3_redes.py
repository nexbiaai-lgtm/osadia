#!/usr/bin/env python3
"""Crea redes-sociales.html (gestión de redes sociales) a partir de la plantilla de web.html."""
import re, json, sys
sys.path.insert(0, '.')
from tools_v3_pages import ig_grid, IG_ICON

s = open('web.html', encoding='utf-8').read()
head, rest = s.split('<main>', 1)
foot = rest.split('</main>', 1)[1]

TITLE = 'Gestión de redes sociales en Granada | Crecemia'
DESC = 'Llevamos las redes sociales de tu negocio en Granada: Instagram, TikTok y Facebook. Plan de contenidos, diseño, reels, textos y publicación cada semana.'
head = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', head)
head = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + DESC, head)
head = re.sub(r'(og:description" content=")[^"]*', r'\g<1>' + DESC, head)
head = re.sub(r'(og:title" content=")[^"]*', r'\g<1>' + TITLE, head)
head = head.replace('https://www.crecemia.es/web.html', 'https://www.crecemia.es/redes-sociales.html')
head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "Service".*?</script>',
              '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Service", "name": "Gestión de redes sociales",
              "serviceType": "Gestión de redes sociales (social media)", "url": "https://www.crecemia.es/redes-sociales.html",
              "provider": {"@id": "https://www.crecemia.es/#organization"}, "areaServed": [{"@type": "City", "name": "Granada"}]}, ensure_ascii=False) + '</script>', head, flags=re.S)
head = head.replace('"name": "Desarrollo web", "item": "https://www.crecemia.es/redes-sociales.html"', '"name": "Redes sociales", "item": "https://www.crecemia.es/redes-sociales.html"')
head = head.replace('"name": "Páginas web", "item": "https://www.crecemia.es/redes-sociales.html"', '"name": "Redes sociales", "item": "https://www.crecemia.es/redes-sociales.html"')
# FAQ schema de web.html fuera (no aplica)
head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>', '', head, flags=re.S)
head = head.replace('<a href="web.html" class="active" aria-current="page">', '<a href="web.html">')
foot = foot.replace('<a href="web.html" class="active" aria-current="page">', '<a href="web.html">')
head = head.replace('<a href="redes-sociales.html">Redes sociales</a>', '<a href="redes-sociales.html" class="active" aria-current="page">Redes sociales</a>')

PLAT = [('Instagram', IG_ICON),
        ('TikTok', '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.6 3c.4 2.2 1.8 3.7 4 3.9v3.2a7.5 7.5 0 0 1-4-1.2v6.3A5.8 5.8 0 1 1 10.8 9.4v3.3a2.6 2.6 0 1 0 2.6 2.6V3h3.2z"/></svg>'),
        ('Facebook', '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.5H16l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H8v3h2.6V21h2.9z"/></svg>'),
        ('Google Business', '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>')]

CARDS = [
 ('Plan de contenidos', 'Cada mes te proponemos qué publicar y cuándo: ideas pensadas para tu negocio y tu cliente, no frases genéricas.'),
 ('Diseño con tu marca', 'Publicaciones y carruseles con tus colores y tu estilo, para que se reconozca tu negocio de un vistazo.'),
 ('Reels y vídeos cortos', 'Guiones, grabación sencilla con el móvil y edición. Te decimos qué grabar y nosotros hacemos el resto.'),
 ('Textos que venden', 'Descripciones claras, con llamada a la acción y los hashtags y palabras que busca la gente de tu zona.'),
 ('Publicación y comunidad', 'Lo publicamos en el mejor momento y respondemos comentarios y mensajes para que nadie se quede sin respuesta.'),
 ('Informe cada mes', 'Qué ha funcionado, cuánta gente te ha visto y te ha escrito, y qué cambiamos el mes siguiente.'),
]
STEPS = [('Nos conocemos', '15 minutos para entender tu negocio, tu cliente y cómo quieres que te vean.'),
         ('Plan del mes', 'Te enviamos el calendario con las publicaciones y lo ajustamos contigo.'),
         ('Creamos y publicamos', 'Diseñamos, editamos y publicamos. Tú solo nos mandas fotos o vídeos de tu día a día.'),
         ('Medimos y mejoramos', 'Cada mes vemos los números y repetimos lo que trae clientes.')]
PLANS = [('Arranque', False, ['1 red social', '8 publicaciones al mes', 'Diseño con tu marca', 'Informe mensual']),
         ('Crecimiento', True, ['2 redes sociales', '12 publicaciones al mes, con reels', 'Respuesta a comentarios y mensajes', 'Informe y reunión mensual']),
         ('A medida', False, ['Las redes que necesites', 'Campañas de anuncios en Meta', 'Grabación en tu negocio', 'Lo que tu negocio pida'])]
FAQ = [('¿Tengo que grabar yo los vídeos?', 'Te decimos exactamente qué grabar con el móvil, en pocos minutos. Si lo prefieres, vamos a tu negocio y grabamos nosotros.'),
       ('¿Hay permanencia?', 'No. Trabajamos mes a mes y puedes dejarlo cuando quieras.'),
       ('¿Cuánto cuesta?', 'Depende de cuántas redes y publicaciones necesites. En la llamada de 15 minutos te damos un precio cerrado.'),
       ('¿Y si ya tengo redes?', 'Mejor: partimos de lo que tienes, vemos qué funciona y lo ordenamos.')]

def card(t, p, n=None):
    num = f'<span class="rs-num">{n:02d}</span>' if n else ''
    return f'<div class="rs-card">{num}<h3>{t}</h3><p>{p}</p></div>'

main = f'''<main>
<div class="wrap page-hero">
  <div class="breadcrumb"><a href="index.html">Inicio</a><span>/</span><span>Redes sociales</span></div>
  <div class="ph-grid"><div class="ph-main"><h1>Gestión de redes sociales en Granada: <span class="hl-hand">tus redes al día</span> sin que tengas que pensar en ellas</h1>
  <p class="lead">Nos encargamos de tu Instagram, TikTok y Facebook: ideas, diseño, vídeos cortos, textos y publicación. Tú solo nos mandas fotos de tu día a día.</p>
  <div class="cta-row" style="margin-top:22px;">
      <a class="btn btn-accent btn-cta" href="contacto.html">Quiero que llevéis mis redes</a>
      <a class="btn btn-ghost" href="https://wa.me/34620762842?text=Hola%2C%20me%20interesa%20la%20gesti%C3%B3n%20de%20redes%20sociales" target="_blank" rel="noopener">Escribir por WhatsApp</a>
    </div>
  <div class="rs-plat">{''.join(f"<span>{svg}{n}</span>" for n, svg in PLAT)}</div></div></div>
</div>
<section>
  <div class="wrap">
    <div class="section-head"><h2>Qué hacemos por tus redes</h2><p>Todo lo que hace falta para que tu negocio se vea, guste y reciba mensajes.</p></div>
    <div class="rs-grid">{''.join(card(t, p) for t, p in CARDS)}</div>
  </div>
</section>
<section class="band-light">
  <div class="wrap">
    <div class="section-head"><h2>Así trabajamos</h2></div>
    <div class="rs-grid" style="grid-template-columns:repeat(4,1fr)">{''.join(card(t, p, i + 1) for i, (t, p) in enumerate(STEPS))}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><h2>Así llevamos nuestras propias redes</h2><p>Publicaciones reales de nuestro Instagram. Toca una para verla.</p></div>
    {ig_grid('rs-feed', 4)}
  </div>
</section>
<section class="band-light">
  <div class="wrap">
    <div class="section-head"><h2>Elige cómo empezar</h2><p>Sin permanencia. En la llamada te damos el precio cerrado del plan que encaje contigo.</p></div>
    <div class="rs-plans">{''.join(f'<div class="rs-plan{" hl" if hl else ""}"><h3>{n}</h3><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul><a class="btn btn-primary" href="contacto.html">Pedir precio</a></div>' for n, hl, li in PLANS)}</div>
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
      <h2>¿Empezamos con tus redes este mes?</h2>
      <p>En 15 minutos vemos cómo están tus redes hoy y qué haríamos. Sin compromiso.</p>
      <div class="cta-row" style="justify-content:center;">
        <a class="btn btn-accent btn-cta" href="contacto.html">Reservar llamada gratis</a>
        <a class="btn btn-ghost" style="border-color:rgba(255,255,255,0.35);color:#fff;" href="https://wa.me/34620762842" target="_blank" rel="noopener">Escribir por WhatsApp</a>
      </div>
    </div>
  </div>
</section>
</main>'''

open('redes-sociales.html', 'w', encoding='utf-8').write(head + main + foot)
print('ok')
