#!/usr/bin/env python3
"""Genera el blog de Crecemia como un periódico: páginas de artículos nuevos, portada (blog.html),
feed RSS (feed.xml) y sitemap. Uso: python3 tools_blog.py"""
import re, json, html as H, datetime as dt
from blog_data import SECTIONS, OLD_POSTS, NEW_POSTS, FACTS

SITE = 'https://www.crecemia.es/'
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

def fecha(d, dia=False):
    x = dt.date.fromisoformat(d)
    s = f'{x.day} de {MESES[x.month-1]} de {x.year}'
    return (DIAS[x.weekday()].capitalize() + ', ' + s) if dia else s

def esc(s): return H.escape(s, quote=True)
def rd(f): return open(f, encoding='utf-8').read()
def wr(f, s): open(f, 'w', encoding='utf-8').write(s)

ALL = sorted(OLD_POSTS + NEW_POSTS, key=lambda p: (p['date'], p in NEW_POSTS), reverse=True)

def cover(p, cls='blog-cover'):
    return f'<span class="{cls} c-{SECTIONS[p["section"]]}"><i>{esc(p["section"])}</i><b>{esc(p["word"])}</b></span>'

# ---------- páginas de artículo ----------
def article_page(p):
    t = rd('blog-que-es-el-geo.html')
    url = f'{SITE}{p["slug"]}.html'
    head, rest = t.split('<main>', 1)
    foot = rest.split('</main>', 1)[1]
    head = re.sub(r'<title>[^<]*</title>', f'<title>{esc(p["title"])} | Crecemia</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(p['desc']), head)
    head = re.sub(r'(og:description" content=")[^"]*', lambda m: m.group(1) + esc(p['desc']), head)
    head = re.sub(r'(og:title" content=")[^"]*', lambda m: m.group(1) + esc(p['title']) + ' | Crecemia', head)
    head = head.replace(f'{SITE}blog-que-es-el-geo.html', url)
    post = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p['title'], "description": p['desc'],
            "datePublished": p['date'], "dateModified": p['date'], "inLanguage": "es-ES", "mainEntityOfPage": url, "url": url,
            "image": f"{SITE}og-image.jpg", "keywords": p.get('keywords', ''), "articleSection": p['section'],
            "author": {"@id": f"{SITE}#organization"}, "publisher": {"@id": f"{SITE}#organization"}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}blog.html"},
        {"@type": "ListItem", "position": 3, "name": p['title'], "item": url}]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (post, crumbs, faq))
    for typ in ('BlogPosting', 'BreadcrumbList', 'FAQPage'):
        head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "' + typ + r'".*?</script>', '', head, flags=re.S)
    head = head.replace('</head>', ld + '\n</head>', 1)
    more = [x for x in ALL if x['slug'] != p['slug']][:6]
    main = f'''<main>
<article class="post wrap">
  <div class="breadcrumb"><a href="/">Inicio</a><span>/</span><a href="blog.html">Blog</a><span>/</span><span>{esc(p["title"])}</span></div>
  <div class="post-cover c-{SECTIONS[p["section"]]}" aria-hidden="true"><i>{esc(p["section"])}</i><b>{esc(p["word"])}</b></div>
  <header class="post-head">
    <p class="post-meta"><time datetime="{p["date"]}">{fecha(p["date"])}</time> · {p["min"]} min de lectura · Equipo Crecemia</p>
    <h1>{esc(p["title"])}</h1>
    <p class="post-lead">{esc(p["lead"])}</p>
  </header>
  <div class="post-body">
{p["body"]}
  </div>
  <section class="post-faq" aria-labelledby="faq-t">
    <h2 id="faq-t">Preguntas frecuentes</h2>
    {''.join(f'<details class="post-faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p["faq"])}
  </section>
  <aside class="post-cta">
    <p class="post-cta-t">¿Lo vemos con tu negocio?</p>
    <p>15 minutos, gratis y sin compromiso. Te decimos qué haríamos y cuánto cuesta.</p>
    <a class="btn btn-primary btn-lg btn-cta" href="contacto.html">Quiero mi llamada gratis</a>
  </aside>
  <nav class="post-more" aria-label="Más artículos"><p class="post-more-t">Sigue leyendo</p><ul>{''.join(f'<li><a href="{x["slug"]}.html">{esc(x["title"])}</a></li>' for x in more)}</ul></nav>
</article>
</main>'''
    wr(f'{p["slug"]}.html', head + main + foot)

# ---------- portada del blog ----------
def card(p, cls=''):
    return (f'<li class="blog-card{cls}" data-cat="{esc(p["section"])}"><a href="{p["slug"]}.html">{cover(p)}'
            f'<span class="blog-body"><span class="blog-card-meta"><time datetime="{p["date"]}">{fecha(p["date"])}</time> · {p["min"]} min</span>'
            f'<h2>{esc(p["title"])}</h2><p>{esc(p["desc"])}</p><span class="blog-more">Leer artículo →</span></span></a></li>')

