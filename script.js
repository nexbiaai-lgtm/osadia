// Always open a page at the top (unless a #section link was used)
(function(){
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch(e) {}
  function toTop(){
    var id = location.hash ? decodeURIComponent(location.hash.slice(1)) : '';
    if (id && document.getElementById(id)) return;
    window.scrollTo(0, 0);
    try { document.documentElement.scrollIntoView({ block: 'start' }); } catch(e) {}
  }
  toTop();
  window.addEventListener('pageshow', function(e){ if (e.persisted) toTop(); });
  window.addEventListener('load', function(){ setTimeout(toTop, 0); });
  // Clicking a link to another page: go to the top first (also scrolls the viewer that may contain the site)
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.target === '_blank' || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || /^(mailto:|tel:|https?:)/i.test(href)) return;
    if (href.indexOf('#') !== -1) return;
    window.scrollTo(0, 0);
    try { document.documentElement.scrollIntoView({ block: 'start' }); } catch(err) {}
  }, true);
})();

(function(){
  // Mobile nav toggle
  var toggle = document.querySelector('.menu-toggle');
  var links = document.querySelector('nav.links');
  if(toggle && links){
    toggle.setAttribute('aria-expanded', 'false');
    function setMenu(open){
      if (open){
        var hdr = document.querySelector('header.nav');
        if (hdr) document.documentElement.style.setProperty('--nav-h', Math.max(0, hdr.getBoundingClientRect().bottom) + 'px');
      }
      links.classList.toggle('open', open);
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
      var path = toggle.querySelector('path');
      if (path){
        if (!path.dataset.d) path.dataset.d = path.getAttribute('d');
        path.setAttribute('d', open ? 'M6 6l12 12M18 6L6 18' : path.dataset.d);
      }
    }
    toggle.addEventListener('click', function(){ setMenu(!links.classList.contains('open')); });
    links.addEventListener('click', function(e){ if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && links.classList.contains('open')){ setMenu(false); toggle.focus(); } });
    window.addEventListener('resize', function(){ if (window.innerWidth > 760 && links.classList.contains('open')) setMenu(false); });
    var dropTrigger = links.querySelector('.has-drop > span');
    if(dropTrigger){
      dropTrigger.addEventListener('click', function(){
        if(window.innerWidth <= 760){
          dropTrigger.parentElement.classList.toggle('open');
        }
      });
    }
  }

  // Intro loader cleanup — removes the overlay once its fade-out finishes
  var introLoader = document.getElementById('intro-loader');
  if(introLoader){
    setTimeout(function(){
      document.body.classList.remove('intro-active');
      if(introLoader.parentNode){ introLoader.parentNode.removeChild(introLoader); }
    }, 2100);
  }

  // Tabs demo
  var tabBtns = document.querySelectorAll('.tab-btn[data-tab]');
  var panels = document.querySelectorAll('.demo-panel');
  tabBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      tabBtns.forEach(function(b){ b.setAttribute('aria-selected','false'); });
      btn.setAttribute('aria-selected','true');
      var key = btn.getAttribute('data-tab');
      panels.forEach(function(p){ p.classList.toggle('active', p.getAttribute('data-panel') === key); });
    });
  });

  // FAQ accordion
  document.querySelectorAll('.faq-item').forEach(function(item){
    var q = item.querySelector('.faq-q');
    var a = item.querySelector('.faq-a');
    function sync(){
      var open = item.getAttribute('data-open') === 'true';
      a.style.maxHeight = open ? a.scrollHeight + 'px' : '0px';
    }
    sync();
    q.addEventListener('click', function(){
      var open = item.getAttribute('data-open') === 'true';
      item.setAttribute('data-open', open ? 'false' : 'true');
      sync();
    });
    window.addEventListener('resize', sync);
  });

  // Live restaurant chatbot demo
  var chatMsgs = document.getElementById('liveChatMessages');
  var chatForm = document.getElementById('liveChatForm');
  var chatInput = document.getElementById('liveChatInput');
  if(chatMsgs && chatForm && chatInput){
    function addBubble(text, who){
      var div = document.createElement('div');
      div.className = 'bubble ' + (who === 'bot' ? 'in' : 'out');
      div.textContent = text;
      chatMsgs.appendChild(div);
      chatMsgs.scrollTop = chatMsgs.scrollHeight;
    }
    function addTyping(){
      var div = document.createElement('div');
      div.className = 'bubble in typing-row';
      div.innerHTML = '<span class="typing-dots"><span></span><span></span><span></span></span>';
      chatMsgs.appendChild(div);
      chatMsgs.scrollTop = chatMsgs.scrollHeight;
      return div;
    }
    var WORD_NUMS = {un:1,uno:1,una:1,dos:2,tres:3,cuatro:4,cinco:5,seis:6,siete:7,ocho:8,nueve:9,diez:10};
    function extractPeople(t){
      var m = t.match(/(\d{1,2})\s*(personas?|comensales?|pax)/);
      if(m) return parseInt(m[1],10);
      m = t.match(/mesa\s*(?:para|de)\s*(\d{1,2})\b/);
      if(m) return parseInt(m[1],10);
      m = t.match(/\bsomos\s*(\d{1,2})\b/);
      if(m) return parseInt(m[1],10);
      m = t.match(/\bpara\s*(\d{1,2})\b(?!\s*(?:h\b|:))/);
      if(m && !/\bpara\s*las?\s*\d/.test(t)) return parseInt(m[1],10);
      for(var w in WORD_NUMS){
        if(new RegExp('\\b' + w + '\\s*(personas?|comensales?)\\b').test(t)) return WORD_NUMS[w];
      }
      return null;
    }
    function extractTime(t){
      var m = t.match(/(\d{1,2})[:.](\d{2})\s*h?/);
      if(m) return m[1] + ':' + m[2];
      m = t.match(/\blas?\s*(\d{1,2})\b/);
      if(m) return m[1] + ':00';
      m = t.match(/\b(\d{1,2})\s*h\b/);
      if(m) return m[1] + ':00';
      return null;
    }
    function dayOf(t){
      var m = t.match(/\b(hoy|esta noche|esta tarde|manana|pasado manana|lunes|martes|miercoles|jueves|viernes|sabado|domingo)\b/);
      if(!m) return null;
      var d = m[1];
      return ({'manana':'mañana','pasado manana':'pasado mañana','miercoles':'miércoles','sabado':'sábado'})[d] || d;
    }
    function norm(raw){
      return raw.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[¿?¡!.,;]/g,' ').replace(/\s+/g,' ').trim();
    }
    var res = { active:false, people:null, day:null, time:null, done:false, note:null };
    function resetRes(){ res = { active:false, people:null, day:null, time:null, done:false, note:null }; }
    function reservationStep(t){
      var p = extractPeople(t), d = dayOf(t), h = extractTime(t);
      if(p) res.people = p; if(d) res.day = d; if(h) res.time = h;
      if(res.time){ var hh = parseInt(res.time,10); if(hh >= 16 && hh < 20 || hh < 13 && hh > 0) {
        var bad = res.time; res.time = null;
        return 'A las ' + bad + ' tenemos la cocina cerrada 😕 Servimos comidas de 13:00 a 16:00 y cenas de 20:00 a 23:30. ¿A qué hora te viene bien dentro de ese horario?';
      } }
      if(res.day === 'lunes'){ res.day = null; return 'Los lunes cerramos por descanso. ¿Te viene bien otro día, de martes a domingo?'; }
      var missing = [];
      if(!res.people) missing.push('para cuántas personas');
      if(!res.day) missing.push('qué día');
      if(!res.time) missing.push('a qué hora');
      if(!missing.length){
        res.done = true; res.active = false;
        return 'Listo ✅ Mesa para ' + res.people + (res.people === 1 ? ' persona' : ' personas') + ', ' + res.day + ' a las ' + res.time + '. ¿Alguna alergia o algo que debamos saber? Si no, ¡os esperamos!';
      }
      res.active = true;
      var lead = res.people ? 'Genial, mesa para ' + res.people + (res.people === 1 ? ' persona' : ' personas') + '.' : 'Perfecto, te reservo encantado.';
      if(missing.length === 3) return 'Perfecto, te reservo encantado. Dime para cuántas personas, qué día y a qué hora.';
      return lead + ' Dime ' + missing.join(' y ') + '.';
    }
    var INTENTS = [
      [/(plato estrella|especialidad|que me recomiendas|que recomiendas|recomendacion|lo mejor|que esta bueno|que esta rico|plato tipico|que pido)/,
        'Nuestro plato estrella es el arroz negro con alioli de la casa 🥘 También triunfan el rabo de toro estofado y las berenjenas con miel de caña. ¿Te reservo mesa para probarlos?'],
      [/(postre|dulce|tarta)/, 'De postre, la tarta de queso al horno es la favorita, y también hacemos torrijas caseras. 🍰'],
      [/(vino|bebida|cerveza|carta de vinos|copa)/, 'Tenemos una carta de vinos con mucha bodega andaluza (Málaga, Granada y Jerez), cerveza de barril y refrescos. Vino por copa desde 3,50 €.'],
      [/(menu del dia|menu|carta|que teneis de comer|que hay de comer|platos)/, 'Entre semana tenemos menú del día por 15 € (primero, segundo, postre y bebida). Por las noches y los fines de semana, carta: arroces, carnes a la brasa, pescado del día y tapas para compartir.'],
      [/(precio|cuanto cuesta|cuanto vale|caro|barato|ticket medio|cuanto sale)/, 'El menú del día cuesta 15 €. A la carta, el ticket medio ronda los 25-30 € por persona con bebida.'],
      [/(vegano|vegetariano|sin carne)/, 'Sí, tenemos opciones vegetarianas y veganas: verduras a la brasa, arroz de verduras y varias tapas. Avísanos al reservar y el equipo te aconseja.'],
      [/(gluten|celiac|alerg|intoleran|lactosa|frutos secos|marisco)/, 'Tenemos la carta con los 14 alérgenos señalados y podemos adaptar muchos platos (sin gluten, sin lactosa…). Dinos qué alergia es y lo anotamos para que la cocina lo tenga en cuenta.'],
      [/(horario|hora abr|a que hora|abris|abierto|cerrais|cierra|abre)/, 'Abrimos de martes a domingo: comidas de 13:00 a 16:00 y cenas de 20:00 a 23:30. Los lunes cerramos por descanso.'],
      [/(donde|direccion|ubicacion|situais|como llego|como llegar|mapa)/, 'Estamos en pleno centro, a 2 minutos a pie de la plaza principal. Al confirmar la reserva te mando la ubicación exacta por WhatsApp.'],
      [/(aparcar|parking|aparcamiento|coche)/, 'Hay un parking público a 150 metros, y por la noche suele ser fácil aparcar en las calles de alrededor.'],
      [/(terraza|fuera|exterior|aire libre)/, 'Sí, tenemos terraza con 10 mesas, con calefactores en invierno. Si la quieres, dímelo al reservar.'],
      [/(nino|ninos|trona|carrito|bebe|menu infantil)/, 'Somos muy familiares: tenemos tronas, espacio para carritos y menú infantil por 9 €.'],
      [/(perro|mascota|animal)/, 'Las mascotas son bienvenidas en la terraza 🐶 Dentro del comedor no podemos aceptarlas.'],
      [/(silla de ruedas|accesib|movilidad reducida|escalon)/, 'El local es accesible: entrada sin escalones y baño adaptado.'],
      [/(grupo|evento|cumpleanos|celebracion|empresa|comida de navidad|cena de empresa|despedida)/, 'Hacemos grupos y celebraciones de hasta 40 personas, con menús cerrados desde 30 €. Dime la fecha y cuántos seréis y te paso las opciones.'],
      [/(para llevar|domicilio|delivery|recoger|glovo|just eat|uber)/, 'Sí, puedes pedir para llevar llamando al restaurante o por WhatsApp, y recogerlo en 20 minutos. A domicilio vamos con Glovo.'],
      [/(pagar|pago|tarjeta|bizum|efectivo)/, 'Aceptamos tarjeta, efectivo y Bizum.'],
      [/(cancelar|anular|cambiar la reserva|modificar)/, 'Sin problema. Dime el nombre y la hora de la reserva y la cambiamos o cancelamos. Te agradecemos que avises con unas horas de antelación.'],
      [/(wifi|enchufe)/, 'Sí, tenemos wifi gratis para clientes. La contraseña te la dan en la barra.'],
      [/(hablar con|persona|humano|encargado|telefono|llamar)/, 'Claro, te paso con el equipo: escríbenos por WhatsApp o llama al restaurante y te atiende una persona. Mientras tanto, si quieres, yo te dejo la reserva hecha.']
    ];
    var askAllergy = false;
    function botReply(raw){
      var t = norm(raw);
      if(!t) return '¿Me lo repites? No lo he pillado.';
      if(/^(no|nada|nada mas|eso es todo|no gracias|ninguna|no tengo)$/.test(t)){ var was = res.done; resetRes(); return was ? '¡Perfecto! Os esperamos 🙂 Si necesitas cambiar algo, escríbeme por aquí.' : 'Vale 🙂 ¿Te ayudo con algo más? Puedo reservarte mesa o resolver dudas de la carta.'; }
      if(/^(tengo (una )?alergia|soy alergico|soy alergica|alergias?)$/.test(t)){ askAllergy = true; return 'Gracias por avisar. ¿A qué eres alérgico/a? Lo anoto para que la cocina lo tenga en cuenta.'; }
      if(askAllergy){ askAllergy = false; return 'Anotado ✓ La cocina lo tendrá en cuenta y el camarero te indicará qué platos puedes tomar sin problema.'; }
      if(res.done && /(alerg|intoleran|gluten|celiac|lactosa|vegan|vegetarian|trona|carrito|terraza|silla de ruedas|cumple)/.test(t)){
        res.done = false; resetRes();
        return 'Anotado en tu reserva ✓ La cocina y la sala lo tendrán en cuenta. ¡Gracias por avisar!';
      }
      var wantsRes = /(reserv|mesa|apunt|hueco|sitio para)/.test(t);
      if(wantsRes || (res.active && (extractPeople(t) || dayOf(t) || extractTime(t))) || (dayOf(t) && extractPeople(t))){
        if(wantsRes && res.done) resetRes();
        return reservationStep(t);
      }
      for(var i = 0; i < INTENTS.length; i++){ if(INTENTS[i][0].test(t)) return INTENTS[i][1]; }
      if(/(gracias|genial|perfecto|vale|ok)/.test(t)) return '¡A ti! ¿Te ayudo con algo más?';
      if(/(adios|hasta luego|chao|nos vemos)/.test(t)) return '¡Hasta pronto! Que tengas un buen día 🙂';
      if(/^(hola|buenas|buenos dias|buenas tardes|buenas noches|hey|que tal)( .*)?$/.test(t) && t.split(' ').length <= 3) return '¡Hola! 😊 ¿Te reservo mesa o tienes alguna pregunta sobre la carta, el horario o cómo llegar?';
      return 'Esa no la sé responder con seguridad, y prefiero no inventármela 🙂 Te puedo ayudar con reservas, la carta y el plato estrella, horarios, alergias, grupos o cómo llegar. Si es otra cosa, te paso con el equipo por WhatsApp.';
    }
    chatForm.addEventListener('submit', function(e){
      e.preventDefault();
      var val = chatInput.value.trim();
      if(!val) return;
      addBubble(val, 'user');
      chatInput.value = '';
      var typingEl = addTyping();
      setTimeout(function(){
        typingEl.remove();
        addBubble(botReply(val), 'bot');
      }, 600 + Math.random()*500);
    });
    document.querySelectorAll('.chat-live-suggestions button').forEach(function(btn){
      btn.addEventListener('click', function(){
        chatInput.value = btn.textContent;
        chatForm.dispatchEvent(new Event('submit', {cancelable:true}));
      });
    });
  }

  // Mini interactive web demo — loads the real, working landing pages in an iframe
  var webdemoPicker = document.querySelector('.webdemo-picker');
  var webdemoIframe = document.querySelector('.webdemo-viewport iframe');
  var webdemoUrlEl = document.querySelector('.webdemo-chrome .url');
  var webdemoOpenFull = document.querySelector('.webdemo-chrome .webdemo-openfull');
  if(webdemoPicker && webdemoIframe){
    webdemoPicker.querySelectorAll('button').forEach(function(btn){
      btn.addEventListener('click', function(){
        webdemoPicker.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-selected','false'); });
        btn.setAttribute('aria-selected','true');
        var file = btn.getAttribute('data-file');
        var url = btn.getAttribute('data-url');
        webdemoIframe.src = file;
        if(webdemoUrlEl) webdemoUrlEl.textContent = url;
        if(webdemoOpenFull) webdemoOpenFull.setAttribute('href', file);
      });
    });
  }

  // Booking flow (contacto.html) — day/time picker that confirms via WhatsApp
  var bookingFlow = document.querySelector('.booking-flow');
  if(bookingFlow){
    var bookSteps = bookingFlow.querySelectorAll('.booking-step');
    var bookIndicators = bookingFlow.querySelectorAll('.booking-steps span');
    var servicioParam = null;
    try{
      servicioParam = (new URLSearchParams(window.location.search).get('servicio') || '').slice(0, 80) || null;
    }catch(e){}
    var bookState = { day: null, time: null, servicio: servicioParam };
    var bookContext = document.getElementById('bookContext');
    if(bookContext && servicioParam){
      bookContext.textContent = 'Pidiendo cita sobre: ' + servicioParam;
      bookContext.style.display = '';
    }
    function showBookStep(n){
      bookSteps.forEach(function(s){ s.style.display = (s.getAttribute('data-step') === String(n)) ? '' : 'none'; });
      bookIndicators.forEach(function(ind, i){ ind.classList.toggle('done', i < n); });
    }
    function escHTML(s){ return String(s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
    function updateBookSummary(){
      var summary = document.getElementById('bookSummary');
      if(!summary) return;
      if(bookState.day && bookState.time){
        var svcLine = bookState.servicio ? ' Sobre <b>' + escHTML(bookState.servicio) + '</b>.' : '';
        summary.innerHTML = 'Consultoría: <b>' + bookState.day + '</b> · franja <b>' + bookState.time + '</b>.' + svcLine + ' Déjanos tus datos para confirmarla.';
      }
    }
    function wireChipRow(rowId, stateKey, dataAttr, nextStep){
      var row = document.getElementById(rowId);
      if(!row) return;
      row.querySelectorAll('.chip').forEach(function(btn){
        btn.addEventListener('click', function(){
          row.querySelectorAll('.chip').forEach(function(b){ b.setAttribute('aria-pressed','false'); });
          btn.setAttribute('aria-pressed','true');
          bookState[stateKey] = btn.getAttribute(dataAttr);
          updateBookSummary();
          setTimeout(function(){ showBookStep(nextStep); }, 200);
        });
      });
    }
    wireChipRow('bookDayRow', 'day', 'data-day', 2);
    wireChipRow('bookTimeRow', 'time', 'data-time', 3);
    var bookConfirmBtn = document.getElementById('bookConfirmBtn');
    if(bookConfirmBtn){
      bookConfirmBtn.addEventListener('click', function(){
        var name = (document.getElementById('bookName') || {}).value || '';
        var company = (document.getElementById('bookCompany') || {}).value || '';
        var email = (document.getElementById('bookEmail') || {}).value || '';
        var contact = (document.getElementById('bookContact') || {}).value || '';
        var text = 'Hola, quiero reservar la consultoría gratuita de 15 minutos.';
        if(bookState.servicio) text += ' Me interesa: ' + bookState.servicio + '.';
        if(bookState.day) text += ' Día: ' + bookState.day + '.';
        if(bookState.time) text += ' Franja: ' + bookState.time + '.';
        if(name) text += ' Soy ' + name + (company ? ', de ' + company : '') + '.';
        if(contact) text += ' Teléfono: ' + contact + '.';
        if(email) text += ' Email: ' + email + '.';
        var site = (document.getElementById('bookWeb') || {}).value || '';
        if(site) text += ' Web: ' + site + '.';
        bookConfirmBtn.setAttribute('href', 'https://wa.me/34620762842?text=' + encodeURIComponent(text));
      });
    }
    showBookStep(1);
  }

  // ROI calculator
  var horas = document.getElementById('horas');
  var coste = document.getElementById('coste');
  if(horas && coste){
    var horasVal = document.getElementById('horasVal');
    var costeVal = document.getElementById('costeVal');
    var ahorroMes = document.getElementById('ahorroMes');
    var ahorroAnio = document.getElementById('ahorroAnio');
    var horasMes = document.getElementById('horasMes');
    function fmt(n){ return new Intl.NumberFormat('es-ES').format(Math.round(n)); }
    function recalc(){
      var h = parseFloat(horas.value);
      var c = parseFloat(coste.value);
      horasVal.textContent = h;
      costeVal.textContent = c;
      var hMes = h * 4.33;
      var eurMes = hMes * c;
      horasMes.textContent = fmt(hMes);
      ahorroMes.textContent = fmt(eurMes);
      ahorroAnio.textContent = fmt(eurMes * 12);
    }
    horas.addEventListener('input', recalc);
    coste.addEventListener('input', recalc);
    recalc();
  }

})();

