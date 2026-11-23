# -*- coding: utf-8 -*-
"""Datos del blog de Crecemia. Cada artículo nuevo se añade a NEW_POSTS (con su cuerpo en HTML)
y luego se ejecuta tools_blog.py, que genera la página del artículo, la portada del blog,
el feed RSS y el sitemap."""

# Secciones del "periódico" y su color de portada
SECTIONS = {
    'Curiosidades': 'cur',
    'Redes sociales': 'redes',
    'Publicidad': 'ads',
    'SEO y GEO': 'geo',
    'IA y automatización': 'ia',
    'Webs': 'web',
    'Sectores': 'sector',
}

# Artículos que ya existían (la página no se regenera; solo se listan)
OLD_POSTS = [
    dict(slug='blog-ia-empresas-espana-datos', title='Cuántas empresas usan IA en España: datos 2025-2026', date='2026-11-18', min=5, section='IA y automatización', word='IA en España',
         desc='Qué porcentaje de empresas españolas usa inteligencia artificial según el INE, cuánto ha crecido y qué significa para una pyme de Granada.'),
    dict(slug='blog-que-es-el-geo', title='Qué es el GEO y cómo conseguir que ChatGPT recomiende tu negocio', date='2026-11-18', min=6, section='SEO y GEO', word='GEO',
         desc='El GEO es el posicionamiento en inteligencia artificial. Te explicamos qué es, por qué importa ya en España y qué hacer para que ChatGPT o Google te recomienden.'),
    dict(slug='blog-chatbot-whatsapp-negocio', title='Chatbot de WhatsApp para tu negocio: cuándo compensa y cuándo no', date='2026-11-18', min=5, section='IA y automatización', word='WhatsApp',
         desc='Qué hace un chatbot de WhatsApp para una pyme, qué datos hay sobre cómo prefieren contactar los clientes y cómo saber si a tu negocio le compensa.'),
    dict(slug='blog-recepcionista-virtual-ia', title='Recepcionista virtual con IA: qué es, qué hace y qué no', date='2026-11-18', min=5, section='IA y automatización', word='Llamadas',
         desc='Qué es una recepcionista virtual con IA, cómo atiende llamadas en tu número de siempre y en qué casos conviene más una persona. Con datos honestos.'),
    dict(slug='blog-inteligencia-artificial-granada', title='Inteligencia artificial en Granada: qué puede hacer hoy una pyme granadina', date='2026-11-18', min=5, section='IA y automatización', word='Granada',
         desc='Granada se ha convertido en un polo de inteligencia artificial. Qué significa para los negocios de la ciudad y qué pueden automatizar hoy.'),
    dict(slug='blog-cuanto-cuesta-un-chatbot', title='Cuánto cuesta un chatbot para tu empresa en 2026', date='2026-11-18', min=4, section='IA y automatización', word='Precios',
         desc='Precio de un chatbot para WhatsApp y web en 2026: qué incluye, de qué depende y cuánto cuesta con nosotros. Precios orientativos y sin letra pequeña.'),
    dict(slug='blog-seo-local-granada', title='SEO local en Granada: cómo salir en Google Maps y en el mapa de resultados', date='2026-11-18', min=6, section='SEO y GEO', word='Google Maps',
         desc='Guía de SEO local para negocios de Granada: los tres factores con los que Google ordena los resultados locales y qué hacer en tu ficha, tu web y tus reseñas.'),
    dict(slug='blog-pagina-web-granada-precio', title='Página web para tu negocio en Granada: qué debe tener y cuánto cuesta', date='2026-11-18', min=5, section='Webs', word='Tu web',
         desc='Qué tiene que tener la web de una pyme en Granada para conseguir clientes, cuánto cuesta y por qué casi todas las empresas ya tienen una pero pocas reservan solas.'),
    dict(slug='blog-ia-clinicas-dentales', title='IA para clínicas dentales: menos llamadas, menos huecos en la agenda', date='2026-11-18', min=5, section='Sectores', word='Clínicas',
         desc='Cómo usar la IA en una clínica dental: recepcionista de voz, recordatorios por WhatsApp, citas online y avisos. Qué automatizar primero y qué dejar a la recepción.'),
    dict(slug='blog-reservas-restaurante-whatsapp', title='Reservas automáticas para restaurantes: WhatsApp, teléfono y web sin descolgar', date='2026-11-18', min=4, section='Sectores', word='Reservas',
         desc='Cómo automatizar las reservas de un restaurante o bar por WhatsApp, teléfono y web, con lista de espera y recordatorios, para no perder mesas en hora punta.'),
    dict(slug='blog-automatizar-facturas-pyme', title='Automatizar facturas en una pyme: qué se puede hacer y qué pasa con Verifactu', date='2026-11-18', min=5, section='IA y automatización', word='Facturas',
         desc='Cómo automatizar la entrada de facturas, los cobros y los recordatorios en una pyme, y qué fechas de Verifactu están vigentes hoy según el BOE.'),
]

