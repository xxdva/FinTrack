// FinTrack — интерактивность интерфейса (без бэкенда)
(function () {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  function showToast(text) {
    const toast = $('[data-toast-el]');
    if (!toast) return;
    toast.textContent = text;
    toast.classList.add('is-visible');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove('is-visible'), 2500);
  }

  // Переключатель Расход / Доход
  $$('[data-toggle]').forEach((group) => {
    const hidden = group.parentElement.querySelector('input[type=hidden]');
    group.addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-value]');
      if (!btn) return;
      $$('button', group).forEach((b) => {
        const active = b === btn;
        b.classList.remove('btn--expense', 'btn--income', 'btn--outline');
        if (!active) b.classList.add('btn--outline');
        else b.classList.add(b.dataset.value === 'Доход' ? 'btn--income' : 'btn--expense');
      });
      hidden.value = btn.dataset.value;
    });
  });

  // Форма операции: валидация суммы, сохранение, очистка, горячие клавиши
  const form = $('#operation-form');
  if (form) {
    const amount = $('[data-amount]', form);
    const hint = $('[data-hint]', form);

    const isValid = () => {
      const value = Number(amount.value.replace(/\s/g, '').replace(',', '.'));
      const ok = amount.value.trim() !== '' && value > 0;
      amount.style.borderColor = ok ? '' : 'var(--expense)';
      if (hint) hint.style.color = ok ? '' : 'var(--expense)';
      return ok;
    };

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (isValid()) showToast(form.dataset.toast);
    });
    amount.addEventListener('input', isValid);

    const clear = $('[data-clear]', form);
    if (clear) {
      clear.addEventListener('click', () => {
        $$('input:not([type=hidden])', form).forEach((i) => (i.value = ''));
        amount.style.borderColor = '';
        if (hint) hint.style.color = '';
      });
    }

    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {
        e.preventDefault();
        form.requestSubmit();
      }
      if (e.key === 'Escape') window.history.back();
    });
  }

  // Быстрые категории
  $$('[data-quick-category]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const select = $('select[name=category]');
      if (select) select.value = btn.dataset.quickCategory;
    });
  });

  // Переключатель «Повторять платёж»
  const sw = $('[data-switch]');
  if (sw) {
    const label = $('[data-switch-label]', sw);
    sw.addEventListener('click', () => {
      const on = $('.switch', sw).classList.toggle('is-on');
      label.textContent = 'Повторять платёж: ' + (on ? 'ежемесячно' : 'не повторять');
    });
  }

  // Диалог удаления
  const dialog = $('[data-dialog]');
  if (dialog) {
    $('[data-open-dialog]').addEventListener('click', () => (dialog.hidden = false));
    $('[data-close-dialog]').addEventListener('click', () => (dialog.hidden = true));
  }

  // Таблица операций: выбор строки, фильтры, сортировка, удаление
  const table = $('[data-table]');
  if (table) {
    const rows = () => $$('.table__row', table);
    const editLink = $('[data-edit-link]');
    const summary = $('[data-summary]');
    const fmt = (n) => n.toLocaleString('ru-RU').replace(/ /g, ' ');
    const num = (s) => Number(s.replace(/[^\d-]/g, ''));

    const updateSummary = () => {
      const visible = rows().filter((r) => !r.hidden);
      let inc = 0, exp = 0;
      visible.forEach((r) => {
        const v = num(r.dataset.amount);
        if (v > 0) inc += v; else exp += v;
      });
      summary.textContent =
        `Найдено операций: ${visible.length}   |   Доходы: +${fmt(inc)} ₸   |   Расходы: ${exp ? '-' + fmt(-exp) : '0'} ₸`;
    };

    table.addEventListener('click', (e) => {
      const row = e.target.closest('.table__row');
      if (!row) return;
      rows().forEach((r) => r.classList.toggle('is-selected', r === row));
      editLink.href = `/operations/${row.dataset.id}/edit`;
    });
    table.addEventListener('dblclick', (e) => {
      const row = e.target.closest('.table__row');
      if (row) window.location.href = `/operations/${row.dataset.id}/edit`;
    });

    $('[data-delete-selected]').addEventListener('click', () => {
      const selected = $('.table__row.is-selected', table);
      if (selected && confirm('Удалить операцию? Действие нельзя отменить.')) {
        selected.remove();
        updateSummary();
      }
    });

    const filters = $('#filters');
    filters.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = filters.q.value.trim().toLowerCase();
      const type = filters.type.value;
      const category = filters.category.value;
      rows().forEach((r) => {
        r.hidden =
          (q && !r.dataset.comment.toLowerCase().includes(q)) ||
          (type && r.dataset.type !== type) ||
          (category && r.dataset.category !== category);
      });
      updateSummary();
    });
    filters.addEventListener('reset', () => {
      setTimeout(() => {
        rows().forEach((r) => (r.hidden = false));
        updateSummary();
      });
    });

    let asc = false;
    $('[data-sort]').addEventListener('click', (e) => {
      asc = !asc;
      const key = (r) => r.children[0].textContent.split('.').reverse().join('');
      rows()
        .sort((a, b) => (asc ? 1 : -1) * key(a).localeCompare(key(b)))
        .forEach((r) => table.appendChild(r));
      e.currentTarget.textContent = 'Сортировка: дата ' + (asc ? '▴' : '▾');
    });
  }
})();
