const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

const dictionary = document.querySelector('#dictionary');
if (dictionary) {
  const input = document.querySelector('#dictionary-query');
  const rows = [...dictionary.tBodies[0].rows];
  const indexed = rows.map(row => normalize(row.textContent));
  const status = document.querySelector('#dictionary-status');
  document.querySelector('.dictionary-tools').hidden = false;
  const filter = () => {
    const query = normalize(input.value.trim());
    let count = 0;
    rows.forEach((row, i) => { row.hidden = !indexed[i].includes(query); if (!row.hidden) count++; });
    status.textContent = `${count} of ${rows.length} records`;
  };
  input.addEventListener('input', filter);
  filter();
}

const form = document.querySelector('.search-form');
if (form) {
  const query = document.querySelector('#query');
  const category = document.querySelector('#category');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#results');
  const more = document.querySelector('#more-results');
  let indexPromise, matches = [], shown = 0, sequence = 0, timer;
  const params = new URLSearchParams(location.search);
  query.value = (params.get('q') || '').slice(0, 200);
  category.value = params.get('category') || '';
  function appendResults() {
    const next = matches.slice(shown, shown + 20);
    for (const match of next) {
      const li = document.createElement('li');
      const label = document.createElement('span'); label.className = 'eyebrow'; label.textContent = match.category;
      const h2 = document.createElement('h2');
      const a = document.createElement('a'); a.href = match.href; a.textContent = match.title;
      h2.append(a);
      const p = document.createElement('p');
      const text = match.text.replace(/\s+/g, ' ').trim();
      const pos = Math.max(0, normalize(text).indexOf(normalize(query.value.trim())) - 65);
      p.textContent = (pos ? '…' : '') + text.slice(pos, pos + 230) + (text.length > pos + 230 ? '…' : '');
      li.append(label, h2, p); results.append(li);
    }
    shown += next.length;
    more.hidden = shown >= matches.length;
    status.textContent = matches.length ? `${matches.length} results. Showing ${shown}.` : 'No results. Try a shorter term or choose Everything.';
  }
  async function search() {
    const request = ++sequence;
    const raw = query.value.trim();
    const selected = category.value;
    const url = new URL(location.href);
    if (raw) url.searchParams.set('q', raw); else url.searchParams.delete('q');
    if (selected) url.searchParams.set('category', selected); else url.searchParams.delete('category');
    history.replaceState(null, '', url);
    results.replaceChildren(); more.hidden = true;
    if (!raw && !selected) { status.textContent = 'Enter a word or phrase to explore the lore.'; return; }
    status.textContent = 'Searching the lore…';
    try {
      indexPromise ||= fetch('search-index.json').then(response => { if (!response.ok) throw new Error('Search unavailable'); return response.json(); }).catch(error => { indexPromise = undefined; throw error; });
      const index = await indexPromise;
      if (request !== sequence) return;
      const terms = normalize(raw).split(/\s+/).filter(Boolean);
      matches = index.filter(item => (!selected || item.category === selected) && terms.every(term => normalize(item.title + ' ' + item.text).includes(term)));
      const score = item => terms.reduce((sum, term) => sum + (normalize(item.title).includes(term) ? 1 : 0), 0);
      matches.sort((a,b) => score(b) - score(a) || a.title.localeCompare(b.title));
      shown = 0; appendResults();
    } catch {
      if (request === sequence) status.textContent = 'Search could not load. Submit again to retry, or browse the topic links in the navigation.';
    }
  }
  form.addEventListener('submit', event => { event.preventDefault(); clearTimeout(timer); search(); });
  query.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(search, 250); });
  category.addEventListener('change', () => { clearTimeout(timer); search(); });
  more.addEventListener('click', () => {
    const previous = results.children.length;
    appendResults();
    // Move focus to the newly revealed content before the button disappears.
    results.children[previous]?.querySelector('a').focus();
  });
  if (query.value || category.value) search();
}