// Neon timeline — the line lights up following the mouse (desktop) or the swipe (touch)
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  document.querySelectorAll('[data-ntl]').forEach(function(ntl){
    var rail = ntl.querySelector('.ntl-rail');
    var steps = [].slice.call(ntl.querySelectorAll('.ntl-step'));
    var n = steps.length, val = 0, target = 0, k = 0.16, raf = null, hovering = false;
    function clamp(p){ return Math.max(0, Math.min(1, p)); }
    function render(p){
      ntl.style.setProperty('--p', p.toFixed(4));
      ntl.style.setProperty('--head', (p > 0.01 && p < 0.995) ? 1 : 0);
      steps.forEach(function(s, i){ s.classList.toggle('lit', p >= i / (n - 1) - 0.002); });
    }
    function tick(){
      val += (target - val) * k;
      if (Math.abs(target - val) < 0.0015) val = target;
      render(val);
      raf = (val !== target) ? requestAnimationFrame(tick) : null;
    }
    function go(t, speed){
      target = clamp(t); k = reduce ? 1 : (speed || 0.16);
      if (!raf) raf = requestAnimationFrame(tick);
    }
    function railFrac(x){ var r = rail.getBoundingClientRect(); return (x - r.left) / r.width; }
    function visibleFrac(){ var v = ntl.getBoundingClientRect(); return railFrac(v.right - 30); }
    if (fine){
      ntl.addEventListener('pointerenter', function(){ hovering = true; });
      ntl.addEventListener('pointermove', function(e){ hovering = true; go(railFrac(e.clientX), 0.18); });
      ntl.addEventListener('pointerleave', function(){ hovering = false; go(0, 0.05); });
    } else {
      ntl.addEventListener('scroll', function(){ go(visibleFrac(), 0.2); }, { passive: true });
      steps.forEach(function(s, i){ s.addEventListener('click', function(){ go(Math.max(i / (n - 1), visibleFrac()), 0.12); }); });
    }
    if ('IntersectionObserver' in window){
      var io = new IntersectionObserver(function(entries){
        entries.forEach(function(e){
          if (!e.isIntersecting) return;
          io.disconnect();
          if (fine){
            go(1, 0.035);
            setTimeout(function(){ if (!hovering) go(0, 0.05); }, 2600);
          } else {
            go(visibleFrac(), 0.05);
          }
        });
      }, { threshold: 0.6 });
      io.observe(ntl);
    }
  });
})();

