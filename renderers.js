/* Shared by the browser and the static HTML synchroniser. All editorial text is escaped. */
window.PORTFOLIO_RENDER = (() => {
  const e = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const arrow = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M5 12h14m-5-5 5 5-5 5"/></svg>';
  const external = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M14 4h6v6M20 4 10 14m0-9H5a1 1 0 0 0-1 1v13a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1v-5"/></svg>';
  const link = (url, text, cls='text-link') => `<a class="${cls}" href="${e(url)}" target="_blank" rel="noopener noreferrer">${e(text)}${external}</a>`;
  const tags = list => `<ul class="tags" aria-label="Technologies">${list.map(t=>`<li>${e(t)}</li>`).join('')}</ul>`;
  const media = {
    k1: [['k1-interface', 'k1_interface_caption'], ['k1-graph', 'k1_graph_caption']],
    archi: [['archi-building', 'archi_building_caption'], ['archi-site', 'archi_site_caption']],
    dataset: [['dataset-interface', 'dataset_interface_caption']]
  };
  const gallery = (data, id) => media[id] ? `<section class="project-gallery"><h3>${e(data.ui.gallery_title)}</h3><p class="gallery-note">${e(data.ui.gallery_note)}</p>${media[id].map(([file, caption]) => `<figure><a href="assets/images/projects/${file}.webp" target="_blank" rel="noopener noreferrer"><img src="assets/images/projects/${file}.webp" alt="${e(data.ui[caption])}" loading="lazy" decoding="async"><span class="media-open">${e(data.ui.view_visual)}</span></a><figcaption>${e(data.ui[caption])}</figcaption></figure>`).join('')}</section>` : '';
  const more = (id, title, ui) => `<button type="button" class="text-link project-open" data-project="${id}"><span>${e(ui.detail)}</span><span class="sr-only"> — ${e(title)}</span>${arrow}</button>`;
  return {
    escape: e,
    secondary(data) {
      return ['sovereign','asu','vigie'].map((id, i) => {const p=data.projects[id];return `<article class="secondary-card"><span class="small-index">0${i+4}</span><p class="eyebrow">${e(p.label)}</p><h4>${e(p.title)}</h4><p>${e(p.description)}</p>${more(id,p.title,data.ui)}</article>`;}).join('');
    },
    journey(data) { return data.journey.map(j=>`<article class="journey-item"><p class="eyebrow">${e(j.date)}</p><h3>${e(j.title)}</h3><p class="journey-place">${e(j.place)}</p><p>${e(j.desc)}</p></article>`).join(''); },
    skills(data) { return data.skills.map(s=>`<article class="skill-card"><span class="small-index">${e(s.number)}</span><h3>${e(s.title)}</h3><p>${e(s.desc)}</p><ul class="skill-list">${s.items.map(i=>`<li>${e(i)}</li>`).join('')}</ul><p class="tools">${e(s.tools)}</p></article>`).join(''); },
    articles(data) { return data.articles.map(a=>`<article class="article-card"><p class="eyebrow">${e(data.ui.article_label)}</p><h3>${e(a.title)}</h3><p>${e(a.desc)}</p><div class="article-bottom"><span>${e(a.tag)}</span>${link(a.url,data.ui.read_article)}</div></article>`).join(''); },
    projectText(data, id) {
      const p=data.projects[id];
      return `<div class="project-meta"><span>${e(p.label)}</span><span class="project-number">${id==='k1'?'01':id==='archi'?'02':'03'}</span></div><p class="eyebrow project-category">${e(p.category)}</p><h3>${e(p.title)}</h3><p class="project-description">${e(p.description)}</p>${tags(p.tags)}<div class="project-context"><span class="eyebrow">${e(data.ui.context_label)}</span><p>${e(p.context)}</p></div><div class="project-actions">${more(id,p.title,data.ui)}${p.githubPublic !== false ? link(p.github,'GitHub') : p.live ? link(p.live,data.ui.live) : ''}</div>`;
    },
    detail(data, id) {
      const p=data.projects[id], u=data.ui;
      return `<p class="eyebrow">${e(p.label)}</p><h2 id="project-dialog-title" tabindex="-1">${e(p.title)}</h2><p class="dialog-intro">${e(p.description || p.category)}</p><section><h3>${e(u.context_label)}</h3><p>${e(p.context)}</p></section><section><h3>${e(u.role_label)}</h3><p>${e(p.role)}</p></section><section><h3>${e(u.approach_label)}</h3><ol class="approach-list">${p.steps.map(s=>`<li><h4>${e(s[0])}</h4><p>${e(s[1])}</p></li>`).join('')}</ol></section><section class="scope-note"><h3>${e(u.limits_label)}</h3><p>${e(p.limits)}</p></section>${gallery(data,id)}<section><h3>${e(u.stack_label)}</h3>${tags(p.stack)}</section>${p.githubPublic === false || p.websiteAvailable === false ? `<p class="editorial-note">${e(u.link_unavailable)}</p>` : ''}<div class="dialog-links">${p.githubPublic !== false ? link(p.github,u.source,'button button-dark') : ''}${p.live?link(p.live,u.live,'button button-outline'):''}${p.website && p.websiteAvailable !== false?link(p.website,u.website,'button button-outline'):''}${p.githubPublic === false ? `<a class="button button-dark" href="mailto:contact@archicam-ai.com?subject=${encodeURIComponent(p.title)}">${e(u.discuss)}${arrow}</a>` : ''}</div>`;
    }
  };
})();
