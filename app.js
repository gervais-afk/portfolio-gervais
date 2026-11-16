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
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => translate(button.dataset.lang, true)));
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
  $('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
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
  if ('IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        nav.querySelectorAll('a').forEach(link => link.classList.toggle('active', link.hash === '#' + entry.target.id));
      });
    }, {rootMargin: '-15% 0px -55% 0px', threshold: 0});
    document.querySelectorAll('main>section[id]').forEach(section => sectionObserver.observe(section));
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    const revealTargets = document.querySelectorAll('.project-card, .about-intro, .skill-card, .article-card, .contact-grid');
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
      }), {threshold: .07});
      revealTargets.forEach(el => {
        el.classList.add('reveal-ready'); entranceObserver.observe(el);
      });
      // Do not leave content hidden if the preference changes during the visit.
      motion.addEventListener('change', event => { if (event.matches) showAll(); });
    }
  }
})();