// SEO search example — types the query, then the business climbs to position 1
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-serp]').forEach(function(serp){
    var list = serp.querySelector('[data-serp-list]');
    var win = serp.querySelector('[data-serp-win]');
    var q = serp.querySelector('[data-serp-query]');
    var text = q.getAttribute('data-text') || q.textContent;
    serp.classList.add('js');
    if (reduce || !('IntersectionObserver' in window)){ serp.classList.add('done'); return; }
    // start: query empty, our business further down the results
    q.textContent = '';
    var third = list.children[3];
    list.insertBefore(win, third || null);
    function climb(){
      var items = [].slice.call(list.children);
      var before = items.map(function(el){ return el.getBoundingClientRect().top; });
      list.insertBefore(win, list.firstChild);
      items.forEach(function(el, i){
        var dy = before[i] - el.getBoundingClientRect().top;
        if (!dy) return;
        el.style.transition = 'none';
        el.style.transform = 'translateY(' + dy + 'px)';
      });
      list.offsetHeight; // force reflow
      items.forEach(function(el){
        el.style.transition = 'transform .9s cubic-bezier(.22,1,.36,1), opacity .5s ease';
        el.style.transform = '';
      });
      setTimeout(function(){ serp.classList.add('done'); }, 650);
    }
    function type(i){
      q.textContent = text.slice(0, i);
      if (i < text.length){ setTimeout(function(){ type(i + 1); }, 55 + Math.random() * 45); }
      else { setTimeout(function(){ serp.classList.remove('typing'); climb(); }, 650); }
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        io.disconnect();
        serp.classList.add('typing');
        setTimeout(function(){ type(1); }, 400);
      });
    }, { threshold: 0.45 });
    io.observe(serp);
  });
})();