# Datos cortos para la cinta "¿Sabías que...?" de la portada (con su fuente)
FACTS = [
    ('El 54 % de los usuarios de redes en España busca información en ellas antes de comprar online.', 'IAB Spain 2026'),
    ('Google Ads arrancó en octubre de 2000 con unos 350 anunciantes.', 'Search Engine Land'),
    ('Instagram ya es la red social que más españoles usan de forma habitual: el 57,9 %.', 'CNMC'),
    ('Las marcas publican un 30 % menos en redes que hace un año, y su interacción ha subido un 29 %.', 'IAB Spain 2026'),
    ('Más de la mitad de los usuarios con smartphone entra en redes varias veces al día.', 'CNMC'),
    ('En Google Ads, la media de clics por cada 100 veces que sale un anuncio de búsqueda es de 6,6.', 'WordStream by LocaliQ 2026'),
]

L = lambda url, txt: f'<a href="{url}" target="_blank" rel="noopener">{txt}</a>'

S_IAB26 = 'https://ppc.land/spains-social-media-users-jump-to-7-2-platforms-but-42-quit-at-least-one/'
S_CNMC = 'https://www.cnmc.es/node/420468'
S_COMSCORE = 'https://www.marketingdirecto.com/anunciantes-general/publicaciones/espana-lider-en-consumo-de-redes-sociales-comscore-revela-el-impacto-de-las-redes-e-influencers'
S_IAB25 = 'https://www.modaes.com/back-stage/radiografia-de-las-redes-sociales-en-espana-caen-x-y-facebook-frente-al-liderazgo-de-whatsapp'
S_OBS26 = 'https://www.marketingdirecto.com/anunciantes-general/publicaciones/marcas-espanolas-reducen-volumen-publicaciones-disparan-703-eficiencia-redes-sociales'
S_DR27 = 'https://datareportal.com/reports/digital-2027-spain'
S_SEL = 'https://searchengineland.com/google-adwords-turns-15-a-look-back-at-the-origins-of-a-60-billion-business-234579'
S_WPN = 'https://www.webpronews.com/adwords-turns-15-google-celebrates-with-stat-heavy-timeline-infographic/'
S_SEP = 'https://www.searchenginepeople.com/?p=92255'
S_TWG = 'https://business.google.com/es/think/search-and-video/tendencias-de-busqueda-aprendizajes-de-marketing/'
S_WS26 = 'https://www.wordstream.com/blog/2026-google-ads-benchmarks'
S_SEJ_CTR = 'https://www.searchenginejournal.com/what-a-good-ctr-for-google-ads/492785/'
S_SEJ_CPL = 'https://www.searchenginejournal.com/what-is-a-good-ctr-for-google-ads/'
S_FB26 = 'https://searchengineland.com/facebook-ad-costs-fall-as-traffic-and-lead-performance-improvements-report-488433'
S_RELAUD = 'https://www.relevantaudience.com/general-topics/history-of-google-ads/'

