// /packages/ — behaviour for the package catalogue.
//
// The page itself is rendered at build time from _data/npm_stats.yml (see
// scripts/fetch_npm_stats.py); nothing here fetches anything. Same house style
// as shell.js: vanilla, driving the classes Carbon's CSS already ships, every
// feature guarded by its own root element so the static render always stands
// on its own. The parts that make no sense without JavaScript (the toolbar,
// the odometer, the copy buttons) ship `hidden` in the markup and are
// revealed here.
(function () {
  'use strict';

  var REDUCED = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)').matches : false;
  var NUMBER = new Intl.NumberFormat('en-US');

  function all(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = text;
    return node;
  }

  function num(value) {
    return NUMBER.format(Math.round(value));
  }

  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  // "2026-06-04" -> "4 Jun 2026". Read as UTC so the date never slips a day,
  // and spelled out by hand to match the dates Liquid renders ("%-d %b %Y") —
  // toLocaleDateString says "Sept" in some locales and "September" in others.
  function day(iso) {
    var parsed = new Date(iso + 'T00:00:00Z');
    if (isNaN(parsed.getTime())) return iso;
    return parsed.getUTCDate() + ' ' + MONTHS[parsed.getUTCMonth()] + ' ' + parsed.getUTCFullYear();
  }

  function pick(list) {
    return list[Math.floor(Math.random() * list.length)];
  }

  function shuffled(list) {
    var copy = list.slice();
    for (var i = copy.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var swap = copy[i];
      copy[i] = copy[j];
      copy[j] = swap;
    }
    return copy;
  }

  function announce(message) {
    var region = document.querySelector('[data-announce]');
    if (region) region.textContent = message;
  }

  // --- Copy buttons ---------------------------------------------------------
  // Every [data-copy] button copies its own attribute; the terminal keeps its
  // button's attribute in step with whatever is on screen.
  function copyToClipboard(text) {
    // The async API is the good path, but it rejects wherever the permission
    // is withheld (some Safari and Firefox contexts, an unfocused document),
    // so a rejection falls through to the old selection trick rather than
    // straight to an error.
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () { return selectionCopy(text); });
    }
    return selectionCopy(text);
  }

  function selectionCopy(text) {
    return new Promise(function (resolve, reject) {
      var area = el('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      var copied = false;
      try { copied = document.execCommand('copy'); } catch (e) { copied = false; }
      document.body.removeChild(area);
      if (copied) resolve(); else reject(new Error('copy unavailable'));
    });
  }

  function initCopyButtons() {
    document.addEventListener('click', function (event) {
      var button = event.target.closest('[data-copy]');
      if (!button) return;
      var label = button.querySelector('[data-copy-label]');
      copyToClipboard(button.getAttribute('data-copy')).then(function () {
        button.classList.add('is-copied');
        if (label) label.textContent = 'Copied';
        announce('Copied to clipboard');
        clearTimeout(button.copyTimer);
        button.copyTimer = setTimeout(function () {
          button.classList.remove('is-copied');
          if (label) label.textContent = 'Copy';
        }, 2000);
      }, function () {
        announce('Could not copy — select the command and copy it by hand.');
      });
    });
  }

  // Snippets carry the text to copy; the button itself is cloned in from one
  // template, so the icons are not repeated ~150 times in the HTML.
  function initSnippets() {
    var template = document.querySelector('[data-copy-button]');
    if (!template || !template.content) return;
    all('[data-copy-text]').forEach(function (snippet) {
      var text = snippet.getAttribute('data-copy-text');
      var button = template.content.firstElementChild.cloneNode(true);
      button.setAttribute('data-copy', text);
      button.setAttribute('aria-label', 'Copy command: ' + text);
      snippet.appendChild(button);
    });
  }

  // --- Hero terminal --------------------------------------------------------
  // Types out the README examples of one package after another. The command
  // currently on screen is the one the copy button hands over.
  function initTerminal() {
    var root = document.querySelector('[data-term]');
    if (!root) return;

    var items = all('[data-term-list] li', root).map(function (node) {
      return {
        name: node.getAttribute('data-name'),
        command: node.getAttribute('data-command'),
        desc: node.getAttribute('data-desc'),
        examples: (node.getAttribute('data-examples') || '').split('\n').filter(Boolean)
      };
    }).filter(function (item) { return item.examples.length; });
    if (!items.length) return;
    // With a single package there is nothing to cycle through, but its command
    // is still on screen and still worth copying.
    var cycles = items.length > 1;

    var comment = root.querySelector('[data-term-comment]');
    var installLine = root.querySelector('[data-term-install-line]');
    var install = root.querySelector('[data-term-install]');
    var command = root.querySelector('[data-term-cmd]');
    var copyButton = root.querySelector('[data-term-copy]');
    var nextButton = root.querySelector('[data-term-next]');
    var pauseButton = root.querySelector('[data-term-pause]');

    var queue = shuffled(items);
    var position = -1;
    var typeTimer = null;
    var nextTimer = null;
    // Reduced motion: nothing types itself and nothing advances on its own.
    var paused = REDUCED;
    // Two flags rather than one counter: `focusin` bubbles on every focus
    // change inside the terminal while `focusout` only fires clear of it, so a
    // counter climbs as you tab between the buttons and never comes back down.
    var hovering = false;
    var focused = false;

    function schedule() {
      clearTimeout(nextTimer);
      if (!cycles || paused || hovering || focused || document.hidden) return;
      nextTimer = setTimeout(advance, 4200);
    }

    function render(item, example) {
      clearTimeout(typeTimer);
      var installCommand = /^npx\s/.test(example) ? '' : 'npm i -g ' + item.name;
      comment.textContent = '# ' + item.command + ' — ' + item.desc;
      install.textContent = installCommand;
      installLine.hidden = !installCommand;
      copyButton.setAttribute('data-copy', (installCommand ? installCommand + '\n' : '') + example);

      if (REDUCED) {
        command.textContent = example;
        return;
      }
      var typed = 0;
      command.textContent = '';
      (function type() {
        typed += 1;
        command.textContent = example.slice(0, typed);
        if (typed < example.length) typeTimer = setTimeout(type, 25 + Math.random() * 45);
        else schedule();
      })();
    }

    function advance() {
      position = (position + 1) % queue.length;
      var item = queue[position];
      render(item, pick(item.examples));
    }

    root.addEventListener('mouseenter', function () { hovering = true; schedule(); });
    root.addEventListener('mouseleave', function () { hovering = false; schedule(); });
    root.addEventListener('focusin', function () { focused = true; schedule(); });
    root.addEventListener('focusout', function (event) {
      if (root.contains(event.relatedTarget)) return;
      focused = false;
      schedule();
    });
    // Nothing to type into a tab nobody is looking at.
    document.addEventListener('visibilitychange', schedule);

    copyButton.hidden = false;

    if (cycles) {
      nextButton.hidden = false;
      nextButton.addEventListener('click', advance);
    }

    if (cycles && !REDUCED) {
      pauseButton.hidden = false;
      pauseButton.addEventListener('click', function () {
        paused = !paused;
        pauseButton.textContent = paused ? 'Play' : 'Pause';
        pauseButton.setAttribute('aria-pressed', String(paused));
        schedule();
      });
      schedule();
    }
  }

  // --- Install odometer -----------------------------------------------------
  // Downloads are counted per day, so at ~470 a day a whole-number counter
  // would read 0 for the length of a visit. It counts fractions instead, and
  // says outright that it is a rate, not a live feed.
  function initOdometer() {
    var root = document.querySelector('[data-odometer]');
    if (!root) return;
    var perDay = parseFloat(root.getAttribute('data-rate'));
    if (!(perDay > 0)) return;

    var value = root.querySelector('[data-odometer-value]');
    var every = root.querySelector('[data-odometer-every]');
    var seconds = 86400 / perDay;
    every.textContent = seconds < 90 ? Math.round(seconds) + ' seconds'
      : seconds < 5400 ? Math.round(seconds / 60) + ' minutes'
        : Math.round(seconds / 3600) + ' hours';

    var opened = Date.now();
    root.hidden = false;
    setInterval(function () {
      // The count is derived from elapsed time, so there is nothing to catch
      // up on — a hidden tab simply skips the paint.
      if (document.hidden) return;
      value.textContent = ((Date.now() - opened) / 1000 / seconds).toFixed(2);
    }, 500);
  }

  // --- Catalogue: expand, sort, filter --------------------------------------
  function initCatalogue() {
    var table = document.querySelector('[data-pkg-table]');
    if (!table) return;

    var groups = all('tbody[data-group]', table);
    var entries = all('tr[data-pkg]', table).map(function (row, index) {
      return {
        row: row,
        detail: row.nextElementSibling,
        group: row.parentNode,
        order: index,
        domain: row.getAttribute('data-domain'),
        text: row.getAttribute('data-search') || '',
        keys: {
          name: (row.getAttribute('data-command') || row.getAttribute('data-short') || '').toLowerCase(),
          month: Number(row.getAttribute('data-month')) || 0,
          year: Number(row.getAttribute('data-year')) || 0
        }
      };
    });
    if (!entries.length) return;

    all('.cds--table-expand__button', table).forEach(function (button) { button.hidden = false; });

    // Expanding rows. Carbon's contract: the parent row carries
    // .cds--expandable-row while open and the expand cell carries
    // data-previous-value="collapsed", which turns the chevron.
    table.addEventListener('click', function (event) {
      var button = event.target.closest('.cds--table-expand__button');
      if (!button || !table.contains(button)) return;
      var row = button.closest('tr');
      var detail = row.nextElementSibling;
      var open = !row.classList.contains('cds--expandable-row');
      row.classList.toggle('cds--expandable-row', open);
      button.setAttribute('aria-expanded', String(open));
      button.setAttribute('aria-label', (open ? 'Hide' : 'Show') + ' details for ' + row.getAttribute('data-name'));
      if (open) button.parentNode.setAttribute('data-previous-value', 'collapsed');
      else button.parentNode.removeAttribute('data-previous-value');
      // A collapsed detail row is only 0px tall, so without `inert` its links
      // and copy buttons would still be in the tab order.
      if (detail) {
        if (open) detail.removeAttribute('inert');
        else detail.setAttribute('inert', '');
      }
    });

    // Sorting flattens the table: the group bodies step aside and every row
    // moves into one list. Carbon's third click ("none") brings the groups
    // back, which makes grouped-by-domain the table's resting state.
    var flat = el('tbody');
    flat.setAttribute('data-flat', '');
    flat.hidden = true;
    table.appendChild(flat);

    var headers = all('th[data-sort]', table);
    var sortKey = null;
    var sortDir = 'none';

    function applySort(key, direction) {
      sortKey = key;
      sortDir = direction;
      headers.forEach(function (header) {
        var active = key && header.getAttribute('data-sort') === key;
        var button = header.querySelector('.cds--table-sort');
        header.setAttribute('aria-sort', active ? direction : 'none');
        button.classList.toggle('cds--table-sort--active', !!active);
        button.classList.toggle('cds--table-sort--descending', !!active && direction === 'descending');
      });

      if (!key) {
        entries.forEach(function (entry) {
          entry.group.appendChild(entry.row);
          entry.group.appendChild(entry.detail);
        });
        flat.hidden = true;
      } else {
        var sign = direction === 'ascending' ? 1 : -1;
        entries.slice().sort(function (a, b) {
          var left = a.keys[key];
          var right = b.keys[key];
          var result = typeof left === 'string' ? left.localeCompare(right) : left - right;
          return (result * sign) || (a.order - b.order);
        }).forEach(function (entry) {
          flat.appendChild(entry.row);
          flat.appendChild(entry.detail);
        });
        flat.hidden = false;
      }
      applyFilter();
    }

    headers.forEach(function (header) {
      header.querySelector('.cds--table-sort').addEventListener('click', function () {
        var key = header.getAttribute('data-sort');
        // Numbers are most useful biggest-first; names read A to Z.
        var cycle = key === 'name'
          ? ['ascending', 'descending', 'none']
          : ['descending', 'ascending', 'none'];
        var next = sortKey === key ? cycle[(cycle.indexOf(sortDir) + 1) % cycle.length] : cycle[0];
        applySort(next === 'none' ? null : key, next);
      });
    });

    // Searching and the domain chips.
    var toolbar = document.querySelector('[data-pkg-toolbar]');
    var search = document.querySelector('[data-pkg-search]');
    var clear = document.querySelector('[data-pkg-clear]');
    var chips = all('[data-domain-filter]');
    var empty = document.querySelector('[data-pkg-empty]');
    var count = document.querySelector('[data-pkg-count]');
    var domain = '';

    function applyFilter() {
      var query = (search.value || '').trim().toLowerCase();
      var terms = query ? query.split(/\s+/) : [];
      var shown = 0;

      entries.forEach(function (entry) {
        var match = (!domain || entry.domain === domain) && terms.every(function (term) {
          return entry.text.indexOf(term) !== -1;
        });
        entry.row.hidden = !match;
        entry.detail.hidden = !match;
        if (match) shown += 1;
      });

      groups.forEach(function (group) {
        group.hidden = !!sortKey || !entries.some(function (entry) {
          return entry.group === group && !entry.row.hidden;
        });
      });

      clear.classList.toggle('cds--search-close--hidden', !query);
      empty.hidden = shown > 0;
      count.textContent = shown === entries.length
        ? entries.length + ' packages'
        : 'Showing ' + shown + ' of ' + entries.length + ' packages';
    }

    search.addEventListener('input', applyFilter);
    search.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { search.value = ''; applyFilter(); }
    });
    clear.addEventListener('click', function () {
      search.value = '';
      applyFilter();
      search.focus();
    });

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var value = chip.getAttribute('data-domain-filter');
        domain = domain === value ? '' : value;
        chips.forEach(function (other) {
          var on = other.getAttribute('data-domain-filter') === domain;
          other.classList.toggle('cds--tag--selectable-selected', on);
          other.setAttribute('aria-pressed', String(on));
        });
        applyFilter();
      });
    });

    toolbar.hidden = false;
    applyFilter();
  }

  // --- Shared hover readout -------------------------------------------------
  // Both plots hang their tooltip off `.site-plot`, which is the positioning
  // context — inside the heatmap's own scroll container it would be clipped.
  function showTip(plot, lines, rect) {
    var tip = plot.querySelector('[data-tip]');
    if (!tip) return;
    tip.textContent = '';
    lines.filter(Boolean).forEach(function (line, index) {
      tip.appendChild(el(index === 0 ? 'strong' : 'span', null, line));
    });
    tip.hidden = false;

    var box = plot.getBoundingClientRect();
    var centre = rect.left + rect.width / 2 - box.left;
    var above = rect.top - box.top - tip.offsetHeight - 8;
    tip.style.left = Math.round(Math.max(0, Math.min(box.width - tip.offsetWidth, centre - tip.offsetWidth / 2))) + 'px';
    tip.style.top = Math.round(above >= 0 ? above : rect.bottom - box.top + 8) + 'px';
  }

  function hideTip(plot) {
    var tip = plot.querySelector('[data-tip]');
    if (tip) tip.hidden = true;
  }

  // --- Release heatmap ------------------------------------------------------
  function initHeatmap() {
    var plot = document.querySelector('[data-heat]');
    if (!plot) return;
    var scroller = plot.querySelector('.site-heat__scroll');
    var cells = all('.site-heat__cell[data-n]', plot);
    if (!cells.length) return;

    function show(cell) {
      var releases = Number(cell.getAttribute('data-n'));
      cells.forEach(function (other) { other.classList.toggle('is-active', other === cell); });
      showTip(plot, [
        releases + (releases === 1 ? ' release' : ' releases'),
        'week of ' + day(cell.getAttribute('data-d')),
        cell.getAttribute('data-p')
      ], cell.getBoundingClientRect());
    }

    function clear() {
      cells.forEach(function (cell) { cell.classList.remove('is-active'); });
      hideTip(plot);
    }

    plot.addEventListener('pointerover', function (event) {
      var cell = event.target.closest('.site-heat__cell[data-n]');
      if (cell) show(cell);
    });
    plot.addEventListener('pointerleave', clear);

    // Roving tabindex: the grid is a single tab stop and the arrow keys walk
    // the weeks that actually have releases — ~80 of them, against 600-odd
    // squares that would otherwise all land in the tab order.
    var current = cells.length - 1;
    cells.forEach(function (cell, index) { cell.tabIndex = index === current ? 0 : -1; });

    function focusCell(index) {
      index = Math.max(0, Math.min(cells.length - 1, index));
      cells[current].tabIndex = -1;
      current = index;
      cells[current].tabIndex = 0;
      cells[current].focus();
    }

    plot.addEventListener('keydown', function (event) {
      var step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
      if (step) { event.preventDefault(); focusCell(current + step); return; }
      if (event.key === 'Home') { event.preventDefault(); focusCell(0); }
      if (event.key === 'End') { event.preventDefault(); focusCell(cells.length - 1); }
    });
    plot.addEventListener('focusin', function (event) {
      var cell = event.target.closest('.site-heat__cell[data-n]');
      if (!cell) return;
      current = cells.indexOf(cell);
      show(cell);
    });
    plot.addEventListener('focusout', function (event) {
      if (!plot.contains(event.relatedTarget)) clear();
    });

    // Open on the most recent weeks when the grid is wider than the viewport.
    if (scroller && scroller.scrollWidth > scroller.clientWidth) {
      var last = cells[cells.length - 1];
      scroller.scrollLeft = last.offsetLeft - scroller.clientWidth / 2;
    }
  }

  // --- Combined download chart ---------------------------------------------
  function initChart() {
    var plot = document.querySelector('[data-chart]');
    if (!plot) return;
    var values = (plot.getAttribute('data-values') || '').split(',').map(Number);
    var starts = (plot.getAttribute('data-starts') || '').split(',');
    if (values.length < 2 || values.length !== starts.length) return;

    var svg = plot.querySelector('.site-chart');
    var cursor = plot.querySelector('[data-chart-cursor]');
    var dot = plot.querySelector('[data-chart-dot]');
    var peak = Math.max.apply(null, values) || 1;
    var current = -1;

    function show(index, speak) {
      current = Math.max(0, Math.min(values.length - 1, index));
      var box = svg.getBoundingClientRect();
      var x = (current / (values.length - 1)) * box.width;
      var y = (1 - values[current] / peak) * box.height;
      var reading = num(values[current]) + ' downloads, week of ' + day(starts[current]);

      cursor.hidden = false;
      cursor.style.left = Math.round(x) + 'px';
      dot.hidden = false;
      dot.style.left = Math.round(x) + 'px';
      dot.style.top = Math.round(y) + 'px';
      showTip(plot, [
        num(values[current]) + ' downloads',
        'week of ' + day(starts[current])
      ], { left: box.left + x, right: box.left + x, width: 0, top: box.top + y, bottom: box.top + y });
      // The tooltip is decoration (aria-hidden, inside a role="img"), so
      // stepping by keyboard has to say the figure out loud itself. Pointer
      // moves stay silent — they would announce on every pixel.
      if (speak) announce(reading);
    }

    function hide() {
      current = -1;
      cursor.hidden = true;
      dot.hidden = true;
      hideTip(plot);
    }

    plot.addEventListener('pointermove', function (event) {
      var box = svg.getBoundingClientRect();
      show(Math.round(((event.clientX - box.left) / box.width) * (values.length - 1)));
    });
    plot.addEventListener('pointerleave', hide);

    // Keyboard: the plot becomes one tab stop that steps week by week. It
    // takes over the SVG's label so the reading is not announced twice.
    plot.tabIndex = 0;
    plot.setAttribute('role', 'img');
    plot.setAttribute('aria-label', svg.getAttribute('aria-label') + '. Use the arrow keys to step through the weeks.');
    plot.addEventListener('focus', function () { if (current < 0) show(values.length - 1, true); });
    plot.addEventListener('blur', hide);
    plot.addEventListener('keydown', function (event) {
      var step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
      if (!step) return;
      event.preventDefault();
      show((current < 0 ? values.length - 1 : current) + step, true);
    });
  }

  initCopyButtons();
  initSnippets();
  initTerminal();
  initOdometer();
  initCatalogue();
  initHeatmap();
  initChart();
})();