// Automation flow examples — tabs
document.querySelectorAll('[data-flows]').forEach(function(box){
  var tabs = [].slice.call(box.querySelectorAll('[data-flow-tab]'));
  function show(key, focus){
    tabs.forEach(function(t){
      var on = t.getAttribute('data-flow-tab') === key;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    box.querySelectorAll('[data-flow-panel]').forEach(function(p){ p.hidden = p.getAttribute('data-flow-panel') !== key; });
  }
  tabs.forEach(function(t, i){
    t.tabIndex = t.getAttribute('aria-selected') === 'true' ? 0 : -1;
    t.addEventListener('click', function(){ show(t.getAttribute('data-flow-tab')); });
    t.addEventListener('keydown', function(e){
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var j = (i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length;
      show(tabs[j].getAttribute('data-flow-tab'), true);
    });
  });
});

// Digitalización — interactive growth sequence
(function(){
  var root = document.querySelector('[data-growth]');
  if (!root) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var PRESETS = {
    clinica:      { daily: 20, pct: 20, value: 120 },
    restaurante:  { daily: 40, pct: 25, value: 40 },
    inmobiliaria: { daily: 10, pct: 30, value: 600 },
    otro:         { daily: 15, pct: 20, value: 80 }
  };
  var SETUP = 199, MONTHLY = 298, RAMP = [0.5, 0.75, 1, 1, 1, 1];
  var inputs = {};
  root.querySelectorAll('[data-in]').forEach(function(el){ inputs[el.getAttribute('data-in')] = el; });
  var fmt = { format: function(n){ return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); } };
  function money(n){ return fmt.format(Math.round(n)) + ' €'; }
  var FORMAT = {
    lost: function(n){ return fmt.format(n); },
    lostEur: money,
    recovered: function(n){ return fmt.format(n); },
    hours: function(n){ return '+' + fmt.format(n) + ' h'; },
    newClients: function(n){ return '+' + fmt.format(n); },
    extra: function(n){ return '+' + money(n); },
    cum6: function(n){ return '+' + money(n); },
    roi: function(n){ return (Math.round(n * 10) / 10).toLocaleString('es-ES') + '×'; }
  };
  var current = {};
  function animateTo(key, target){
    var els = root.querySelectorAll('[data-out="' + key + '"]');
    var from = current[key] || 0; current[key] = target;
    if (reduce || from === target){ els.forEach(function(e){ e.textContent = FORMAT[key](target); }); return; }
    var t0 = null, dur = 550;
    function step(ts){
      if (!t0) t0 = ts;
      var k = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      var v = from + (target - from) * e;
      var shown = key === 'roi' ? v : Math.round(v);
      els.forEach(function(el){ el.textContent = FORMAT[key](shown); });
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  // chart skeleton
  var bars = root.querySelector('.gs-bars');
  for (var m = 1; m <= 6; m++){
    var d = document.createElement('div'); d.className = 'gs-m';
    d.innerHTML = '<i class="g"></i><i class="c"></i><span>Mes ' + m + '</span>';
    bars.appendChild(d);
  }
  function compute(){
    var daily = +inputs.daily.value, pct = +inputs.pct.value / 100, value = +inputs.value.value;
    root.querySelector('[data-show="daily"]').textContent = daily;
    root.querySelector('[data-show="pct"]').textContent = Math.round(pct * 100) + ' %';
    root.querySelector('[data-show="value"]').textContent = money(value);
    var lost = Math.round(daily * 30 * pct);
    var recovered = Math.round(lost * 0.8);
    var newClients = Math.round(recovered * 0.2);
    var extra = newClients * value;
    var hours = Math.round(daily * 30 * 3 / 60 * 0.7);
    var gains = [], costs = [], cg = 0;
    RAMP.forEach(function(r, i){ cg += extra * r; gains.push(cg); costs.push(SETUP + MONTHLY * (i + 1)); });
    var cum6 = gains[5], roi = cum6 / costs[5];
    animateTo('lost', lost); animateTo('lostEur', Math.round(lost * 0.2) * value);
    animateTo('recovered', recovered); animateTo('hours', hours);
    animateTo('newClients', newClients); animateTo('extra', extra);
    animateTo('cum6', cum6); animateTo('roi', roi);
    var max = Math.max(gains[5], costs[5]) || 1;
    bars.querySelectorAll('.gs-m').forEach(function(el, i){
      el.querySelector('.g').style.setProperty('--h', (gains[i] / max * 100).toFixed(1) + '%');
      el.querySelector('.c').style.setProperty('--h', (costs[i] / max * 100).toFixed(1) + '%');
    });
  }
  root.querySelectorAll('[data-preset]').forEach(function(chip){
    chip.addEventListener('click', function(){
      var p = PRESETS[chip.getAttribute('data-preset')];
      root.querySelectorAll('[data-preset]').forEach(function(c){ c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      inputs.daily.value = p.daily; inputs.pct.value = p.pct; inputs.value.value = p.value;
      compute();
    });
  });
  Object.keys(inputs).forEach(function(k){ inputs[k].addEventListener('input', compute); });
  compute();

  // top-to-bottom reveal + glowing line
  var steps = [].slice.call(root.querySelectorAll('[data-gs-step]'));
  var flow = root.querySelector('.gs-flow'), line = root.querySelector('.gs-line');
  var chart = root.querySelector('[data-gs-chart]');
  if (reduce || !('IntersectionObserver' in window)){
    steps.forEach(function(s){ s.classList.add('in', 'lit'); });
    chart.classList.add('grown'); line.style.setProperty('--gp', 1);
    return;
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.25 });
  steps.forEach(function(s){ io.observe(s); });
  var cio = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if (e.isIntersecting){ chart.classList.add('grown'); cio.disconnect(); } });
  }, { threshold: 0.4 });
  cio.observe(chart);
  function onScroll(){
    var mark = window.innerHeight * 0.6;
    var r = line.getBoundingClientRect();
    var p = Math.max(0, Math.min(1, (mark - r.top) / r.height));
    line.style.setProperty('--gp', p.toFixed(4));
    steps.forEach(function(s){
      var d = s.querySelector('.gs-dot').getBoundingClientRect();
      s.classList.toggle('lit', d.top + d.height / 2 < mark);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();

// Home — neon line runs down the benefits and then draws a ring around the booking box
(function(){
  var wrap = document.querySelector('[data-o1journey]');
  if (!wrap) return;
  var line = wrap.querySelector('.o1-line');
  var box = wrap.querySelector('[data-o1box]');
  var steps = [].slice.call(wrap.querySelectorAll('[data-o1]'));
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function layout(){
    var w = wrap.getBoundingClientRect(), b = box.getBoundingClientRect();
    line.style.setProperty('--o1h', Math.max(0, b.top - w.top - 28) + 'px');
    // ring starts at the top centre (where the line lands) and closes at the bottom centre
    var W = b.width, H = b.height, r = Math.min(28, H / 2), m = W / 2;
    var svg = box.querySelector('.o1-ring');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    box.querySelector('.o1-ring-r').setAttribute('d', 'M' + m + ',0 H' + (W - r) + ' A' + r + ',' + r + ' 0 0 1 ' + W + ',' + r + ' V' + (H - r) + ' A' + r + ',' + r + ' 0 0 1 ' + (W - r) + ',' + H + ' H' + m);
    box.querySelector('.o1-ring-l').setAttribute('d', 'M' + m + ',0 H' + r + ' A' + r + ',' + r + ' 0 0 0 0,' + r + ' V' + (H - r) + ' A' + r + ',' + r + ' 0 0 0 ' + r + ',' + H + ' H' + m);
  }
  function onScroll(){
    var mark = window.innerHeight * 0.62;
    var lr = line.getBoundingClientRect();
    var p = reduce ? 1 : Math.max(0, Math.min(1, (mark - lr.top) / lr.height));
    line.style.setProperty('--o1p', p.toFixed(4));
    line.style.setProperty('--o1spark', p > 0.01 && p < 0.999 ? 1 : 0);
    steps.forEach(function(s){ s.classList.toggle('in', reduce || s.getBoundingClientRect().top < mark); });
    var br = box.getBoundingClientRect();
    var q = p < 1 ? 0 : Math.max(0, Math.min(1, (mark - br.top) / (br.height * 0.7)));
    if (reduce) q = 1;
    box.style.setProperty('--o1q', q.toFixed(4));
    box.classList.toggle('lit', q >= 0.999);
  }
  layout(); onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function(){ layout(); onScroll(); });
  window.addEventListener('load', function(){ layout(); onScroll(); });
})();

// ---------------------------------------------------------------------------
// Form → Google Sheets + aviso por email (Google Apps Script)
// Pega aquí la URL de la aplicación web de Apps Script (termina en /exec).
// Mientras esté vacía, la reserva se confirma por WhatsApp como hasta ahora.
var NEXBIA_FORM_URL = 'https://script.google.com/macros/s/AKfycbwBwdnmp4AiEegJpMe1Bm5X-_4w2oKefZ5P_nXAc6L6V8eXDIES44zWcyA5Tt35Fbkx/exec';
// ---------------------------------------------------------------------------
(function(){
  var btn = document.getElementById('bookSendBtn');
  if (!btn) return;
  var flow = btn.closest('.booking-flow');
  function chosen(rowId){ var c = document.querySelector('#' + rowId + ' .chip[aria-pressed="true"]'); return c ? (c.getAttribute('data-day') || c.getAttribute('data-time')) : ''; }
  btn.addEventListener('click', function(){
    var name = (document.getElementById('bookName').value || '').trim();
    var contact = (document.getElementById('bookContact').value || '').trim();
    var company = ((document.getElementById('bookCompany') || {}).value || '').trim();
    var email = ((document.getElementById('bookEmail') || {}).value || '').trim();
    var sitio = ((document.getElementById('bookWeb') || {}).value || '').trim();
    var hp = (document.getElementById('bookHp') || {}).value || '';
    var err = document.getElementById('bookError'), ok = document.getElementById('bookOk');
    var emailOk = !email || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!name || !company || (!contact && !email) || !emailOk){
      err.textContent = !emailOk ? 'Revisa el email, parece que falta algo.' : 'Pon tu nombre, tu empresa y un teléfono o email para poder llamarte.';
      err.hidden = false; return;
    }
    err.hidden = true;
    var servicio = '';
    try { servicio = (new URLSearchParams(location.search).get('servicio') || '').slice(0, 80); } catch(e) {}
    var data = { tipo: 'Reserva de llamada', nombre: name, empresa: company, contacto: contact, email: email, sitio: sitio, dia: chosen('bookDayRow'), franja: chosen('bookTimeRow'), servicio: servicio, pagina: location.pathname.split('/').pop() || 'index.html', url_trap: hp };
    if (!NEXBIA_FORM_URL){
      // Fallback: open WhatsApp with the booking already written
      var wa = document.getElementById('bookConfirmBtn');
      wa.click();
      return;
    }
    btn.disabled = true; btn.textContent = 'Enviando…';
    function done(){
      ok.hidden = false;
      document.getElementById('bookOkText').textContent = 'Te llamamos ' + (data.dia ? data.dia.toLowerCase() : 'pronto') + (data.franja ? ', ' + data.franja.toLowerCase() : '') + '. Gracias, ' + name.split(/[ ,]/)[0] + '.';
      btn.textContent = 'Reserva enviada ✓';
    }
    function fail(){
      btn.disabled = false; btn.textContent = 'Reservar mi llamada gratis →';
      var wa = document.getElementById('bookConfirmBtn');
      try { wa.dispatchEvent(new Event('click', {cancelable:true})); } catch(e) {}
      err.textContent = 'No se ha podido enviar desde aquí. ';
      var waLink = document.createElement('a');
      waLink.href = wa.href; waLink.target = '_blank'; waLink.rel = 'noopener';
      var waB = document.createElement('b'); waB.textContent = 'Envíanos la reserva por WhatsApp →';
      waLink.appendChild(waB); err.appendChild(waLink);
      err.hidden = false;
    }
    // Plan B: envío con un formulario oculto (funciona aunque el navegador bloquee fetch)
    function viaForm(){
      var blocked = false;
      function onViolation(ev){ if (String(ev.blockedURI || '').indexOf('script.google') > -1 || ev.violatedDirective === 'form-action') blocked = true; }
      document.addEventListener('securitypolicyviolation', onViolation);
      var name_ = 'nxb_' + Date.now();
      var ifr = document.createElement('iframe'); ifr.name = name_; ifr.style.display = 'none'; ifr.setAttribute('aria-hidden', 'true');
      document.body.appendChild(ifr);
      var f = document.createElement('form'); f.method = 'POST'; f.action = NEXBIA_FORM_URL; f.target = name_; f.style.display = 'none';
      Object.keys(data).forEach(function(k){ var i = document.createElement('input'); i.type = 'hidden'; i.name = k; i.value = data[k]; f.appendChild(i); });
      document.body.appendChild(f);
      try { f.submit(); } catch(e) { blocked = true; }
      setTimeout(function(){
        document.removeEventListener('securitypolicyviolation', onViolation);
        f.remove(); setTimeout(function(){ ifr.remove(); }, 5000);
        blocked ? fail() : done();
      }, 1500);
    }
    fetch(NEXBIA_FORM_URL, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(data) })
      .then(done)
      .catch(viaForm);
  });
})();

// ---------------------------------------------------------------------------
// Capa premium — mejoras de interacción (no sustituyen a la lógica anterior)
// ---------------------------------------------------------------------------
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Cabecera: sombra suave al hacer scroll
  var header = document.querySelector('header.nav');
  if (header){
    var onScroll = function(){ header.classList.toggle('is-scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Menú móvil: estado accesible, bloqueo de scroll, cierre al elegir enlace o con Escape
  var toggle = document.querySelector('.menu-toggle');
  var links = document.querySelector('nav.links');
  if (toggle && links){
    toggle.setAttribute('aria-expanded', 'false');
    var sync = function(){
      var open = links.classList.contains('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
      var path = toggle.querySelector('path');
      if (path){
        if (!path.dataset.d) path.dataset.d = path.getAttribute('d');
        path.setAttribute('d', open ? 'M6 6l12 12M18 6L6 18' : path.dataset.d);
      }
      document.body.classList.toggle('menu-open', open);
    };
    toggle.addEventListener('click', function(){ setTimeout(sync, 0); });
    links.addEventListener('click', function(e){
      if (e.target.closest('a') && links.classList.contains('open')){ links.classList.remove('open'); sync(); }
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && links.classList.contains('open')){ links.classList.remove('open'); sync(); toggle.focus(); }
    });
    window.addEventListener('resize', function(){ if (window.innerWidth > 760 && links.classList.contains('open')){ links.classList.remove('open'); sync(); } });
  }

  // FAQ: estado accesible para lectores de pantalla
  document.querySelectorAll('.faq-item').forEach(function(item){
    var q = item.querySelector('.faq-q');
    if (!q) return;
    var set = function(){ q.setAttribute('aria-expanded', item.getAttribute('data-open') === 'true' ? 'true' : 'false'); };
    set();
    q.addEventListener('click', function(){ setTimeout(set, 0); });
  });

  // Aparición suave de bloques al entrar en pantalla
  if (reduce || !('IntersectionObserver' in window)) return;
  var sel = '.section-head, .benefit-card, .usecase-card, .value-card, .trust-card, .faq-item, .case-card, .team-card, .contact-card, .final-cta, .plan:not(.hero-plan):not(.pcard), .check-item, .ab-card, .integ-row, .chat-live, .calc-box, .voice-card, .webdemo, .booking-flow, .legal-body, .plan-category .cat-head, .serp, .aichat, .flows, .demo-panel, .tabs, .map-embed';
  var vh = window.innerHeight || 800;
  var items = [];
  document.querySelectorAll(sel).forEach(function(el){
    if (el.closest('.o1-wrap, #intro-loader, .price-show')) return;
    if (el.getBoundingClientRect().top < vh * 0.9) return; // lo que ya se ve, se queda tal cual
    var i = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
    el.style.setProperty('--rv-d', (Math.min(i, 5) * 70) + 'ms');
    el.classList.add('rv');
    items.push(el);
  });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('rv-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
  items.forEach(function(el){ io.observe(el); });
  // red de seguridad: si algo no llegara a observarse, se muestra igualmente
  window.addEventListener('beforeprint', function(){ items.forEach(function(el){ el.classList.add('rv-in'); }); });
})();

// GEO chat example: types the question, the AI "thinks" and recommends the business first
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-aichat]').forEach(function(chat){
    var user = chat.querySelector('[data-aichat-user]');
    var typed = chat.querySelector('[data-aichat-typed]');
    var items = [].slice.call(chat.querySelectorAll('.aichat-list li'));
    var text = user.textContent;
    chat.classList.add('js');
    function finish(){ chat.classList.add('sent','answered','done'); items.forEach(function(li){ li.classList.add('in'); }); }
    if (reduce || !('IntersectionObserver' in window)){ finish(); return; }
    function answer(){
      chat.classList.remove('thinking'); chat.classList.add('answered');
      items.forEach(function(li, i){ setTimeout(function(){ li.classList.add('in'); }, 250 + i * 380); });
      setTimeout(function(){ chat.classList.add('done'); }, 250 + items.length * 380 + 500);
    }
    function send(){
      chat.classList.remove('typing','has-text'); typed.textContent = '';
      chat.classList.add('sent');
      setTimeout(function(){ chat.classList.add('thinking'); }, 300);
      setTimeout(answer, 1700);
    }
    function type(i){
      typed.textContent = text.slice(0, i);
      chat.classList.toggle('has-text', i > 0);
      if (i < text.length){ setTimeout(function(){ type(i + 1); }, 35 + Math.random() * 35); }
      else { setTimeout(send, 550); }
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        io.disconnect();
        chat.classList.add('typing');
        setTimeout(function(){ type(1); }, 400);
      });
    }, { threshold: 0.45 });
    io.observe(chat);
  });
})();

