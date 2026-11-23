#!/usr/bin/env python3
"""v3 global: quita etiquetas pequeñas encima de títulos, nueva tipografía de títulos,
barra superior y pie más humanos, menú con Redes sociales y Desarrollo web."""
import re, glob

FONT_OLD_1 = 'family=Sora:wght@400;600;700;800&family=Inter'
FONT_OLD_2 = 'family=Sora:wght@700;800&family=Inter'
FONT_NEW = 'family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Sora:wght@800&family=Inter'

TOPBAR_NEW = ('<span class="topbar-claim"><b>Agencia en Granada</b> · ¿Hablamos? '
              '<a href="tel:+34620762842">620 76 28 42</a></span>')
FOOT_TAG_OLD = 'Implantamos la IA que atiende, agenda y factura por tu negocio. Granada.'
FOOT_TAG_NEW = 'Webs, redes sociales y asistentes con IA para negocios de Granada. Trato cercano y precios claros.'

def eyebrows(s):
    n = 0
    for pat in [r'<div class="hero-eyebrow">.*?</div>\s*',
                r'<div class="eyebrow">(?:(?!</div>).)*</div>\s*',
                r'<div class="eyebrow-inline">(?:(?!</div>).)*</div>\s*',
                r'<span class="eyebrow-inline">(?:(?!</span>).)*</span>\s*']:
        s, k = re.subn(pat, '', s, flags=re.S); n += k
    return s, n

def nav(s):
    # Redes sociales en el desplegable de servicios
    if 'href="redes-sociales.html"' not in s.split('</header>')[0]:
        s = s.replace('<a href="automatizaciones.html">Automatizaciones</a>\n</div>',
                      '<a href="automatizaciones.html">Automatizaciones</a>\n<a href="redes-sociales.html">Redes sociales</a>\n</div>', 1)
    s = re.sub(r'(<a href="web\.html"[^>]*>)Páginas web(</a>)', r'\1Desarrollo web\2', s)
    # pie: servicios
    s = s.replace('<li><a href="web.html">Páginas web</a></li>',
                  '<li><a href="web.html">Desarrollo web</a></li><li><a href="redes-sociales.html">Redes sociales</a></li>')
    return s

def run():
    files = [f for f in glob.glob('*.html') if not f.startswith('google')]
    report = []
    for f in files:
        s = open(f, encoding='utf-8').read(); o = s
        s = s.replace(FONT_OLD_1, FONT_NEW).replace(FONT_OLD_2, FONT_NEW)
        s = re.sub(r"font(-family)?:([^;\"']*?)\bSora\b", lambda m: m.group(0).replace('Sora', "'Bricolage Grotesque'"), s)
        s = s.replace("''Bricolage Grotesque''", "'Bricolage Grotesque'")
        s, n = eyebrows(s)
        s = re.sub(r'<span class="topbar-claim">.*?</span></div></aside>', TOPBAR_NEW + '</div></aside>', s, flags=re.S)
        s = s.replace(FOOT_TAG_OLD, FOOT_TAG_NEW)
        s = nav(s)
        s = s.replace('styles.css?v=24', 'styles.css?v=25')
        if s != o:
            open(f, 'w', encoding='utf-8').write(s); report.append(f'{f}:{n}')
    # CSS
    c = open('styles.css', encoding='utf-8').read()
    if '/* v3 */' not in c:
        c = re.sub(r"'Sora'", "'Bricolage Grotesque'", c)
        # el logo sigue con Sora
        c = c.replace(".brand{display:flex;align-items:center;gap:9px;font-family:'Bricolage Grotesque'", ".brand{display:flex;align-items:center;gap:9px;font-family:'Sora'")
        c = c.replace(".intro-logo span{font-family:'Bricolage Grotesque'", ".intro-logo span{font-family:'Sora'")
        c = c.replace(".brand{font-family:'Bricolage Grotesque'", ".brand{font-family:'Sora'")
        c += open('/home/claude/nexbia/v3.css', encoding='utf-8').read()
        open('styles.css', 'w', encoding='utf-8').write(c)
    print(' '.join(sorted(report)))

if __name__ == '__main__':
    run()
