#!/usr/bin/env python3
"""v3 por páginas: titulares y llamadas a la acción, reseñas reales en el inicio, tarjeta de redes,
página de desarrollo web, Instagram en Nosotros, blog con portadas y página nueva de redes sociales."""
import re, html as H

def rd(f): return open(f, encoding='utf-8').read()
def wr(f, s): open(f, 'w', encoding='utf-8').write(s)
def rep(s, a, b, n=1):
    assert a in s, ('NO ENCONTRADO', a[:90]); return s.replace(a, b, n)

GEN_P = '<p>Reserva 15 minutos gratis: vemos tu negocio y te decimos cuántas horas puedes recuperar y cómo.</p>'
CTA_H2 = '<h2>Cada semana que esperas son horas que no vuelven</h2>'

HEROES = {
 'index.html': ('<h1>Agencia de IA y marketing en Granada: más clientes, menos tareas repetitivas</h1>',
   '<h1>Más clientes para tu negocio, <span class="hl-hand">sin vivir pegado al móvil</span></h1>',
   'Contestamos tus llamadas y WhatsApp, llenamos tu agenda y hacemos que te encuentren en Google. Tú te ocupas de tu negocio.',
   'Somos Crecemia, una agencia de Granada. Hacemos tu web, llevamos tus redes y te montamos un asistente que contesta llamadas y WhatsApp cuando tú no puedes.'),
 'chatbots.html': ('<h1>El chatbot que responde por ti, no un contestador automático</h1>',
   '<h1>Tu WhatsApp contesta al momento, también a las once de la noche</h1>', None, None),
 'voz.html': ('<h1>Que nadie más se quede sin que le cojan el teléfono</h1>',
   '<h1>Que ninguna llamada de un cliente se quede sin contestar</h1>', None, None),
 'automatizaciones.html': ('<h1>Tus programas, trabajando solos — sin que nadie copie un dato a mano</h1>',
   '<h1>Deja de copiar datos a mano de un programa a otro</h1>', None, None),
 'web.html': ('<h1>Una web pensada para convertir, no solo para existir</h1>',
   '<h1>Desarrollo web en Granada: webs a medida que te traen clientes</h1>',
   'Rápida, clara y conectada a tu WhatsApp o tu CRM desde el primer día.',
   'Diseñamos y programamos tu web desde cero: rápida, cómoda en el móvil y pensada para que te llamen, te escriban o reserven. Desde 199 €, pago único.'),
 'sobre-nosotros.html': ('<h1>Crecemia: agencia de IA en Granada</h1>',
   '<h1>Somos Crecemia, una agencia pequeña de Granada</h1>',
   'Un solo objetivo: que la IA haga el trabajo repetitivo, no que sea otro proyecto que gestionar.',
   'Hacemos webs, llevamos redes sociales y montamos asistentes con IA para negocios de aquí. Hablas directamente con quien hace el trabajo.'),
 'contacto.html': ('<h1>Reserva 15 minutos y te decimos qué automatizar ya</h1>',
   '<h1>Cuéntanos qué necesitas y te llamamos hoy</h1>', None, None),
 'blog.html': ('<h1>IA, marketing y posicionamiento para negocios</h1>',
   '<h1>Ideas para conseguir más clientes</h1>',
   'Guías claras, con datos y fuentes, para que decidas qué te compensa automatizar y cómo conseguir más clientes en Google y en ChatGPT.',
   'Guías cortas y con datos sobre webs, redes, Google y asistentes con IA, pensadas para negocios de Granada.'),
}
CTAS = {
 'web.html': ('¿Hablamos de tu web?', 'En 15 minutos vemos qué necesitas y te damos un precio cerrado. Sin compromiso.'),
 'chatbots.html': ('Que tu WhatsApp conteste aunque tú no puedas', 'En 15 minutos te enseñamos cómo quedaría en tu negocio y cuánto cuesta.'),
 'voz.html': ('Deja de perder llamadas desde la semana que viene', 'En 15 minutos te enseñamos cómo atendería tu teléfono y cuánto cuesta.'),
 'seo.html': ('Que te encuentren antes que a tu competencia', 'En 15 minutos miramos cómo sales hoy en Google y en ChatGPT, y qué haríamos.'),
 'sobre-nosotros.html': ('¿Nos tomamos un café?', 'O una llamada de 15 minutos. Te escuchamos, te damos ideas y un precio claro, sin compromiso.'),
 'automatizaciones.html': (None, 'Reserva 15 minutos gratis: te decimos qué tareas podemos quitarte de encima y cuánto cuesta.'),
}

def heroes():
    for f, (h_old, h_new, l_old, l_new) in HEROES.items():
        s = rd(f); s = rep(s, h_old, h_new)
        if l_old: s = rep(s, l_old, l_new)
        if f in CTAS:
            h2, p = CTAS[f]
            if h2: s = rep(s, CTA_H2, f'<h2>{h2}</h2>')
            s = rep(s, GEN_P, f'<p>{p}</p>')
        wr(f, s)