// Google Maps: solo se carga si el usuario lo pide (sin cookies de terceros antes)
(function(){
  document.querySelectorAll('[data-map-load]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var box = btn.closest('.map-consent');
      var f = document.createElement('iframe');
      f.src = box.getAttribute('data-map-src');
      f.loading = 'lazy'; f.title = 'Mapa'; f.referrerPolicy = 'no-referrer-when-downgrade';
      box.replaceWith(f);
    });
  });
})();

// Inicio: formulario «¿Te recomienda ChatGPT?» (auditoría GEO gratis) → misma hoja de Reservas
(function(){
  var form = document.getElementById('geoForm');
  if (!form || typeof NEXBIA_FORM_URL === 'undefined') return;
  var btn = document.getElementById('geoSend'), err = document.getElementById('geoError'), ok = document.getElementById('geoOk');
  function v(id){ return ((document.getElementById(id) || {}).value || '').trim(); }
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var name = v('geoName'), biz = v('geoBiz'), city = v('geoCity'), contact = v('geoContact');
    if (!name || !biz || !city || !contact){ err.textContent = 'Rellena los cuatro campos para poder enviarte el resultado.'; err.hidden = false; return; }
    var isEmail = contact.indexOf('@') > -1;
    if (isEmail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact)){ err.textContent = 'Revisa el email, parece que falta algo.'; err.hidden = false; return; }
    if (!isEmail && contact.replace(/\D/g,'').length < 9){ err.textContent = 'Revisa el teléfono: tiene que tener al menos 9 cifras.'; err.hidden = false; return; }
    err.hidden = true;
    var data = { tipo: 'Auditoría GEO gratis', nombre: name, empresa: biz, contacto: isEmail ? '' : contact, email: isEmail ? contact : '', sitio: '', dia: '', franja: '', servicio: 'Auditoría GEO · ' + city, pagina: location.pathname.split('/').pop() || 'index.html', url_trap: v('geoHp') };
    btn.disabled = true; btn.textContent = 'Enviando…';
    function done(){ ok.hidden = false; btn.textContent = 'Solicitud enviada ✓'; form.querySelectorAll('input').forEach(function(i){ i.disabled = true; }); }
    function fail(){
      btn.disabled = false; btn.textContent = 'Comprobar mi negocio gratis';
      var msg = 'Hola, quiero la auditoría GEO gratis. Soy ' + name + ', de ' + biz + ' (' + city + ').';
      err.textContent = 'No se ha podido enviar desde aquí. ';
      var a = document.createElement('a'); a.href = 'https://wa.me/34620762842?text=' + encodeURIComponent(msg); a.target = '_blank'; a.rel = 'noopener';
      var b = document.createElement('b'); b.textContent = 'Pídela por WhatsApp →'; a.appendChild(b); err.appendChild(a); err.hidden = false;
    }
    fetch(NEXBIA_FORM_URL, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(data) }).then(done).catch(fail);
  });
})();

