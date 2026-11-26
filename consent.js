/* Crecemia — banner de cookies + etiqueta de Google Ads (Consent Mode v2, modo básico) + Microsoft Clarity
   Ni la etiqueta de Google ni Clarity se cargan hasta que el visitante pulsa «Aceptar».
   Conversión «Contacto»: solo cuando el formulario de reserva o el de auditoría GEO se envían bien.
   Los botones de WhatsApp y de llamar no cuentan como conversión. */
(function(){
  var TAG_ID = 'GTM-N9B7QQNZ';
  var ADS_ID = 'AW-18571290832';
  var CONVERSION = 'AW-18571290832/AGOlCM7b97gdENDRvZdF';
  var CLARITY_ID = 'zjsuxe7f7p'; // Microsoft Clarity: mapas de calor y grabaciones
  var KEY = 'crecemia-cookies-v2'; // v2: se añadió Clarity, se vuelve a pedir el consentimiento
  var MAX_AGE = 365 * 24 * 3600 * 1000; // volvemos a preguntar a los 12 meses

  window.dataLayer = window.dataLayer || [];
  function gtag(){ window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag('consent', 'default', {
    ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    analytics_storage: 'denied', functionality_storage: 'granted', security_storage: 'granted'
  });

  function readChoice(){
    try{
      var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (v && (v.c === 'granted' || v.c === 'denied') && Date.now() - v.t < MAX_AGE) return v.c;
    }catch(e){}
    return null;
  }
  function saveChoice(c){ try{ localStorage.setItem(KEY, JSON.stringify({ c: c, t: Date.now() })); }catch(e){} }

  var loaded = false;
  function loadTag(){
    if (loaded) return; loaded = true;
    gtag('consent', 'update', { ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted', analytics_storage: 'granted' });
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ADS_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', TAG_ID);
    gtag('config', ADS_ID);
    loadClarity();
  }
  function loadClarity(){
    (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src='https://www.clarity.ms/tag/'+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window, document, 'clarity', 'script', CLARITY_ID);
    window.clarity('consentv2', { ad_Storage: 'granted', analytics_Storage: 'granted' });
  }
  function clearGoogleCookies(){
    document.cookie.split(';').forEach(function(c){
      var n = c.split('=')[0].trim();
      if (/^(_gcl|_ga|_gid|_gac|_clck|_clsk)/.test(n)){
        var host = location.hostname.replace(/^www\./, '');
        ['', '; domain=' + host, '; domain=.' + host].forEach(function(d){
          document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + d;
        });
      }
    });
  }

  // ---- Conversión «Contacto» (una vez por tipo y por página) ----
  var sent = {};
  function conversion(kind){
    if (!loaded || sent[kind] || typeof window.gtag !== 'function') return;
    sent[kind] = true;
    window.gtag('event', 'conversion', { send_to: CONVERSION, event_label: kind, transport_type: 'beacon' });
  }
  window.nexbiaConversion = conversion;

  function watchShown(id, kind){
    var el = document.getElementById(id);
    if (!el || !window.MutationObserver) return;
    new MutationObserver(function(){ if (!el.hidden) conversion(kind); })
      .observe(el, { attributes: true, attributeFilter: ['hidden'] });
  }

  // ---- Banner ----
  var css = '' +
    '.ck-bar{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;max-width:720px;margin:0 auto;background:#fff;color:#1d1b2e;' +
    'border-radius:16px;box-shadow:0 12px 40px rgba(40,25,90,.18);padding:18px 20px;font:15px/1.5 Inter,system-ui,sans-serif;display:flex;gap:16px;align-items:center;flex-wrap:wrap}' +
    '.ck-bar p{margin:0;flex:1 1 320px}.ck-bar a{color:#4B3AA6;font-weight:600}' +
    '.ck-btns{display:flex;gap:8px;flex:0 0 auto}' +
    '.ck-btns button{font:600 14px Inter,system-ui,sans-serif;padding:10px 18px;border-radius:999px;cursor:pointer;border:1.5px solid #4B3AA6;min-width:110px}' +
    '.ck-yes{background:#4B3AA6;color:#fff}.ck-no{background:#fff;color:#4B3AA6}' +
    '.ck-btns button:focus-visible{outline:3px solid #C6A9FF;outline-offset:2px}' +
    '.ck-bar[hidden]{display:none!important}' +
    '@media (max-width:640px){.ck-bar{left:10px;right:10px;bottom:84px;padding:16px}.ck-btns{width:100%}.ck-btns button{flex:1}}';

  var bar = null;
  function showBanner(){
    if (bar) { bar.hidden = false; return; }
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    bar = document.createElement('div');
    bar.className = 'ck-bar'; bar.setAttribute('role', 'dialog'); bar.setAttribute('aria-label', 'Cookies');
    bar.innerHTML = '<p>Usamos cookies de Google Ads y Microsoft Clarity para saber si nuestros anuncios funcionan y cómo se usa la web. Solo se activan si las aceptas. <a href="cookies.html">Más información</a></p>' +
      '<div class="ck-btns"><button type="button" class="ck-no">Rechazar</button><button type="button" class="ck-yes">Aceptar</button></div>';
    document.body.appendChild(bar);
    bar.querySelector('.ck-yes').addEventListener('click', function(){ saveChoice('granted'); bar.hidden = true; loadTag(); });
    bar.querySelector('.ck-no').addEventListener('click', function(){
      var wasOn = loaded;
      saveChoice('denied'); bar.hidden = true; clearGoogleCookies();
      if (wasOn){
        gtag('consent', 'update', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied' });
        if (typeof window.clarity === 'function') window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: 'denied' });
        location.reload();
      }
    });
  }
  window.nexbiaCookieSettings = showBanner;

  function init(){
    watchShown('bookOk', 'reserva');
    watchShown('geoOk', 'auditoria-geo');
    document.querySelectorAll('[data-cookie-settings]').forEach(function(el){
      el.addEventListener('click', function(e){ e.preventDefault(); showBanner(); });
    });
    var c = readChoice();
    if (c === 'granted') loadTag();
    else if (c === null) showBanner();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