# ---------- Web: desarrollo web ----------
def web():
    s = rd('web.html')
    s = rep(s, '<title>Diseño de páginas web en Granada | Crecemia', '<title>Desarrollo web en Granada | Crecemia')
    s = s.replace('og:title" content="Diseño de páginas web en Granada | Crecemia', 'og:title" content="Desarrollo web en Granada | Crecemia')
    d_old = 'Diseño de páginas web en Granada pensadas para convertir visitas en llamadas y reservas. Rápidas, con SEO y GEO para que la IA te recomiende. Desde 199 €, pago único.'
    d_new = 'Desarrollo web en Granada: diseñamos y programamos webs a medida, rápidas y pensadas para que te llamen y te reserven. SEO incluido. Desde 199 €, pago único.'
    s = s.replace(d_old, d_new)
    s = rep(s, '<span>Páginas web</span></div>', '<span>Desarrollo web</span></div>')
    s = rep(s, '<h2><span class="hl">GEO</span>: para qué sirve en tu página web</h2>', '<h2>Preparada para salir en Google y en ChatGPT</h2>')
    s = s.replace('"name": "Diseño de páginas web"', '"name": "Desarrollo web"')
    wr('web.html', s)

# ---------- Inicio ----------
REVIEWS = [
 ('Camila Gauna', 'Hemos tenido una muy buena experiencia trabajando con ellos. Desde el principio todo ha sido fácil, muy buena atención , precios competitivos y, sobre todo, soluciones rápidas cuando hemos tenido problemas, que es lo que buscábamos. Daniel nos ha ayudado muchísimo durante todo el proceso, guiándonos y resolviendo  las dudas que nos han ido surgiendo, se agradece encontrar a alguien que se implica de verdad y te hace sentir que estás en buenas manos. Sin duda, muy satisfechos con el servicio y totalmente recomendables.', True, '#7A4FD1'),
 ('Costasol', 'Me ha encantado la profesionalidad a la vez que cercanía que me generaron desde el principio. Gracias', False, '#1F5BB8'),
 ('Salvador Mateos Guirado', 'Súper buena atención, un trato estupendo de Dani', False, '#0E7A43'),
 ('Alvaro S.C', '10/10 increíble servicio por parte de dani!', False, '#B3366B'),
 ('Alicia García López', 'Muy buen servicio! Lo recomiendo!!', False, '#B25E09'),
]
G_SVG = '<svg class="rv-g" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'

def reviews_html():
    cards = []
    for name, text, big, col in REVIEWS:
        ini = ''.join(w[0] for w in name.split()[:2]).upper()
        cards.append(f'<figure class="rv-card{" big" if big else ""}"><span class="rv-stars" aria-label="5 de 5 estrellas">★★★★★</span>'
                     f'<blockquote>{H.escape(text)}</blockquote><figcaption class="rv-who"><span class="rv-av" style="background:{col}">{ini}</span>'
                     f'<span><b>{H.escape(name)}</b>Reseña en Google</span></figcaption></figure>')
    return ('<section class="rv-wrap" id="resenas" aria-labelledby="rv-t"><div class="rv-top"><h2 id="rv-t">Lo que dicen nuestros clientes</h2>'
            f'<a class="rv-score" href="https://www.google.com/search?q=Crecemia+Granada" target="_blank" rel="noopener">{G_SVG}<b>5,0</b><span class="rv-stars">★★★★★</span><span>en Google</span></a></div>'
            '<div class="rv-grid">' + ''.join(cards) + '</div></section>\n')

REDES_CARD = ('<a class="sg-card" href="redes-sociales.html"><span class="sg-svc">Redes sociales</span><h3>Publicas cuando te acuerdas y nadie te escribe</h3>'
              '<p>Llevamos tu Instagram, TikTok y Facebook: ideas, diseño, vídeos y publicaciones cada semana.</p>'
              '<span class="sg-foot"><b>Plan mensual</b><span>Ver cómo funciona →</span></span></a>')

def home():
    s = rd('index.html')
    s = rep(s, '<section class="geo-lead" id="auditoria-geo">', reviews_html() + '<section class="geo-lead" id="auditoria-geo">')
    s = rep(s, '<span class="sg-svc">Páginas web</span>', '<span class="sg-svc">Desarrollo web</span>')
    s = rep(s, '<div class="sg-calc o1-final" id="calculadora">', REDES_CARD + '<div class="sg-calc o1-final" id="calculadora">')
    s = rep(s, '.sg-calc{border-radius:20px}', '.sg-calc{border-radius:20px;grid-column:1/-1}.sg-calc .o1-card{display:grid;grid-template-columns:1.1fr 1fr;gap:6px 34px;align-items:center}.sg-calc .o1-card>*{margin:0}@media(max-width:860px){.sg-calc .o1-card{display:block}}')
    wr('index.html', s)