// Recorrido del inicio: calculadora de horas → euros y botones que marcan el servicio en la reserva
(function(){
  var rate = document.getElementById('o1Rate'), out = document.getElementById('o1Month');
  if (rate && out){
    var upd = function(){ var v = Math.max(0, Math.min(500, parseFloat(rate.value) || 0)); out.textContent = String(Math.round(v * 18 * 4)).replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ' €'; };
    rate.addEventListener('input', upd); upd();
  }
  document.querySelectorAll('.o1-want[data-servicio]').forEach(function(a){
    a.addEventListener('click', function(){
      var svc = a.getAttribute('data-servicio');
      try { history.replaceState(null, '', '?servicio=' + encodeURIComponent(svc) + '#consultoria'); } catch(e) {}
      var ctx = document.getElementById('bookContext');
      if (ctx){ ctx.textContent = 'Revisión gratis sobre: ' + svc; ctx.style.display = ''; }
    });
  });
})();

/* Vídeo hero: CTA al final de cada vuelta */
(function(){
  var box=document.querySelector('[data-hv]'); if(!box) return;
  var v=box.querySelector('video'), btn=box.querySelector('.hv-cta .btn');
  if(window.matchMedia && window.matchMedia('(max-width: 640px)').matches){ v.setAttribute('poster','video/hero-s-poster.jpg'); }
  function set(on){ box.classList.toggle('show',on); if(btn) btn.tabIndex=on?0:-1; }
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    v.removeAttribute('autoplay'); try{v.pause();}catch(e){} set(true); return;
  }
  v.addEventListener('timeupdate',function(){ set(v.currentTime>=12.9); });
})();

