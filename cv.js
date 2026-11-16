/* All editorial content comes from generated profile.js, also usable with file://. */
(() => {
  'use strict';
  const profile = window.PORTFOLIO_PROFILE;
  if (!profile) {
    document.getElementById('cv').textContent = 'Profil indisponible / Profile unavailable. Please download the PDF.';
    return;
  }
  const paths = {
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    phone: '<path d="m7 3 3 5-2 2a14 14 0 0 0 6 6l2-2 5 3c-1 7-9 4-14-1S0 4 7 3Z"/>',
    pin: '<path d="M12 22S4 14 4 9a8 8 0 1 1 16 0c0 5-8 13-8 13Z"/><circle cx="12" cy="9" r="2.5"/>',
    github: '<path d="M9 19c-5 2-5-3-7-3m14 6v-4a4 4 0 0 0-1-3c4 0 7-2 7-6a5 5 0 0 0-1-4c0-1 0-3-1-3-2 0-3 1-4 1a14 14 0 0 0-7 0C7 2 5 1 4 2s0 3 0 3a5 5 0 0 0-2 4c0 4 3 6 7 6-1 1-1 2-1 3v4"/>',
    linkedin: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7m4 0v-7m0 3c0-4 6-4 6 0v4M7 7v.1"/>',
    dev: '<rect x="1" y="4" width="22" height="16" rx="2"/><text x="3" y="15" fill="currentColor" stroke="none" font-family="Arial,sans-serif" font-weight="bold" font-size="8">DEV</text>',
    link: '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>'
  };
  const escape = text => String(text).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  const icon = kind => `<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${paths[kind]}</svg>`;
  function render(lang) {
    const data = profile.cv[lang];
    const identity = profile.identity;
    const contact = (kind, label, href) => `<${href ? `a href="${escape(href)}"` : 'span'} class="contact">${icon(kind)}<span>${escape(label)}</span></${href ? 'a' : 'span'}>`;
    const urlContact = key => contact(({github: 'github', linkedin: 'linkedin', devto: 'dev'})[key] || 'link', identity[key].replace(/^https:\/\//, ''), identity[key]);
    const entry = (item, project = false) => `<article class="entry${project ? ' project-entry' : ''}"><h3>${escape(item.title)}${item.date ? `<span class="date">${escape(item.date)}</span>` : ''}</h3>${item.context ? `<p class="context">${escape(item.context)}</p>` : ''}${project ? `<ul class="project-details">${item.details.map(text => `<li>${escape(text)}</li>`).join('')}</ul>` : item.details.map(text => `<p>${escape(text)}</p>`).join('')}${item.stack ? `<p class="stack">${escape(item.stack)}</p>` : ''}</article>`;
    const section = (key, content) => `<section aria-labelledby="heading-${key}"><h2 id="heading-${key}">${escape(data.labels[key])}</h2>${content}</section>`;
    document.documentElement.lang = lang;
    document.title = `CV · ${identity.name} · ${data.title}`;
    document.querySelector('meta[name="description"]').content = `${identity.name} — ${data.title}. ${data.summary}`;
    document.querySelector('.toolbar').setAttribute('aria-label', lang === 'fr' ? 'Actions CV' : 'CV actions');
    document.getElementById('back-link').href = 'index.html?lang=' + lang;
    document.getElementById('cv').innerHTML = `<header class="identity"><div class="identity-main"><div class="identity-copy"><h1><span class="family-name">${escape(identity.familyName)}</span> <span class="given-names">${escape(identity.givenNames)}</span></h1><p class="target">${escape(data.title)}</p></div><img class="cv-photo" src="${escape(identity.photo)}" width="480" height="600" alt="${lang === 'fr' ? 'Portrait de' : 'Portrait of'} ${escape(identity.name)}" fetchpriority="high"></div><address><div class="contact-row">${contact('mail', identity.email, `mailto:${identity.email}`)}${contact('phone', identity.phone, identity.phoneHref)}${contact('pin', identity.location[lang])}</div><div class="contact-row">${urlContact('github')}${urlContact('linkedin')}</div><div class="contact-row">${urlContact('devto')}${urlContact('website')}</div></address></header><p class="summary">${escape(data.summary)}</p><div class="cv-columns"><div class="cv-main">${section('projects', data.projects.map(item => entry(item, true)).join(''))}${section('experience', data.experience.map(item => entry(item)).join(''))}</div><div class="cv-sidebar">${section('skills', data.skills.map(item => `<p class="skill"><strong>${escape(item.label)}</strong><span>${escape(item.text)}</span></p>`).join(''))}${section('education', data.education.map(item => entry(item)).join(''))}${section('additional', `<p>${escape(data.languages)}</p>`)}${section('award', `<p class="award">${escape(data.award)}</p>`)}</div></div>`;
    document.querySelectorAll('[data-lang]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.lang === lang)));
    const pdf = document.getElementById('download-pdf');
    const docx = document.getElementById('download-docx');
    pdf.href = data.files.pdf;
    docx.href = data.files.docx;
    pdf.textContent = lang === 'fr' ? 'PDF présentation' : 'Presentation PDF';
    pdf.setAttribute('aria-label', lang === 'fr' ? 'PDF présentation — Télécharger le CV français avec photo' : 'Presentation PDF — Download the English CV with photo');
    const ats = document.getElementById('download-ats');
    ats.href = data.files.atsPdf;
    ats.textContent = lang === 'fr' ? 'PDF candidature' : 'Application PDF';
    ats.setAttribute('aria-label', lang === 'fr' ? 'PDF candidature — Télécharger le CV français, une colonne et sans photo' : 'Application PDF — Download the English CV, one column and no photo');
    document.getElementById('download-note').textContent = lang === 'fr'
      ? 'Présentation : deux colonnes avec photo. Candidature : une colonne, sans photo, pour les plateformes de recrutement. Même contenu ; aucune garantie de classement ATS.'
      : 'Presentation: two columns with a photo. Application: one column, no photo, for recruitment platforms. Same content; no guarantee of ATS ranking.';
    docx.setAttribute('aria-label', lang === 'fr' ? 'Télécharger le CV Word français (DOCX)' : 'Download English Word CV (DOCX)');
    document.getElementById('print-cv').textContent = lang === 'fr' ? 'Imprimer' : 'Print';
  }
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => {
    const lang = button.dataset.lang;
    const url = new URL(window.location.href);
    url.searchParams.set('lang', lang);
    history.replaceState(null, '', url);
    render(lang);
  }));
  document.getElementById('print-cv').addEventListener('click', () => window.print());
  render(new URLSearchParams(window.location.search).get('lang') === 'en' ? 'en' : 'fr');
})();
