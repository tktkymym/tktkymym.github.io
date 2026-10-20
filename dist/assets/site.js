(function () {
  'use strict';
  var isEn = document.documentElement.lang === 'en';
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  function closeMenu() {
    if (!nav || !navToggle) return;
    nav.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  }
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = navToggle.getAttribute('aria-expanded') !== 'true';
      navToggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('open', open);
    });
    nav.querySelectorAll('a').forEach(function (link) { link.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); navToggle.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target) && !navToggle.contains(e.target)) closeMenu();
    });
  }
  var chips = Array.from(document.querySelectorAll('.filter-chip'));
  var papers = Array.from(document.querySelectorAll('.paper[data-category]'));
  var selectedCategory = 'all';
  var search = document.querySelector('#publication-search');
  var yearSelect = document.querySelector('#publication-year');
  var typeSelect = document.querySelector('#publication-type');
  var yearGroups = Array.from(document.querySelectorAll('.publication-year'));
  var entries = Array.from(document.querySelectorAll('.legacy-entry'));
  var groups = Array.from(document.querySelectorAll('.legacy-group'));
  var status = document.querySelector('#search-status');
  var empty = document.querySelector('#no-papers');
  function normalized(s) { return s.normalize('NFKC').toLocaleLowerCase().replace(/\s+/g, ' ').trim(); }
  var searchIndex = new WeakMap();
  papers.concat(entries).forEach(function (item) { searchIndex.set(item, normalized(item.textContent)); });
  function applyFilters() {
    var query = normalized(search ? search.value : '');
    var terms = query ? query.split(' ') : [];
    var shownPapers = 0;
    var shownArchive = 0;
    var selectedYear = yearSelect ? yearSelect.value : 'all';
    var selectedType = typeSelect ? typeSelect.value : 'all';
    papers.forEach(function (paper) {
      var categoryMatch = selectedCategory === 'all' || paper.dataset.category === selectedCategory;
      var yearMatch = selectedYear === 'all' || paper.dataset.year === selectedYear;
      var typeMatch = selectedType === 'all' || paper.dataset.type === selectedType;
      var text = searchIndex.get(paper);
      var match = categoryMatch && yearMatch && typeMatch && terms.every(function (term) { return text.includes(term); });
      paper.hidden = !match;
      if (match) shownPapers++;
    });
    yearGroups.forEach(function (group) {
      var visible = group.querySelectorAll('.paper:not([hidden])').length;
      group.hidden = visible === 0;
      group.querySelector('.year-count').textContent = visible;
    });
    entries.forEach(function (entry) {
      var text = searchIndex.get(entry);
      var match = terms.every(function (term) { return text.includes(term); });
      entry.hidden = !match;
      if (match) shownArchive++;
    });
    groups.forEach(function (group) {
      var visible = group.querySelectorAll('.legacy-entry:not([hidden])').length;
      group.hidden = visible === 0;
      if (query) group.open = visible > 0;
      else group.open = false;
      var count = group.querySelector('.group-count');
      if (count) count.textContent = visible + (isEn ? ' records' : '件');
    });
    if (empty) empty.hidden = shownPapers !== 0;
    if (status) status.textContent = isEn
      ? 'Papers: ' + shownPapers + ' / ' + papers.length + ' · Historical record: ' + shownArchive + ' / ' + entries.length
      : '論文 ' + shownPapers + ' / ' + papers.length + ' 件 ・ 過去の業績 ' + shownArchive + ' / ' + entries.length + ' 件';
  }
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      selectedCategory = chip.dataset.filter;
      chips.forEach(function (item) { item.setAttribute('aria-pressed', String(item === chip)); });
      applyFilters();
    });
  });
  if (search) search.addEventListener('input', applyFilters);
  if (yearSelect) yearSelect.addEventListener('change', applyFilters);
  if (typeSelect) typeSelect.addEventListener('change', applyFilters);
  var reset = document.querySelector('#reset-search');
  if (reset && search) reset.addEventListener('click', function () {
    search.value = '';
    if (yearSelect) yearSelect.value = 'all';
    if (typeSelect) typeSelect.value = 'all';
    selectedCategory = 'all';
    chips.forEach(function (item) { item.setAttribute('aria-pressed', String(item.dataset.filter === 'all')); });
    applyFilters();
    search.focus();
  });
  var params = new URLSearchParams(window.location.search);
  var initialCategory = params.get('category');
  if (initialCategory) {
    var initialChip = chips.find(function (chip) { return chip.dataset.filter === initialCategory; });
    if (initialChip) {
      selectedCategory = initialCategory;
      chips.forEach(function (item) { item.setAttribute('aria-pressed', String(item === initialChip)); });
    }
  }
  if (search && params.has('q')) search.value = params.get('q');
  [[yearSelect, 'year'], [typeSelect, 'type']].forEach(function (setting) {
    var select = setting[0];
    var initial = params.get(setting[1]);
    if (select && initial && Array.from(select.options).some(function (option) { return option.value === initial; })) select.value = initial;
  });
  if (papers.length) applyFilters();
  var copy = document.querySelector('.copy-email');
  var copyStatus = document.querySelector('#copy-status');
  if (copy) copy.addEventListener('click', async function () {
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('clipboard unavailable');
      await navigator.clipboard.writeText('takayoshi@isc.chubu.ac.jp');
      copyStatus.textContent = isEn ? 'Email address copied.' : 'メールアドレスをコピーしました。';
    } catch (e) {
      copyStatus.textContent = isEn ? 'Please select and copy the email address above.' : '上のメールアドレスを選択してコピーしてください。';
    }
  });
})();