/* Menú Servicios desplegable: clic/teclado y cierre con Escape o clic fuera */
(function(){
  var drops = document.querySelectorAll('.has-drop');
  drops.forEach(function(d){
    var btn = d.querySelector('.drop-btn');
    if (!btn) return;
    btn.addEventListener('click', function(){
      var open = !d.classList.contains('open');
      d.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    d.addEventListener('keydown', function(e){
      if (e.key === 'Escape'){ d.classList.remove('open'); btn.setAttribute('aria-expanded','false'); btn.focus(); }
    });
  });
  document.addEventListener('click', function(e){
    drops.forEach(function(d){
      if (!d.contains(e.target)){ d.classList.remove('open'); var b = d.querySelector('.drop-btn'); if (b) b.setAttribute('aria-expanded','false'); }
    });
  });
})();

/* ===== Formulario rápido (portada + ventana desde cualquier "Consultoría gratis") ===== */
(function(){
  if (typeof NEXBIA_FORM_URL === 'undefined') return;
  var IC = {
    tel: '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/>',
    pin: '<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
    heart: '<path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.7 4.5c2.1 0 3.6 1.2 4.3 2.4.7-1.2 2.2-2.4 4.3-2.4 3.7 0 5.8 3.9 4.3 7.3C19.5 16.4 12 21 12 21z"/>',
    ads: '<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1zm13.5 1A4.5 4.5 0 0 0 14 8v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/>',
    web: '<path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-6v2h3v2H7v-2h3v-2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm0 2v10h16V6z"/>',
    doc: '<path d="M6 2h8l6 6v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm7 1.5V9h5.5zM8 13h8v2H8zm0 4h8v2H8z"/>'
  };
  var TEMAS = [
    ['Atender llamadas y WhatsApp', 'Que nadie se quede sin respuesta', 'tel'],
    ['Más clientes desde Google', 'Salir en Google y en Maps', 'pin'],
    ['Redes sociales', 'Publicar sin pensar en ello', 'heart'],
    ['Anuncios en Google y Meta', 'Anuncios que traen contactos', 'ads'],
    ['Una web nueva', 'Que te pidan cita sola', 'web'],
    ['Quitarme papeleo', 'Facturas, citas y avisos solos', 'doc']
  ];
  var n = 0;
  function svg(k){ return '<svg viewBox="0 0 24 24" aria-hidden="true">' + IC[k] + '</svg>'; }
  function html(){
    n++; var p = 'qf' + n;
    return '<form class="qf" novalidate>' +
      '<div class="qf-top"><span class="qf-badge">Gratis · 15 minutos</span><span class="qf-steps"><b class="qf-s1">1</b><i></i><b class="qf-s2">2</b></span></div>' +
      '<p class="qf-q" id="' + p + 'q">¿Qué quieres mejorar primero?</p>' +
      '<p class="qf-hint">Elige una opción y te llamamos con ideas para tu negocio.</p>' +
      '<div class="qf-chips" role="group" aria-labelledby="' + p + 'q">' +
        TEMAS.map(function(t){ return '<button type="button" class="qf-chip" aria-pressed="false" data-t="' + t[0] + '"><span class="qf-ic">' + svg(t[2]) + '</span><span class="qf-tx"><b>' + t[0] + '</b><small>' + t[1] + '</small></span><span class="qf-ck" aria-hidden="true"></span></button>'; }).join('') +
      '</div>' +
      '<div class="qf-fields">' +
        '<p class="qf-q2">¿A quién llamamos?</p>' +
        '<label class="qf-l" for="' + p + 'n">Tu nombre</label><input class="qf-in" id="' + p + 'n" name="nombre" autocomplete="name" placeholder="Tu nombre">' +
        '<label class="qf-l" for="' + p + 't">Teléfono o WhatsApp</label><input class="qf-in" id="' + p + 't" name="contacto" type="tel" inputmode="tel" autocomplete="tel" placeholder="Teléfono o WhatsApp">' +
        '<input class="hp-field" name="url_trap" tabindex="-1" autocomplete="off" aria-hidden="true">' +
        '<button type="submit" class="btn btn-lg qf-send">Quiero que me llaméis gratis <span aria-hidden="true">→</span></button>' +
      '</div>' +
      '<ul class="qf-trust"><li>Sin compromiso</li><li>Respuesta en el día</li><li><span class="qf-stars">★★★★★</span> 5,0 en Google</li></ul>' +
      '<p class="qf-err" role="alert" hidden></p>' +
      '<p class="qf-ok" role="status" hidden><b>¡Recibido!</b> Te llamamos en horario de 10:00 a 19:00, de lunes a viernes. Son 15 minutos y sin compromiso.</p>' +
      '<p class="qf-legal">Responsable: Daniel Mata Jiménez (Crecemia). Usamos tu teléfono solo para llamarte. <a href="privacidad.html">Privacidad</a></p>' +
    '</form>';
  }
  function wire(form){
    var tema = '';
    form.querySelectorAll('.qf-chip').forEach(function(c){
      c.addEventListener('click', function(){
        form.querySelectorAll('.qf-chip').forEach(function(o){ o.setAttribute('aria-pressed', 'false'); });
        c.setAttribute('aria-pressed', 'true'); tema = c.getAttribute('data-t');
        form.classList.add('qf-open');
        var nm = form.querySelector('[name=nombre]'); if (nm && !nm.value) nm.focus();
      });
    });
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var err = form.querySelector('.qf-err'), ok = form.querySelector('.qf-ok'), btn = form.querySelector('.qf-send');
      var nombre = form.querySelector('[name=nombre]').value.trim();
      var tel = form.querySelector('[name=contacto]').value.trim();
      if (!nombre || tel.replace(/\D/g, '').length < 9){
        err.textContent = !nombre ? 'Dinos tu nombre para saber por quién preguntar.' : 'Revisa el teléfono: tiene que tener al menos 9 cifras.';
        err.hidden = false; return;
      }
      err.hidden = true; btn.disabled = true; btn.textContent = 'Enviando…';
      var data = { tipo: 'Llamada rápida', nombre: nombre, empresa: '', contacto: tel, email: '', sitio: '', dia: '', franja: '', servicio: tema || 'Sin elegir', pagina: location.pathname.split('/').pop() || 'index.html', url_trap: form.querySelector('[name=url_trap]').value };
      function done(){
        form.classList.add('qf-done'); ok.hidden = false; btn.textContent = 'Enviado ✓';
        if (typeof window.nexbiaConversion === 'function') window.nexbiaConversion('llamada-rapida');
      }
      function fail(){
        btn.disabled = false; btn.innerHTML = 'Quiero que me llaméis gratis <span aria-hidden="true">→</span>';
        err.innerHTML = 'No se ha podido enviar desde aquí. <a href="https://wa.me/34620762842?text=' + encodeURIComponent('Hola, soy ' + nombre + '. Quiero la llamada gratis' + (tema ? ' sobre: ' + tema : '') + '.') + '" target="_blank" rel="noopener"><b>Escríbenos por WhatsApp →</b></a>';
        err.hidden = false;
      }
      fetch(NEXBIA_FORM_URL, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(data) }).then(done).catch(fail);
    });
  }
  document.querySelectorAll('[data-quick-form]').forEach(function(box){ box.innerHTML = html(); wire(box.querySelector('form')); });

  // Ventana: cualquier botón "Consultoría gratis" la abre sin cambiar de página
  if (!window.HTMLDialogElement) return;
  var dlg = null;
  function open(){
    if (!dlg){
      dlg = document.createElement('dialog'); dlg.className = 'qf-dialog'; dlg.setAttribute('aria-labelledby', 'qf-dlg-t');
      dlg.innerHTML = '<button type="button" class="qf-close" aria-label="Cerrar">×</button><h2 id="qf-dlg-t">Te llamamos gratis</h2><p class="qf-sub">15 minutos para ver qué te podemos quitar de encima. Sin compromiso.</p>' + html();
      document.body.appendChild(dlg); wire(dlg.querySelector('form'));
      dlg.querySelector('.qf-close').addEventListener('click', function(){ dlg.close(); });
      dlg.addEventListener('click', function(e){ if (e.target === dlg) dlg.close(); });
    }
    dlg.showModal();
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a.btn-cta, [data-open-form]');
    if (!a) return;
    e.preventDefault(); open();
  });
})();
