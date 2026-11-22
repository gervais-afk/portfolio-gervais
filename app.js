/* Progressive enhancement. French core content is statically rendered. */
(() => {
  'use strict';
  const content = window.PORTFOLIO_CONTENT;
  const render = window.PORTFOLIO_RENDER;
  if (!content || !render) return;
  const $ = selector => document.querySelector(selector);
  let lang = new URLSearchParams(location.search).get('lang') === 'en' ? 'en' : 'fr';
  let openProject = null;
  let opener = null;
  const dialog = $('#project-dialog');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const menu = $('.menu-toggle');
  const nav = $('#main-nav');
  const targets = {secondary: '#secondary-projects', journey: '#journey', skills: '#skill-cards', articles: '#article-cards'};
  function closeMenu(returnFocus = false) {
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', content[lang].ui.menu);
    nav.classList.remove('is-open');
    if (returnFocus) menu.focus();
  }
  function translate(nextLang, updateUrl = false) {
    lang = nextLang;
    const data = content[lang], ui = data.ui;
    document.documentElement.lang = lang;
    document.title = ui.page_title;
    $('meta[name="description"]').content = ui.page_description;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      if (ui[el.dataset.i18n] !== undefined) el.textContent = ui[el.dataset.i18n];
    });
    Object.entries(targets).forEach(([key, selector]) => {$(selector).innerHTML = render[key](data);});
    ['k1','archi','dataset'].forEach(id => {$('#project-' + id).innerHTML = render.projectText(data, id);});
    document.querySelectorAll('[data-lang]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.lang === lang)));
    document.querySelectorAll('[data-cv-page]').forEach(link => {link.href = 'cv.html?lang=' + lang;});
    document.querySelectorAll('[data-cv-download]').forEach(link => {link.href = `KOA_MARIE_GERVAIS_NELLY_CV_${lang.toUpperCase()}.pdf`;});
    $('.dialog-close').setAttribute('aria-label', ui.close);
    menu.setAttribute('aria-label', menu.getAttribute('aria-expanded') === 'true' ? ui.close_menu : ui.menu);
    nav.setAttribute('aria-label', lang === 'fr' ? 'Navigation principale' : 'Main navigation');
    $('.portrait-frame img').alt = (lang === 'fr' ? 'Portrait de ' : 'Portrait of ') + 'KOA Marie Gervais Nelly';
    $('#archive-player').setAttribute('aria-label', lang === 'fr' ? 'Synthèse audio NotebookLM' : 'NotebookLM audio summary');
    $('#copy-status').textContent = '';
    if (openProject) $('#project-dialog-content').innerHTML = render.detail(data, openProject);
    if (updateUrl) {
      const url = new URL(location.href);
      url.searchParams.set('lang', lang);
      history.replaceState(null, '', url);
    }
  }
  translate(lang);
  let pendingLang = null, langTransition = null;
  function applyPendingLang() {
    if (!pendingLang) return;
    translate(pendingLang, true);
    pendingLang = null;
    requestAnimationFrame(placeIndicator);
  }
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => {
    const next = button.dataset.lang;
    if (next === (pendingLang || lang)) return;
    pendingLang = next;
    // A second click during a transition applies immediately, so the last choice always wins.
    if (langTransition || !document.startViewTransition || motion.matches) { applyPendingLang(); return; }
    langTransition = document.startViewTransition(applyPendingLang);
    langTransition.ready.catch(() => {});
    langTransition.finished.catch(() => {}).then(() => { langTransition = null; });
  }));
  menu.addEventListener('click', () => {
    const expanded = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(expanded));
    menu.setAttribute('aria-label', expanded ? content[lang].ui.close_menu : content[lang].ui.menu);
    nav.classList.toggle('is-open', expanded);
  });
  nav.addEventListener('click', event => {if (event.target.closest('a')) closeMenu();});
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (menu.getAttribute('aria-expanded') === 'true' && !event.target.closest('.site-header')) closeMenu();
    const button = event.target.closest('.project-open');
    if (!button) return;
    const id = button.dataset.project;
    if (!content[lang].projects[id]) return;
    opener = button;
    openProject = id;
    $('#project-dialog-content').innerHTML = render.detail(content[lang], id);
    $('#dialog-index').textContent = String(['k1','archi','dataset','sovereign','asu','vigie'].indexOf(id) + 1).padStart(2,'0');
    dialog.showModal();
    dialog.scrollTop = 0;
    document.body.classList.add('modal-open');
    $('#project-dialog-title').focus({preventScroll: true});
  });
  // Keep keyboard navigation within the modal, including at browser chrome boundaries.
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const focusable = Array.from(dialog.querySelectorAll('a[href], button:not([disabled]), [tabindex="0"]'));
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (event.shiftKey && (document.activeElement === first || document.activeElement.id === 'project-dialog-title')) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); first.focus();
    }
  });
  function closeDialog() {
    if (!dialog.open || dialog.classList.contains('is-closing')) return;
    if (motion.matches || typeof dialog.getAnimations !== 'function') { dialog.close(); return; }
    dialog.classList.add('is-closing');
    let done = false;
    const finish = () => { if (done) return; done = true; dialog.classList.remove('is-closing'); dialog.close(); };
    dialog.addEventListener('animationend', event => { if (event.target === dialog) finish(); }, {once: true});
    setTimeout(finish, 400);
  }
  dialog.addEventListener('cancel', event => { event.preventDefault(); closeDialog(); });
  $('.dialog-close').addEventListener('click', closeDialog);
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) closeDialog();
  });
  dialog.addEventListener('close', () => {
    dialog.classList.remove('is-closing');
    document.body.classList.remove('modal-open');
    openProject = null;
    if (opener && opener.isConnected) opener.focus({preventScroll:true});
  });
  $('.copy-email').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText('contact@archicam-ai.com');
      $('#copy-status').textContent = content[lang].ui.copied;
    } catch {
      $('#copy-status').textContent = content[lang].ui.copy_failed;
    }
  });
  // No audio source or request until the visitor explicitly opens the archive.
  const audioFiles = [
    'podcast_notebooklm_deep_dive.m4a',
    'Bâtir_une_IA_souveraine_sans_hallucinations.m4a',
    'IA_sans_cloud_du_BTP_au_Sahel.m4a',
    'L’IA_souveraine_et_déterministe_sans_cloud.m4a',
    'Offline_AI_for_African_Construction_and_Health.m4a',
    'Sovereign_AI_for_air-gapped_aviation_security.m4a'
  ];
  const audio = $('#archive-player');
  function selectAudio() {
    audio.pause();
    audio.src = 'assets/audio/' + encodeURIComponent(audioFiles[Number($('#audio-select').value)]);
    $('.audio-status').textContent = '';
    audio.load();
  }
  $('#audio-details').addEventListener('toggle', event => {
    if (event.target.open && !audio.getAttribute('src')) selectAudio();
    if (!event.target.open) audio.pause();
  });
  $('#audio-select').addEventListener('change', selectAudio);
  audio.addEventListener('error', () => {$('.audio-status').textContent = content[lang].ui.audio_error;});
  $('#year').textContent = new Date().getFullYear();
  // Sliding navigation indicator: follows the hovered link, rests on the active section.
  const indicator = nav.querySelector('.nav-indicator');
  let hoveredLink = null;
  function placeIndicator() {
    if (!indicator) return;
    const link = hoveredLink || nav.querySelector('a.active');
    if (!link || getComputedStyle(indicator).display === 'none') { nav.style.setProperty('--nav-o', '0'); return; }
    nav.style.setProperty('--nav-x', link.offsetLeft + 'px');
    nav.style.setProperty('--nav-w', link.offsetWidth + 'px');
    nav.style.setProperty('--nav-o', hoveredLink && !hoveredLink.classList.contains('active') ? '.45' : '1');
  }
  if (indicator) {
    nav.classList.add('has-indicator');
    nav.addEventListener('pointerover', event => { const a = event.target.closest('a'); if (a) { hoveredLink = a; placeIndicator(); } });
    nav.addEventListener('pointerleave', () => { hoveredLink = null; placeIndicator(); });
    addEventListener('resize', placeIndicator, {passive: true});
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeIndicator);
  }

  // Pointer light on cards (fine pointers only, delegated so re-rendered cards keep it).
  if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.addEventListener('pointermove', event => {
      const card = event.target.closest && event.target.closest('.project-card, .secondary-card, .skill-card, .article-card');
      if (!card) return;
      const box = card.getBoundingClientRect();
      card.style.setProperty('--mx', (event.clientX - box.left) + 'px');
      card.style.setProperty('--my', (event.clientY - box.top) + 'px');
    }, {passive: true});
  }

  // One scroll loop for header state, reading progress, timeline drawing and gentle parallax.
  const header = $('.site-header');
  const journey = $('.journey');
  const portraitFrame = $('.portrait-frame');
  const hero = $('.hero');
  let ticking = false;
  function onScroll() {
    ticking = false;
    const y = scrollY, vh = innerHeight;
    const max = document.documentElement.scrollHeight - vh;
    header.classList.toggle('is-scrolled', y > 8);
    header.style.setProperty('--progress', max > 0 ? Math.min(1, y / max).toFixed(4) : '0');
    if (motion.matches) return;
    if (journey) {
      const box = journey.getBoundingClientRect();
      const ratio = (vh * .62 - box.top) / box.height;
      journey.style.setProperty('--journey', Math.max(0, Math.min(1, ratio)).toFixed(3));
    }
    if (portraitFrame && hero && y < hero.offsetHeight + 200) {
      portraitFrame.style.setProperty('--portrait-shift', (y * -0.045).toFixed(1) + 'px');
      hero.style.setProperty('--grid-shift', (y * 0.12).toFixed(1) + 'px');
    }
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, {passive: true});
  addEventListener('resize', onScroll, {passive: true});
  onScroll();

  if ('IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        nav.querySelectorAll('a').forEach(link => link.classList.toggle('active', link.hash === '#' + entry.target.id));
        placeIndicator();
      });
    }, {rootMargin: '-15% 0px -55% 0px', threshold: 0});
    document.querySelectorAll('main>section[id]').forEach(section => sectionObserver.observe(section));
    const revealTargets = document.querySelectorAll([
      '.section-heading', '.discipline-rail', '.project-card', '.other-heading', '.secondary-card',
      '.about-intro', '.journey-item', '.skill-card', '.learning-note', '.article-card',
      '.audio-archive', '.contact-grid > div'
    ].join(','));
    let entranceObserver;
    function showAll() {
      if (entranceObserver) entranceObserver.disconnect();
      revealTargets.forEach(el => {
        el.classList.remove('reveal-ready');
        el.classList.add('is-visible');
      });
    }
    if (!motion.matches) {
      entranceObserver = new IntersectionObserver(entries => entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          entranceObserver.unobserve(entry.target);
        }
      }), {threshold: 0, rootMargin: '0px 0px -12% 0px'});
      revealTargets.forEach(el => {
        // Siblings in the same grid arrive one after another, never more than ~0.4 s apart.
        const siblings = Array.from(el.parentElement.children).filter(child => child.matches && Array.prototype.includes.call(revealTargets, child));
        const index = Math.max(0, siblings.indexOf(el));
        if (index) el.style.setProperty('--delay', Math.min(index * 0.11, 0.44) + 's');
        el.classList.add('reveal-ready');
        entranceObserver.observe(el);
      });
      // Do not leave content hidden if the preference changes during the visit.
      motion.addEventListener('change', event => { if (event.matches) showAll(); });
    }
  }
})();