# ---------- Nosotros: Instagram ----------
IG = [('DgFTq24jZCp', 'Las 5 fugas por las que pierdes clientes'),
      ('DfzMwOYEXxC', 'Sin internet, solo te conoce quien pasa por tu puerta'),
      ('DfrtbxFN_pB', 'Solo 4 de cada 10 empresas tenían web'),
      ('De6lK17NJOJ', 'Esta IA coge el teléfono por ti'),
      ('DewkCXqNV0U', '5 trucos de Claude que lo cambian todo')]
def ig_grid(cls='ig-grid', n=5):
    out = []
    for pid, t in IG[:n]:
        out.append(f'<a class="ig-post" href="https://www.instagram.com/p/{pid}/" target="_blank" rel="noopener">'
                   f'<img src="ig/{pid}.jpg" alt="{H.escape(t)}" loading="lazy" decoding="async" width="280" height="374"><span>{H.escape(t)}</span></a>')
    return f'<div class="{cls}">' + ''.join(out) + '</div>'

IG_ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/></svg>'
def nosotros():
    s = rd('sobre-nosotros.html')
    sec = ('<section class="ig-sec"><div class="wrap"><div class="ig-head"><div><h2>Lo que contamos en Instagram</h2>'
           '<p>Consejos cortos para negocios, casos reales y lo que vamos aprendiendo. Toca una publicación para verla.</p></div>'
           f'<a class="ig-follow" href="https://www.instagram.com/danimata.ai/" target="_blank" rel="noopener">{IG_ICON} Síguenos en @danimata.ai</a></div>'
           + ig_grid() + '</div></section>\n')
    k = s.rfind('<section>\n  <div class="wrap">\n    <div class="final-cta">')
    assert k > 0
    s = s[:k] + sec + s[k:]
    wr('sobre-nosotros.html', s)

# ---------- Blog ----------
CAT = {
 'blog-ia-empresas-espana-datos.html': ('ia', 'Datos', 'IA en España'),
 'blog-que-es-el-geo.html': ('geo', 'SEO y GEO', 'GEO'),
 'blog-chatbot-whatsapp-negocio.html': ('chat', 'Chatbots', 'WhatsApp'),
 'blog-recepcionista-virtual-ia.html': ('voz', 'Voz', 'Llamadas'),
 'blog-inteligencia-artificial-granada.html': ('ia', 'IA', 'Granada'),
 'blog-cuanto-cuesta-un-chatbot.html': ('chat', 'Chatbots', 'Precios'),
 'blog-seo-local-granada.html': ('geo', 'SEO y GEO', 'Google Maps'),
 'blog-pagina-web-granada-precio.html': ('web', 'Webs', 'Tu web'),
 'blog-automatizar-facturas-pyme.html': ('auto', 'Automatización', 'Facturas'),
 'blog-ia-clinicas-dentales.html': ('sector', 'Sectores', 'Clínicas'),
 'blog-reservas-restaurante-whatsapp.html': ('sector', 'Sectores', 'Reservas'),
}
def blog():
    s = rd('blog.html')
    cards = re.findall(r'<li class="blog-card"><a href="([^"]+)">(.*?)</a></li>', s, re.S)
    assert len(cards) >= 8, len(cards)
    out = []
    cats = []
    for i, (href, inner) in enumerate(cards):
        c, label, word = CAT.get(href, ('ia', 'Blog', 'Ideas'))
        if label not in cats: cats.append(label)
        out.append(f'<li class="blog-card{" feat" if i == 0 else ""}" data-cat="{label}"><a href="{href}">'
                   f'<span class="blog-cover c-{c}"><i>{label}</i><b>{word}</b></span><span class="blog-body">{inner}</span></a></li>')
    filt = ('<div class="blog-filters" role="group" aria-label="Filtrar por tema"><button type="button" aria-pressed="true" data-f="">Todos</button>'
            + ''.join(f'<button type="button" aria-pressed="false" data-f="{c}">{c}</button>' for c in cats) + '</div>')
    js = ('<script>(function(){var b=document.querySelectorAll(".blog-filters button"),c=document.querySelectorAll(".blog-card");'
          'b.forEach(function(x){x.addEventListener("click",function(){var f=x.dataset.f;b.forEach(function(y){y.setAttribute("aria-pressed",y===x)});'
          'c.forEach(function(k,i){k.hidden=!!f&&k.dataset.cat!==f;k.classList.toggle("feat",!f&&i===0)});});});})();</script>')
    i = s.find('<ul class="blog-list">'); j = s.find('</ul>', i) + 5
    s = s[:i] + filt + '<ul class="blog-list">' + ''.join(out) + '</ul>' + js + s[j:]
    wr('blog.html', s)
    # portada en cada artículo
    for href, (c, label, word) in CAT.items():
        a = rd(href)
        if 'post-cover' in a: continue
        a = rep(a, '<header class="post-head">', f'<div class="post-cover c-{c}" aria-hidden="true"><i>{label}</i><b>{word}</b></div>\n  <header class="post-head">')
        wr(href, a)

if __name__ == '__main__':
    heroes(); web(); home(); nosotros(); blog()
    print('ok')