def blog_index():
    s = rd('blog.html')
    today = max(p['date'] for p in ALL)
    s = re.sub(r'<title>[^<]*</title>', '<title>Blog de Crecemia: noticias, curiosidades y guías de marketing digital</title>', s)
    desc = 'El diario de Crecemia: curiosidades, datos y guías sobre redes sociales, publicidad en Google y Meta, webs, SEO e inteligencia artificial para negocios de Granada.'
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, s)
    s = re.sub(r'(og:description" content=")[^"]*', lambda m: m.group(1) + desc, s)
    s = re.sub(r'(og:title" content=")[^"]*', lambda m: m.group(1) + 'Blog de Crecemia: noticias, curiosidades y guías', s)
    if 'application/rss+xml' not in s:
        s = s.replace('</head>', '<link rel="alternate" type="application/rss+xml" title="Blog de Crecemia" href="https://www.crecemia.es/feed.xml">\n</head>', 1)
    # ItemList para SEO
    il = {"@context": "https://schema.org", "@type": "Blog", "name": "Blog de Crecemia", "url": f"{SITE}blog.html", "inLanguage": "es-ES",
          "blogPost": [{"@type": "BlogPosting", "headline": p['title'], "url": f"{SITE}{p['slug']}.html", "datePublished": p['date']} for p in ALL]}
    s = re.sub(r'<script type="application/ld\+json" id="blog-list">.*?</script>', '', s, flags=re.S)
    s = s.replace('</head>', f'<script type="application/ld+json" id="blog-list">{json.dumps(il, ensure_ascii=False)}</script>\n</head>', 1)

    lead, side, rest = ALL[0], ALL[1:5], ALL[1:]
    secs = [x for x in SECTIONS if any(p['section'] == x for p in ALL)]
    ticker = ''.join(f'<li><b>¿Sabías que…?</b> {esc(t)} <small>({esc(src)})</small></li>' for t, src in FACTS)
    main = f'''<main>
<div class="wrap news">
  <div class="breadcrumb"><a href="/">Inicio</a><span>/</span><span>Blog</span></div>
  <header class="news-mast">
    <p class="news-date"><span data-today>{fecha(today, True)}</span> · Granada · Actualizado el {fecha(today)}</p>
    <h1>El Diario de Crecemia</h1>
    <p class="news-sub">Curiosidades, datos y guías para que tu negocio consiga más clientes en internet.</p>
  </header>
  <div class="news-ticker" aria-label="Datos curiosos"><ul>{ticker}{ticker}</ul></div>
  <section class="news-top">
    <a class="news-lead" href="{lead["slug"]}.html">{cover(lead, 'blog-cover news-lead-cover')}
      <span class="news-lead-body"><span class="news-kicker">Última hora · <time datetime="{lead["date"]}">{fecha(lead["date"])}</time></span><h2>{esc(lead["title"])}</h2><p>{esc(lead["desc"])}</p><span class="blog-more">Leer artículo →</span></span></a>
    <aside class="news-side"><p class="news-side-t">Lo último</p><ol>{''.join(f'<li><a href="{p["slug"]}.html"><span class="news-sec">{esc(p["section"])}</span>{esc(p["title"])}<time datetime="{p["date"]}">{fecha(p["date"])}</time></a></li>' for p in side)}</ol></aside>
  </section>
  <div class="blog-filters" role="group" aria-label="Filtrar por sección"><button type="button" aria-pressed="true" data-f="">Todas las secciones</button>{''.join(f'<button type="button" aria-pressed="false" data-f="{esc(x)}">{esc(x)}</button>' for x in secs)}</div>
  <ul class="blog-list">{''.join(card(p) for p in rest)}</ul>
  <aside class="news-sub-box"><div><p class="news-side-t">Cada semana, algo nuevo</p><p>Publicamos curiosidades y guías nuevas cada semana. Síguelo por <a href="feed.xml">RSS</a> o en nuestro <a href="https://www.instagram.com/danimata.ai/" target="_blank" rel="noopener">Instagram</a>.</p></div><a class="btn btn-primary" href="contacto.html">Hablar con nosotros</a></aside>
</div>
</main>
<script>(function(){{var b=document.querySelectorAll(".blog-filters button"),c=document.querySelectorAll(".blog-list .blog-card");b.forEach(function(x){{x.addEventListener("click",function(){{var f=x.dataset.f;b.forEach(function(y){{y.setAttribute("aria-pressed",y===x)}});c.forEach(function(k){{k.hidden=!!f&&k.dataset.cat!==f}});}});}});}})();</script>'''
    i = s.find('<main>'); j = s.find('</main>') + len('</main>')
    # quitar el script de filtros antiguo si estaba justo detrás
    tail = s[j:]
    tail = re.sub(r'^\s*<script>\(function\(\)\{var b=document\.querySelectorAll\("\.blog-filters button"\).*?</script>', '', tail, flags=re.S)
    s = s[:i] + main + tail
    wr('blog.html', s)

def feed():
    items = ''.join(f'<item><title>{esc(p["title"])}</title><link>{SITE}{p["slug"]}.html</link><guid>{SITE}{p["slug"]}.html</guid>'
                    f'<pubDate>{dt.datetime.fromisoformat(p["date"]+"T09:00:00").strftime("%a, %d %b %Y %H:%M:%S +0100")}</pubDate>'
                    f'<category>{esc(p["section"])}</category><description>{esc(p["desc"])}</description></item>' for p in ALL)
    wr('feed.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Blog de Crecemia</title><link>{SITE}blog.html</link>'
       f'<description>Curiosidades, datos y guías de marketing digital para negocios.</description><language>es-es</language>{items}</channel></rss>\n')

def sitemap():
    s = rd('sitemap.xml')
    today = max(p['date'] for p in ALL)
    for p in NEW_POSTS:
        loc = f'{SITE}{p["slug"]}.html'
        if loc not in s:
            s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{p["date"]}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n</urlset>')
    s = re.sub(r'(<loc>https://www.crecemia.es/blog.html</loc>\s*<lastmod>)[^<]*', r'\g<1>' + today, s)
    wr('sitemap.xml', s)

if __name__ == '__main__':
    for p in NEW_POSTS: article_page(p)
    blog_index(); feed(); sitemap()
    print('ok', len(ALL), 'artículos')