NEW_POSTS = [
 dict(slug='blog-curiosidades-redes-sociales-espana', date='2026-11-24', min=5, section='Curiosidades', word='¿Sabías que…?',
  title='12 curiosidades de las redes sociales en España que quizá no sabías (2026)',
  desc='Cuánta gente usa redes en España, cuál es la red más usada, cuántas veces al día entramos y por qué las marcas publican menos. Doce datos curiosos con su fuente.',
  keywords='curiosidades redes sociales España 2026',
  lead='Las redes sociales forman parte del día a día de casi todo el mundo, pero algunos datos sorprenden. Hemos reunido doce, todos con su fuente, y al final te contamos qué significan para un negocio.',
  body=f'''
<h2>Cuánta gente las usa</h2>
<ol class="facts">
<li><strong>Casi 9 de cada 10 internautas usan redes.</strong> En 2026, el 86 % de los españoles conectados de entre 12 y 75 años usa al menos una red social, unos 33,1 millones de personas, según el {L(S_IAB26, 'Estudio de Redes Sociales 2026 de IAB Spain')}.</li>
<li><strong>Más de 40 millones de perfiles.</strong> España tenía en octubre de 2026 unos 40,5 millones de identidades activas en redes, el 84,7 % de la población, según {L(S_DR27, 'DataReportal')}. No son personas únicas: una misma persona puede tener varias cuentas.</li>
<li><strong>Los mayores también están.</strong> Entre los internautas de 61 a 75 años, el 80 % tiene redes sociales, según el {L(S_IAB25, 'estudio de IAB Spain de 2025')}.</li>
</ol>
<h2>Qué redes ganan y cuáles pierden</h2>
<ol class="facts" start="4">
<li><strong>Instagram ya es la red más usada.</strong> El 57,9 % de los internautas la usa de forma habitual, por delante de Facebook (52 %), según el {L(S_CNMC, 'Panel de Hogares de la CNMC')} del último trimestre de 2025.</li>
<li><strong>TikTok no para de crecer.</strong> Llega ya al 31 % de los internautas, mientras X (antes Twitter) baja al 16,3 % ({L(S_CNMC, 'CNMC')}).</li>
<li><strong>WhatsApp sigue siendo el rey.</strong> Llega al 94 % de los usuarios de redes cada mes, y el 97 % de quienes lo usan lo abre a diario ({L(S_IAB26, 'IAB Spain 2026')}).</li>
<li><strong>Donde más tiempo pasamos no es donde crees.</strong> En el estudio de 2025, la plataforma en la que más tiempo pasaban los usuarios era Spotify, por delante de TikTok y WhatsApp ({L(S_IAB25, 'IAB Spain 2025')}).</li>
</ol>
<h2>Cuánto tiempo y para qué</h2>
<ol class="facts" start="8">
<li><strong>Varias veces al día.</strong> El 52,6 % de los usuarios con smartphone entra en redes varias veces cada día ({L(S_CNMC, 'CNMC')}).</li>
<li><strong>22 horas al mes.</strong> En junio de 2025, los españoles pasaron de media unas 22 horas al mes en redes, un 9 % más que un año antes, según {L(S_COMSCORE, 'Comscore')}.</li>
<li><strong>Las redes deciden compras.</strong> El 54 % de los usuarios busca información en redes antes de comprar online, seis puntos más que el año anterior ({L(S_IAB26, 'IAB Spain 2026')}).</li>
</ol>
<h2>Lo que hacen las marcas</h2>
<ol class="facts" start="11">
<li><strong>Publican menos… y les va mejor.</strong> Las marcas analizadas por el {L(S_OBS26, 'Observatorio de Marcas en Redes Sociales 2026 de IAB Spain')} bajaron de 1.722 a 1.208 publicaciones al año (un 30 % menos), y su interacción media subió del 0,91 % al 1,16 %.</li>
<li><strong>Pero se comparte menos.</strong> En ese mismo estudio, la viralidad orgánica de las marcas cayó un 23 % en un año: cada vez cuesta más que un contenido se mueva solo.</li>
</ol>
<h2>Qué significa para tu negocio</h2>
<p>Tus clientes están en redes, entran varias veces al día y más de la mitad mira lo que publicas antes de comprar. Lo que funciona ya no es publicar mucho, sino publicar mejor: vídeos cortos con un guion claro, constancia y responder rápido a quien te escribe.</p>
<p>Si quieres que alguien se encargue de eso, mira cómo trabajamos en <a href="redes-sociales.html">gestión de redes sociales</a>.</p>
''',
  faq=[('¿Cuál es la red social más usada en España?', 'Si hablamos de mensajería, WhatsApp. Como red social, Instagram: el 57,9 % de los internautas la usa de forma habitual, según la CNMC.'),
       ('¿Cuánta gente usa redes sociales en España?', 'El 86 % de los internautas de 12 a 75 años, unos 33,1 millones de personas, según IAB Spain 2026.')]),

 dict(slug='blog-historia-google-ads-curiosidades', date='2026-11-24', min=5, section='Curiosidades', word='Año 2000',
  title='Google Ads cumple 26 años: curiosidades del anuncio que cambió internet',
  desc='Cómo nació Google Ads en el año 2000 con 350 anunciantes, por qué al principio se pagaba por impresiones y qué datos tiene hoy. Historia y curiosidades con fuentes.',
  keywords='historia de Google Ads curiosidades AdWords',
  lead='Hoy casi cualquier negocio puede anunciarse en Google en una tarde. En el año 2000 era una novedad absoluta. Repasamos cómo empezó y qué ha cambiado.',
  body=f'''
<h2>Así empezó todo</h2>
<ol class="facts">
<li><strong>350 anunciantes.</strong> AdWords, el antiguo nombre de Google Ads, salió en octubre de 2000 tras una prueba de alrededor de un mes con unos 350 anunciantes ({L(S_SEL, 'Search Engine Land')}).</li>
<li><strong>No fue el primer intento.</strong> Unos meses antes, en agosto de 2000, Google ya vendía «Premium Sponsorships»: anuncios que gestionaba un equipo comercial y que se cobraban por cada mil impresiones ({L(S_SEL, 'Search Engine Land')}).</li>
<li><strong>Al principio no se pagaba por clic.</strong> Los primeros anuncios eran textos cortos a la derecha de los resultados, y se pagaba por las veces que se mostraban, no por los clics ({L(S_RELAUD, 'Relevant Audience')}). El modelo de pago por clic que conocemos llegó después.</li>
<li><strong>El lema de autoservicio.</strong> El 23 de octubre de 2000 Google anunció que cualquier anunciante podía comprar sus propios anuncios sin pasar por un comercial ({L(S_WPN, 'WebProNews')}).</li>
</ol>
<h2>De 20 millones de búsquedas a billones</h2>
<ol class="facts" start="5">
<li><strong>Un Google pequeño.</strong> En 2000, Google decía recibir más de 20 millones de búsquedas al día ({L(S_SEL, 'Search Engine Land')}).</li>
<li><strong>Un Google gigante.</strong> Hoy, según la propia Google, se hacen más de 5 billones de búsquedas al año ({L(S_TWG, 'Think with Google')}).</li>
<li><strong>Un millón de anunciantes.</strong> Al cumplir 15 años, en 2015, AdWords ya superaba el millón de anunciantes ({L(S_SEL, 'Search Engine Land')}).</li>
<li><strong>Cambio de nombre.</strong> En 2018, AdWords pasó a llamarse Google Ads, porque ya no eran solo anuncios de texto ({L(S_SEP, 'Search Engine People')}).</li>
</ol>
<h2>Y hoy, ¿qué resultados da?</h2>
<p>El estudio anual de {L(S_WS26, 'WordStream by LocaliQ')} analizó más de 13.000 campañas de búsqueda en Estados Unidos entre abril de 2025 y marzo de 2026. Las medias fueron:</p>
<ul>
<li><strong>6,64 %</strong> de clics por impresión ({L(S_SEJ_CTR, 'fuente')}).</li>
<li><strong>8,18 %</strong> de clics que acaban en contacto o venta.</li>
<li>Por primera vez en cinco años, el coste por contacto conseguido <strong>bajó</strong>.</li>
</ul>
<p>Son datos de Estados Unidos y cambian mucho según el sector, pero dejan clara una cosa: un anuncio de búsqueda llega a quien ya está buscando lo que vendes.</p>
<p>Si quieres probarlo en tu negocio, mira cómo montamos las campañas en <a href="publicidad-online.html">publicidad online</a>.</p>
''',
  faq=[('¿Cuándo se creó Google Ads?', 'En octubre de 2000, con el nombre de AdWords y unos 350 anunciantes. En 2018 pasó a llamarse Google Ads.'),
       ('¿Cuál es el CTR medio en Google Ads?', 'Según WordStream by LocaliQ (2026, Estados Unidos), la media de todos los sectores en anuncios de búsqueda es del 6,64 %.')]),

 dict(slug='blog-cuanto-cuesta-un-clic-google-meta-ads', date='2026-11-24', min=5, section='Publicidad', word='Coste por clic',
  title='Cuánto cuesta un clic en Google Ads y en Meta Ads: datos 2026 y qué esperar',
  desc='Clics por impresión, coste por clic y coste por contacto en Google Ads y en Facebook e Instagram según los datos de 2026. Qué cambia entre una y otra y cuál te conviene.',
  keywords='cuánto cuesta un clic Google Ads Meta Ads 2026',
  lead='Antes de invertir en anuncios, la pregunta es siempre la misma: ¿cuánto me va a costar cada cliente? Estos son los datos de referencia de 2026 y cómo leerlos.',
  body=f'''
<h2>Google Ads (anuncios de búsqueda)</h2>
<p>Según el informe 2026 de {L(S_WS26, 'WordStream by LocaliQ')}, con campañas de Estados Unidos:</p>
<div class="data-grid"><div><b>6,64 %</b><span>clics por impresión</span></div><div><b>5,42 $</b><span>coste medio por clic</span></div><div><b>8,18 %</b><span>de clics que se convierten</span></div><div><b>66,69 $</b><span>coste medio por contacto</span></div></div>
<p>Fuentes: {L(S_SEJ_CTR, 'clics y conversión')}, {L(S_SEJ_CPL, 'coste por contacto')}.</p>

<h2>Meta Ads (Facebook e Instagram)</h2>
<p>El mismo equipo analizó casi 1.800 campañas de Facebook en 2026 ({L(S_FB26, 'Search Engine Land')}):</p>
<div class="data-grid"><div><b>1,93 %</b><span>clics por impresión (campañas de tráfico)</span></div><div><b>0,60 $</b><span>coste por clic (tráfico)</span></div><div><b>8,54 %</b><span>conversión en campañas de captación</span></div><div><b>27,39 $</b><span>coste por contacto (captación)</span></div></div>

<h2>Cómo leer estos números</h2>
<ul>
<li><strong>Google cuesta más por clic, pero la persona ya está buscando.</strong> Si alguien escribe «dentista en Granada», tiene una necesidad ahora mismo.</li>
<li><strong>Meta es más barato y llega a más gente, pero hay que despertar el interés.</strong> Funciona muy bien con vídeo, ofertas claras y formularios dentro de la propia app.</li>
<li><strong>Son medias de Estados Unidos.</strong> En España y en ciudades como Granada los precios suelen ser distintos y cambian mucho según el sector y la competencia. Por eso lo primero es medir.</li>
<li><strong>Lo que importa es el coste por cliente, no por clic.</strong> Un clic barato que no llama no sirve de nada.</li>
</ul>
<h2>¿Cuál te conviene?</h2>
<p>Si vendes algo que la gente busca (un servicio urgente, una reserva, una cita), empieza por Google. Si tu producto entra por los ojos o quieres darte a conocer, Meta. Muchas veces lo mejor es combinar las dos.</p>
<p>Te ayudamos a decidirlo y a montarlo en <a href="publicidad-online.html">publicidad online</a>.</p>
''',
  faq=[('¿Cuánto cuesta un clic en Google Ads?', 'La media de 2026 en Estados Unidos es de 5,42 $ por clic según WordStream by LocaliQ, pero varía mucho por sector y país.'),
       ('¿Es más barato anunciarse en Facebook o en Google?', 'Por clic suele ser más barato Meta (0,60 $ de media en campañas de tráfico en 2026), pero en Google la persona ya está buscando lo que ofreces.')]),

 dict(slug='blog-publicar-menos-redes-sociales', date='2026-11-24', min=4, section='Redes sociales', word='Menos es más',
  title='Las marcas publican un 30 % menos en redes y consiguen más interacción: qué aprender',
  desc='El Observatorio de Marcas en Redes Sociales 2026 de IAB Spain muestra que las marcas publican menos y logran más interacción. Qué significa y cómo aplicarlo a un negocio pequeño.',
  keywords='cuántas veces publicar en redes sociales 2026',
  lead='Durante años, el consejo fue «publica todos los días». Los datos de 2026 dicen otra cosa: menos publicaciones, mejor pensadas, consiguen más.',
  body=f'''
<h2>Lo que dicen los datos</h2>
<p>El {L(S_OBS26, 'Observatorio de Marcas en Redes Sociales 2026 de IAB Spain')} analizó 196 marcas de 23 sectores. Tres cifras resumen el cambio:</p>
<div class="data-grid"><div><b>-30 %</b><span>publicaciones al año (de 1.722 a 1.208)</span></div><div><b>+29 %</b><span>interacción (del 0,91 % al 1,16 %)</span></div><div><b>-23 %</b><span>viralidad orgánica</span></div></div>
<p>Es decir: las marcas publican menos, cada publicación funciona mejor, pero es más difícil que algo se comparta solo.</p>

<h2>Por qué pasa</h2>
<ul>
<li><strong>Los algoritmos premian lo que retiene.</strong> Un vídeo que la gente ve hasta el final vale más que tres publicaciones que nadie mira.</li>
<li><strong>La gente busca antes de comprar.</strong> El 54 % de los usuarios consulta redes antes de comprar online ({L(S_IAB26, 'IAB Spain 2026')}), así que tu perfil funciona como un escaparate.</li>
<li><strong>Hay mucha más competencia por la atención.</strong> Por eso la viralidad «gratis» baja.</li>
</ul>

<h2>Cómo aplicarlo en un negocio pequeño</h2>
<ol>
<li><strong>Menos, pero con guion.</strong> Dos o tres vídeos cortos a la semana con un gancho en el primer segundo valen más que una foto diaria.</li>
<li><strong>Series que se repiten.</strong> «Pregunta del cliente de la semana», «un antes y un después»… La gente vuelve a por el siguiente capítulo.</li>
<li><strong>Contesta a todo.</strong> Los comentarios y los mensajes también cuentan como interacción, y son clientes.</li>
<li><strong>Empuja lo que funciona.</strong> Si un vídeo va bien solo, darle un pequeño presupuesto en anuncios lo lleva mucho más lejos.</li>
</ol>
<p>Si quieres un plan con guiones y vídeos pensados para crecer, mira nuestro <a href="redes-sociales.html#planes">plan de redes sociales</a>.</p>
''',
  faq=[('¿Cuántas veces hay que publicar en redes sociales?', 'No hay un número mágico. Los datos de 2026 muestran que las marcas que publican menos pero con mejor contenido consiguen más interacción.'),
       ('¿Por qué cada vez es más difícil hacerse viral?', 'Según IAB Spain, la viralidad orgánica de las marcas cayó un 23 % en un año por la competencia por la atención y los cambios de los algoritmos.')]),
]
