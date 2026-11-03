"""Render WebDeck HTML from slide dicts + optional Chart.js configs."""

from __future__ import annotations

import json
from typing import Any

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>__DOC_TITLE__</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#0f172a;--slide:#ffffff;--accent:#2563eb;--muted:#64748b;--border:#e2e8f0}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--bg);font-family:system-ui,-apple-system,sans-serif;overflow:hidden}
.toolbar{position:fixed;top:0;left:0;right:0;z-index:20;display:flex;align-items:center;justify-content:space-between;padding:.45rem .85rem;background:rgba(15,23,42,.92);color:#e2e8f0;font-size:.78rem;backdrop-filter:blur(8px)}
.toolbar a{color:#93c5fd;margin-left:.65rem;text-decoration:none}
.toolbar button{background:#1e293b;border:1px solid #334155;color:#e2e8f0;border-radius:6px;padding:.3rem .65rem;cursor:pointer;font-size:.78rem}
.toolbar button:hover{background:#334155}
#progress{flex:1;max-width:200px;height:4px;background:#334155;border-radius:2px;margin:0 .75rem;overflow:hidden}
#progress>i{display:block;height:100%;background:var(--accent);width:0;transition:width .2s}
.stage{display:flex;align-items:center;justify-content:center;height:100vh;padding:2.5rem 1rem 3rem}
.slide{display:none;width:min(1120px,96vw);aspect-ratio:16/9;max-height:calc(100vh - 5rem);background:var(--slide);border-radius:12px;box-shadow:0 20px 50px rgba(0,0,0,.35);padding:1.4rem 1.6rem;overflow-y:auto;position:relative}
.slide.active{display:block}
.slide.cover{background:linear-gradient(145deg,#1e3a8a,#2563eb);color:#fff;display:none;align-items:center;justify-content:center;text-align:center}
.slide.cover.active{display:flex}
.slide.chapter{background:linear-gradient(145deg,#1e293b,#334155);color:#fff;display:none;align-items:center;justify-content:center;text-align:center}
.slide.chapter.active{display:flex}
.slide.chapter .cover-inner h1{font-size:1.65rem}
.slide.chapter .sec{font-size:.75rem;opacity:.85;margin-bottom:.5rem}
.slide-header{margin-bottom:.75rem;padding-bottom:.5rem;border-bottom:2px solid var(--border)}
.slide-header .sec{font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700}
.slide-header h2{margin:.15rem 0 0;font-size:1.25rem;line-height:1.25;color:#0f172a}
.cover-inner h1{font-size:2rem;margin:0 0 .5rem}
.cover .subtitle{font-size:1.05rem;opacity:.9;margin:0}
.cover .meta{margin-top:1.5rem;opacity:.75;font-size:.85rem}
.lead{font-size:.88rem;line-height:1.5;margin:.2rem 0 .6rem}
ul{margin:.35rem 0 .6rem;padding-left:1.2rem;font-size:.84rem;line-height:1.45}
li{margin:.15rem 0}
.note{font-size:.78rem;color:var(--muted);margin:.5rem 0 0}
.takeaway{margin-top:.65rem;padding:.55rem .75rem;background:#eff6ff;border-left:3px solid var(--accent);font-size:.82rem;color:#1e3a8a;border-radius:0 6px 6px 0}
.table-wrap{overflow-x:auto;margin:.4rem 0}
.data-table{width:100%;border-collapse:collapse;font-size:.74rem}
.data-table th,.data-table td{border:1px solid var(--border);padding:.28rem .4rem;text-align:left}
.data-table th{background:#f8fafc;font-weight:600}
.data-table.compact th,.data-table.compact td{padding:.2rem .35rem;font-size:.7rem}
.twocol{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:.4rem 0}
.twocol h3{margin:0 0 .35rem;font-size:.85rem;color:#1e40af}
.flow{display:flex;gap:.5rem;flex-wrap:wrap;margin:.5rem 0}
.flow-step{flex:1;min-width:120px;background:#f1f5f9;border:1px solid var(--border);border-radius:8px;padding:.55rem .6rem;font-size:.78rem;position:relative}
.flow-step span{display:inline-block;background:var(--accent);color:#fff;width:1.2rem;height:1.2rem;line-height:1.2rem;text-align:center;border-radius:50%;font-size:.7rem;margin-right:.35rem}
.math.display{margin:.6rem 0;text-align:center;font-size:.95rem;overflow-x:auto}
.chart-box{position:relative;height:200px;margin:.4rem 0}
.chart-box.tall{height:260px}
.figure-split .chart-box{height:180px;margin:0}
.figure{margin:.45rem 0;text-align:center}
.figure img{max-width:100%;width:auto;height:auto;object-fit:contain;border-radius:6px;border:1px solid var(--border)}
.figure figcaption,.figure-panel figcaption{font-size:.72rem;color:var(--muted);margin-top:.25rem;line-height:1.35}
.figure-row{display:flex;gap:.65rem;align-items:flex-start;justify-content:center;margin:.4rem 0}
.figure-panel{flex:1;min-width:0;text-align:center}
.figure-panel img{max-width:100%;width:auto;height:auto;object-fit:contain;border-radius:6px;border:1px solid var(--border)}
.figure-split{display:grid;grid-template-columns:1fr 1fr;gap:1rem;align-items:start;margin:.4rem 0}
.figure-split-3{grid-template-columns:1fr 1fr 1fr}
.figure-split-3 .chart-box{height:200px;margin:0}
.nav-hint{position:fixed;bottom:.5rem;left:50%;transform:translateX(-50%);color:#64748b;font-size:.72rem;z-index:20}
.deck-edit{border:none;background:transparent;color:inherit;font:inherit;line-height:inherit;padding:0;margin:0;outline:none;box-shadow:none;appearance:none;-webkit-appearance:none}
.deck-edit-line{width:100%;display:block}
.deck-edit-cell{width:100%;min-width:3rem;font-size:inherit}
.deck-edit-block{min-height:1em}
.deck-edit:focus,.deck-edit:focus-visible{background:rgba(37,99,235,.07);border-radius:3px}
.slide-header .deck-edit-line{font-size:inherit;font-weight:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit}
.slide-header h2{margin:.15rem 0 0}
.slide-header h2 .deck-edit-line{font-size:1.25rem;font-weight:700;line-height:1.25;color:#0f172a}
.slide.cover .deck-edit-block,.slide.chapter .deck-edit-block{color:inherit}
.slide.cover .deck-edit:focus,.slide.chapter .deck-edit:focus{background:rgba(255,255,255,.12)}
.toolbar .edit-tools{display:inline-flex;gap:.35rem;margin-right:.35rem}
.toolbar .edit-tools button{font-size:.72rem}
.toolbar .edit-tools button:disabled{opacity:.35;cursor:not-allowed}
.toolbar.editing-hint #edit-status{opacity:1}
#edit-status{opacity:.65;font-size:.72rem;margin-right:.5rem;white-space:nowrap}
.deck-move-target[data-positioned="1"]{position:absolute;z-index:2;box-sizing:border-box;min-width:48px;min-height:24px;touch-action:none}
.deck-move-target:not(.deck-text-editing){cursor:move;touch-action:none}
.deck-move-target:not(.deck-text-editing) .deck-edit-block,
.deck-move-target:not(.deck-text-editing) .deck-edit-cell,
.deck-move-target:not(.deck-text-editing) li .deck-edit-block{pointer-events:none;user-select:none}
.deck-move-target.deck-text-editing{cursor:text;z-index:20;touch-action:auto}
.deck-move-target.deck-text-editing .deck-edit{pointer-events:auto;user-select:text}
.deck-move-target.deck-dragging{cursor:grabbing!important;z-index:50!important;opacity:.94;box-shadow:0 10px 28px rgba(15,23,42,.16);touch-action:none}
body.deck-drag-active{user-select:none;cursor:grabbing}
.deck-handles{display:none;position:absolute;inset:-2px;pointer-events:none;border:2px solid #2563eb;z-index:6}
.deck-selected>.deck-handles{display:block}
.deck-handles i{position:absolute;width:8px;height:8px;background:#fff;border:2px solid #2563eb;border-radius:1px;pointer-events:auto;box-sizing:border-box;touch-action:none}
.deck-handles i[data-handle="nw"]{top:0;left:0;transform:translate(-50%,-50%);cursor:nwse-resize}
.deck-handles i[data-handle="n"]{top:0;left:50%;transform:translate(-50%,-50%);cursor:ns-resize}
.deck-handles i[data-handle="ne"]{top:0;left:100%;transform:translate(-50%,-50%);cursor:nesw-resize}
.deck-handles i[data-handle="e"]{top:50%;left:100%;transform:translate(-50%,-50%);cursor:ew-resize}
.deck-handles i[data-handle="se"]{top:100%;left:100%;transform:translate(-50%,-50%);cursor:nwse-resize}
.deck-handles i[data-handle="s"]{top:100%;left:50%;transform:translate(-50%,-50%);cursor:ns-resize}
.deck-handles i[data-handle="sw"]{top:100%;left:0;transform:translate(-50%,-50%);cursor:nesw-resize}
.deck-handles i[data-handle="w"]{top:50%;left:0;transform:translate(-50%,-50%);cursor:ew-resize}
.toolbar .align-tools{display:inline-flex;gap:.25rem;margin-right:.35rem;align-items:center}
.toolbar .align-tools[hidden]{display:none}
.toolbar .align-tools button{font-size:.68rem;padding:.22rem .45rem;min-width:1.6rem}
.toolbar .align-tools button:disabled{opacity:.35;cursor:not-allowed}
.toolbar .align-sep{display:inline-block;width:1px;height:1rem;background:#334155;margin:0 .15rem}
</style>
</head>
<body>
<div class="toolbar" id="toolbar">
  <span id="slide-label">1 / N</span>
  <div id="progress"><i id="progress-bar"></i></div>
  <div>
    __EDIT_TOOLS__
    <button id="prev">←</button>
    <button id="next">→</button>
    __NAV_LINKS__
  </div>
</div>
<div class="stage" id="stage"></div>
<p class="nav-hint">__NAV_HINT__</p>
<script>
const SLIDES = __SLIDES_JSON__;
const CHARTS = __CHARTS_JSON__;
const EDITABLE = __EDITABLE__;
let idx = 0;
const stage = document.getElementById('stage');
const built = {};
const STORAGE_KEY = 'webdeck-edits:' + location.pathname;

function escAttr(s) {
  return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
}

function slideContentHtml(s, i) {
  if (s.kind === 'cover' || s.kind === 'chapter') return s.body;
  const sec = EDITABLE
    ? `<input type="text" class="deck-edit deck-edit-line deck-move-target" data-edit-key="section" value="${escAttr(s.section)}"/>`
    : s.section;
  const title = EDITABLE
    ? `<input type="text" class="deck-edit deck-edit-line deck-move-target" data-edit-key="title" value="${escAttr(s.title)}"/>`
    : s.title;
  return `<div class="slide-header"><div class="sec">${sec}</div><h2>${title}</h2></div><div class="slide-body">${s.body}</div>`;
}

SLIDES.forEach((s, i) => {
  const el = document.createElement('section');
  el.className = 'slide' + (s.kind === 'cover' ? ' cover' : '') + (s.kind === 'chapter' ? ' chapter' : '') + (i === 0 ? ' active' : '');
  el.dataset.idx = i;
  el.innerHTML = slideContentHtml(s, i);
  stage.appendChild(el);
});

function editValue(el) {
  return el.matches('input, textarea, select') ? el.value : el.innerHTML;
}

function setEditValue(el, v) {
  if (el.matches('input, textarea, select')) el.value = v;
  else el.innerHTML = v;
}

const MOVE_SELECTORS = [
  '.deck-edit-block',
  '.slide-header .deck-edit-line',
  '.table-wrap',
  '.twocol',
  '.figure-split',
  'ul',
  '.flow',
  '.figure',
  '.chart-box',
].join(',');

function markMoveTargets() {
  document.querySelectorAll(MOVE_SELECTORS).forEach(el => {
    if (el.closest('td, th')) return;
    el.classList.add('deck-move-target');
  });
  document.querySelectorAll('.deck-move-target').forEach(el => {
    if (el.parentElement && el.parentElement.closest('.deck-move-target')) {
      el.classList.remove('deck-move-target');
    }
  });
}

function lockTextEdits() {
  document.querySelectorAll('.deck-edit-block[contenteditable]').forEach(el => {
    el.contentEditable = 'false';
  });
}

function positionParent(el) {
  return el.closest('.slide');
}

function readPosition(el) {
  if (el.dataset.positioned !== '1') return null;
  const z = parseInt(el.style.zIndex, 10);
  const h = parseFloat(el.style.height);
  return {
    positioned: true,
    x: parseFloat(el.style.left) || 0,
    y: parseFloat(el.style.top) || 0,
    w: parseFloat(el.style.width) || null,
    h: Number.isFinite(h) ? h : null,
    z: Number.isFinite(z) ? z : null,
  };
}

function applyStoredPosition(el, pos) {
  if (!pos || !pos.positioned) return;
  el.style.position = 'absolute';
  el.style.left = pos.x + 'px';
  el.style.top = pos.y + 'px';
  if (pos.w) {
    el.style.width = pos.w + 'px';
    el.style.maxWidth = pos.w + 'px';
  }
  if (pos.h) el.style.height = pos.h + 'px';
  if (pos.z != null) el.style.zIndex = String(pos.z);
  el.dataset.positioned = '1';
}

function ensurePositioned(el) {
  if (el.dataset.positioned === '1') return;
  const slide = positionParent(el);
  if (!slide) return;
  const sRect = slide.getBoundingClientRect();
  const rect = el.getBoundingClientRect();
  el.style.position = 'absolute';
  el.style.left = (rect.left - sRect.left + slide.scrollLeft) + 'px';
  el.style.top = (rect.top - sRect.top + slide.scrollTop) + 'px';
  el.style.width = rect.width + 'px';
  el.style.maxWidth = rect.width + 'px';
  if (!el.style.height && el.offsetHeight) el.style.height = el.offsetHeight + 'px';
  el.dataset.positioned = '1';
}

function prepareShape(el) {
  ensurePositioned(el);
  ensureHandles(el);
}

function packEdit(el) {
  const hasText = el.classList.contains('deck-edit');
  const text = hasText ? editValue(el) : null;
  const pos = readPosition(el);
  if (hasText && pos) return { text, ...pos };
  if (hasText) return text;
  if (pos) return pos;
  return null;
}

function unpackEdit(el, v) {
  if (v == null) return;
  if (typeof v === 'string') {
    if (el.classList.contains('deck-edit')) setEditValue(el, v);
    return;
  }
  if (v.text != null && el.classList.contains('deck-edit')) setEditValue(el, v.text);
  applyStoredPosition(el, v);
}

function assignStorageKeys() {
  document.querySelectorAll('.slide').forEach(slide => {
    const i = slide.dataset.idx;
    slide.querySelectorAll('[data-edit-key]').forEach(el => {
      if (!el.dataset.storageKey) {
        el.dataset.storageKey = `slide-${i}-${el.dataset.editKey}`;
      }
    });
  });
  let n = 0;
  document.querySelectorAll('.slide-body .deck-edit:not([data-storage-key])').forEach(el => {
    el.dataset.storageKey = `body-${n++}`;
  });
  let m = 0;
  document.querySelectorAll('.deck-move-target:not([data-storage-key])').forEach(el => {
    el.dataset.storageKey = `move-${m++}`;
  });
}

function loadEdits() {
  if (!EDITABLE) return;
  let raw;
  try { raw = localStorage.getItem(STORAGE_KEY); } catch (e) { return; }
  if (!raw) return;
  let data;
  try { data = JSON.parse(raw); } catch (e) { return; }
  const seen = new Set();
  document.querySelectorAll('.deck-edit[data-storage-key], .deck-move-target[data-storage-key]').forEach(el => {
    const k = el.dataset.storageKey;
    if (seen.has(k)) return;
    seen.add(k);
    unpackEdit(el, data[k]);
  });
}

function collectEdits() {
  const data = {};
  const seen = new Set();
  document.querySelectorAll('.deck-edit[data-storage-key], .deck-move-target[data-storage-key]').forEach(el => {
    const k = el.dataset.storageKey;
    if (seen.has(k)) return;
    seen.add(k);
    const packed = packEdit(el);
    if (packed != null) data[k] = packed;
  });
  return data;
}

function saveEdits() {
  if (!EDITABLE) return;
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(collectEdits())); } catch (e) {}
}

const MAX_HISTORY = 100;
let history = [];
let historyIdx = -1;
let historyTimer = null;
let historyPaused = false;

function resetShapeLayout(el) {
  el.style.position = '';
  el.style.left = '';
  el.style.top = '';
  el.style.width = '';
  el.style.maxWidth = '';
  el.style.height = '';
  el.style.zIndex = '';
  delete el.dataset.positioned;
  el.classList.remove('deck-selected', 'deck-dragging', 'deck-text-editing');
  el.querySelector(':scope > .deck-handles')?.remove();
}

function applySnapshot(json) {
  historyPaused = true;
  const data = JSON.parse(json);
  document.querySelectorAll('.deck-edit[data-storage-key], .deck-move-target[data-storage-key]').forEach(el => {
    resetShapeLayout(el);
    const k = el.dataset.storageKey;
    if (data[k] !== undefined) unpackEdit(el, data[k]);
  });
  lockTextEdits();
  document.querySelectorAll('.deck-edit-line').forEach(inp => { inp.readOnly = true; });
  textEditing = null;
  selected.clear();
  updateAlignToolbar();
  saveEdits();
  historyPaused = false;
}

function initHistory() {
  history = [JSON.stringify(collectEdits())];
  historyIdx = 0;
  updateUndoButtons();
}

function updateUndoButtons() {
  const u = document.getElementById('undo-edit');
  const r = document.getElementById('redo-edit');
  if (u) u.disabled = historyIdx <= 0;
  if (r) r.disabled = historyIdx >= history.length - 1;
}

function commitHistory() {
  if (!EDITABLE || historyPaused) return;
  const cur = JSON.stringify(collectEdits());
  if (history[historyIdx] === cur) {
    saveEdits();
    updateUndoButtons();
    return;
  }
  history = history.slice(0, historyIdx + 1);
  history.push(cur);
  if (history.length > MAX_HISTORY) {
    history.shift();
  } else {
    historyIdx++;
  }
  saveEdits();
  updateUndoButtons();
}

function scheduleHistoryCommit() {
  clearTimeout(historyTimer);
  historyTimer = setTimeout(commitHistory, 450);
}

function undoEdit() {
  if (historyIdx <= 0) return;
  historyIdx--;
  applySnapshot(history[historyIdx]);
  updateUndoButtons();
}

function redoEdit() {
  if (historyIdx >= history.length - 1) return;
  historyIdx++;
  applySnapshot(history[historyIdx]);
  updateUndoButtons();
}

let saveTimer;
function scheduleSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveEdits, 250);
}

function bindEditable() {
  if (!EDITABLE) return;
  markMoveTargets();
  assignStorageKeys();
  loadEdits();
  initHistory();
  lockTextEdits();
  document.querySelectorAll('.deck-edit').forEach(el => {
    el.addEventListener('input', scheduleHistoryCommit);
    el.addEventListener('blur', () => { clearTimeout(historyTimer); commitHistory(); });
  });
  bindLayoutEditor();
}

const selected = new Set();
let drag = null;
let resize = null;
let textEditing = null;
let pointerDrag = null;
const HANDLES = ['nw','n','ne','e','se','s','sw','w'];
const DRAG_THRESHOLD = 2;

function getActiveSlide() {
  return document.querySelector('.slide.active');
}

function clearSelection() {
  exitTextEdit();
  selected.forEach(el => {
    el.classList.remove('deck-selected');
    el.querySelector(':scope > .deck-handles')?.remove();
  });
  selected.clear();
  updateAlignToolbar();
}

function ensureHandles(el) {
  if (el.querySelector(':scope > .deck-handles')) return;
  const box = document.createElement('div');
  box.className = 'deck-handles';
  HANDLES.forEach(h => {
    const i = document.createElement('i');
    i.dataset.handle = h;
    box.appendChild(i);
  });
  el.appendChild(box);
}

function refreshSelectionChrome() {
  selected.forEach(el => {
    if (selected.has(el)) ensureHandles(el);
  });
}

function updateAlignToolbar() {
  const bar = document.getElementById('align-tools');
  if (!bar) return;
  const slide = getActiveSlide();
  const n = [...selected].filter(el => slide && slide.contains(el)).length;
  bar.hidden = n === 0;
  bar.querySelectorAll('[data-align]').forEach(btn => {
    const mode = btn.dataset.align;
    if (mode === 'dist-h' || mode === 'dist-v') btn.disabled = n < 3;
    else if (mode === 'front' || mode === 'back') btn.disabled = n < 1;
    else btn.disabled = n < 2;
  });
  const status = document.getElementById('edit-status');
  if (status) {
    if (textEditing) status.textContent = '编辑文字 · Esc 结束';
    else if (n > 1) status.textContent = `已选 ${n} 项 · 拖动移动 · 方向键微调`;
    else if (n === 1) status.textContent = '拖动移动 · 双击编辑 · 拖锚点缩放';
    else status.textContent = '单击选中 · 拖动移动 · 双击编辑';
  }
}

function selectOne(el) {
  clearSelection();
  selected.add(el);
  el.classList.add('deck-selected');
  prepareShape(el);
  updateAlignToolbar();
}

function toggleSelect(el) {
  if (selected.has(el)) {
    selected.delete(el);
    el.classList.remove('deck-selected');
    el.querySelector(':scope > .deck-handles')?.remove();
  } else {
    selected.add(el);
    el.classList.add('deck-selected');
    prepareShape(el);
  }
  updateAlignToolbar();
}

function exitTextEdit() {
  if (!textEditing) return;
  textEditing.classList.remove('deck-text-editing');
  textEditing.querySelectorAll('.deck-edit-block[contenteditable]').forEach(ed => {
    ed.contentEditable = 'false';
  });
  textEditing.querySelectorAll('.deck-edit-line').forEach(inp => { inp.readOnly = true; });
  textEditing = null;
  updateAlignToolbar();
}

function enterTextEdit(el) {
  exitTextEdit();
  ensurePositioned(el);
  textEditing = el;
  el.classList.add('deck-text-editing');
  el.querySelectorAll('.deck-edit-block').forEach(ed => { ed.contentEditable = 'true'; });
  el.querySelectorAll('.deck-edit-line').forEach(inp => { inp.readOnly = false; });
  const focusEl = el.querySelector('.deck-edit-block') || el.querySelector('.deck-edit-line');
  if (focusEl) {
    focusEl.focus();
    if (focusEl.matches('[contenteditable="true"]')) {
      const r = document.createRange();
      r.selectNodeContents(focusEl);
      r.collapse(false);
      const s = window.getSelection();
      s.removeAllRanges();
      s.addRange(r);
    }
  }
  updateAlignToolbar();
}

function itemRect(el) {
  ensurePositioned(el);
  const left = parseFloat(el.style.left) || 0;
  const top = parseFloat(el.style.top) || 0;
  const width = el.offsetWidth;
  const height = el.offsetHeight;
  return { el, left, top, width, height,
    right: left + width, bottom: top + height,
    cx: left + width / 2, cy: top + height / 2 };
}

function selectedOnSlide() {
  const slide = getActiveSlide();
  return [...selected].filter(el => slide && slide.contains(el));
}

function alignSelected(mode) {
  const items = selectedOnSlide();
  if (!items.length) return;
  const rects = items.map(itemRect);

  if (mode === 'left') {
    const v = Math.min(...rects.map(r => r.left));
    rects.forEach(r => { r.el.style.left = v + 'px'; });
  } else if (mode === 'right') {
    const v = Math.max(...rects.map(r => r.right));
    rects.forEach(r => { r.el.style.left = (v - r.width) + 'px'; });
  } else if (mode === 'center-h') {
    const min = Math.min(...rects.map(r => r.left));
    const max = Math.max(...rects.map(r => r.right));
    const mid = (min + max) / 2;
    rects.forEach(r => { r.el.style.left = (mid - r.width / 2) + 'px'; });
  } else if (mode === 'top') {
    const v = Math.min(...rects.map(r => r.top));
    rects.forEach(r => { r.el.style.top = v + 'px'; });
  } else if (mode === 'bottom') {
    const v = Math.max(...rects.map(r => r.bottom));
    rects.forEach(r => { r.el.style.top = (v - r.height) + 'px'; });
  } else if (mode === 'center-v') {
    const min = Math.min(...rects.map(r => r.top));
    const max = Math.max(...rects.map(r => r.bottom));
    const mid = (min + max) / 2;
    rects.forEach(r => { r.el.style.top = (mid - r.height / 2) + 'px'; });
  } else if (mode === 'dist-h' && rects.length >= 3) {
    rects.sort((a, b) => a.left - b.left);
    const totalW = rects.reduce((s, r) => s + r.width, 0);
    const span = rects[rects.length - 1].right - rects[0].left;
    const gap = (span - totalW) / (rects.length - 1);
    let x = rects[0].left;
    rects.forEach(r => { r.el.style.left = x + 'px'; x += r.width + gap; });
  } else if (mode === 'dist-v' && rects.length >= 3) {
    rects.sort((a, b) => a.top - b.top);
    const totalH = rects.reduce((s, r) => s + r.height, 0);
    const span = rects[rects.length - 1].bottom - rects[0].top;
    const gap = (span - totalH) / (rects.length - 1);
    let y = rects[0].top;
    rects.forEach(r => { r.el.style.top = y + 'px'; y += r.height + gap; });
  } else if (mode === 'front') {
    const maxZ = Math.max(2, ...items.map(el => parseInt(el.style.zIndex, 10) || 2));
    items.forEach(el => { el.style.zIndex = String(maxZ + 1); });
  } else if (mode === 'back') {
    items.forEach(el => { el.style.zIndex = '1'; });
  } else return;
  commitHistory();
}

function nudgeSelected(key, step) {
  selectedOnSlide().forEach(el => {
    ensurePositioned(el);
    const l = parseFloat(el.style.left) || 0;
    const t = parseFloat(el.style.top) || 0;
    if (key === 'ArrowLeft') el.style.left = (l - step) + 'px';
    if (key === 'ArrowRight') el.style.left = (l + step) + 'px';
    if (key === 'ArrowUp') el.style.top = (t - step) + 'px';
    if (key === 'ArrowDown') el.style.top = (t + step) + 'px';
  });
  commitHistory();
}

function beginDrag(items, clientX, clientY) {
  items.forEach(prepareShape);
  drag = {
    items: items.map(el => ({
      el,
      left: parseFloat(el.style.left) || 0,
      top: parseFloat(el.style.top) || 0,
    })),
    startX: clientX,
    startY: clientY,
    moved: false,
  };
  items.forEach(el => el.classList.add('deck-dragging'));
  document.body.classList.add('deck-drag-active');
}

function endDrag(save) {
  if (!drag) return;
  drag.items.forEach(it => it.el.classList.remove('deck-dragging'));
  if (save && drag.moved) commitHistory();
  else saveEdits();
  drag = null;
  document.body.classList.remove('deck-drag-active');
}

function startResize(el, handle, e) {
  prepareShape(el);
  resize = {
    el, handle,
    startX: e.clientX,
    startY: e.clientY,
    left: parseFloat(el.style.left) || 0,
    top: parseFloat(el.style.top) || 0,
    width: el.offsetWidth,
    height: el.offsetHeight,
  };
}

function applyResize(e) {
  if (!resize) return;
  const dx = e.clientX - resize.startX;
  const dy = e.clientY - resize.startY;
  const minW = 48, minH = 24;
  let left = resize.left;
  let top = resize.top;
  let width = resize.width;
  let height = resize.height;
  const h = resize.handle;
  if (h.includes('e')) width = Math.max(minW, resize.width + dx);
  if (h.includes('s')) height = Math.max(minH, resize.height + dy);
  if (h.includes('w')) {
    width = Math.max(minW, resize.width - dx);
    left = resize.left + (resize.width - width);
  }
  if (h.includes('n')) {
    height = Math.max(minH, resize.height - dy);
    top = resize.top + (resize.height - height);
  }
  resize.el.style.left = left + 'px';
  resize.el.style.top = top + 'px';
  resize.el.style.width = width + 'px';
  resize.el.style.maxWidth = width + 'px';
  resize.el.style.height = height + 'px';
}

function bindLayoutEditor() {
  document.querySelectorAll('.deck-edit-line').forEach(inp => { inp.readOnly = true; });

  document.addEventListener('pointerdown', e => {
    if (!EDITABLE || e.button !== 0) return;
    if (e.target.closest('.toolbar')) return;

    const handleEl = e.target.closest('[data-handle]');
    if (handleEl) {
      const shape = handleEl.closest('.deck-move-target');
      if (shape) {
        if (!selected.has(shape)) selectOne(shape);
        startResize(shape, handleEl.dataset.handle, e);
        shape.setPointerCapture(e.pointerId);
        pointerDrag = { kind: 'resize', id: e.pointerId };
      }
      e.preventDefault();
      return;
    }

    const slide = getActiveSlide();
    const target = e.target.closest('.deck-move-target');
    const multi = e.ctrlKey || e.metaKey || e.shiftKey;

    if (target && slide && slide.contains(target)) {
      if (textEditing === target) return;

      if (multi) {
        toggleSelect(target);
      } else if (!selected.has(target)) {
        selectOne(target);
      }

      if (textEditing && textEditing !== target) exitTextEdit();

      pointerDrag = {
        kind: 'move',
        id: e.pointerId,
        originX: e.clientX,
        originY: e.clientY,
        captureEl: target,
        started: false,
      };
      target.setPointerCapture(e.pointerId);
      e.preventDefault();
      return;
    }

    if (slide && slide.contains(e.target)) {
      exitTextEdit();
      clearSelection();
    }
  });

  document.addEventListener('pointermove', e => {
    if (resize && pointerDrag?.kind === 'resize') {
      applyResize(e);
      return;
    }
    if (pointerDrag?.kind === 'move' && !drag) {
      const dx = e.clientX - pointerDrag.originX;
      const dy = e.clientY - pointerDrag.originY;
      if (!pointerDrag.started && Math.hypot(dx, dy) >= DRAG_THRESHOLD) {
        const items = selectedOnSlide();
        if (items.length) {
          beginDrag(items, e.clientX, e.clientY);
          pointerDrag.started = true;
        }
      }
    }
    if (!drag) return;
    drag.moved = true;
    const dx = e.clientX - drag.startX;
    const dy = e.clientY - drag.startY;
    drag.items.forEach(it => {
      it.el.style.left = (it.left + dx) + 'px';
      it.el.style.top = (it.top + dy) + 'px';
    });
  });

  document.addEventListener('pointerup', e => {
    if (pointerDrag?.captureEl?.hasPointerCapture?.(e.pointerId)) {
      pointerDrag.captureEl.releasePointerCapture(e.pointerId);
    }
    if (resize) {
      commitHistory();
      resize = null;
    }
    endDrag(true);
    pointerDrag = null;
  });

  document.addEventListener('pointercancel', e => {
    if (pointerDrag?.captureEl?.hasPointerCapture?.(e.pointerId)) {
      pointerDrag.captureEl.releasePointerCapture(e.pointerId);
    }
    endDrag(false);
    resize = null;
    pointerDrag = null;
  });

  document.addEventListener('dblclick', e => {
    if (!EDITABLE) return;
    const target = e.target.closest('.deck-move-target');
    const slide = getActiveSlide();
    if (target && slide && slide.contains(target)) {
      e.preventDefault();
      if (!selected.has(target)) selectOne(target);
      enterTextEdit(target);
    }
  });

  document.getElementById('align-tools')?.addEventListener('click', e => {
    const btn = e.target.closest('[data-align]');
    if (!btn || btn.disabled) return;
    alignSelected(btn.dataset.align);
  });

  document.addEventListener('keydown', e => {
    if (!EDITABLE) return;

    const mod = e.ctrlKey || e.metaKey;
    if (mod && e.key === 'z' && !e.shiftKey) {
      e.preventDefault();
      if (textEditing && document.queryCommandEnabled?.('undo')) {
        document.execCommand('undo');
      } else {
        undoEdit();
      }
      return;
    }
    if (mod && (e.key === 'y' || (e.key === 'z' && e.shiftKey) || (e.key === 'Z' && e.shiftKey))) {
      e.preventDefault();
      if (textEditing && document.queryCommandEnabled?.('redo')) {
        document.execCommand('redo');
      } else {
        redoEdit();
      }
      return;
    }

    if (e.key === 'Escape') {
      if (textEditing) { exitTextEdit(); e.preventDefault(); }
      return;
    }
    if (textEditing || e.target.closest('.deck-text-editing')) return;

    const items = selectedOnSlide();
    const step = e.shiftKey ? 10 : 1;
    if (items.length && ['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) {
      if (e.ctrlKey || e.metaKey) {
        const map = { ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'top', ArrowDown: 'bottom' };
        if (e.shiftKey) {
          e.preventDefault();
          alignSelected(e.key === 'ArrowLeft' || e.key === 'ArrowRight' ? 'center-h' : 'center-v');
        } else if (items.length >= 2 && map[e.key]) {
          e.preventDefault();
          alignSelected(map[e.key]);
        }
      } else {
        e.preventDefault();
        nudgeSelected(e.key, step);
      }
      return;
    }
  });
}

function exportEdits() {
  const blob = new Blob([JSON.stringify(collectEdits(), null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'deck-edits.json';
  a.click();
  URL.revokeObjectURL(a.href);
}

function resetEdits() {
  if (!confirm('清除本地已保存的文案与布局修改？')) return;
  try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
  location.reload();
}

if (EDITABLE) {
  document.getElementById('export-edits')?.addEventListener('click', exportEdits);
  document.getElementById('reset-edits')?.addEventListener('click', resetEdits);
  document.getElementById('undo-edit')?.addEventListener('click', undoEdit);
  document.getElementById('redo-edit')?.addEventListener('click', redoEdit);
  bindEditable();
}

function renderMath() {
  if (window.renderMathInElement) {
    renderMathInElement(document.querySelector('.slide.active'), {
      delimiters: [{left:'\\(',right:'\\)',display:false},{left:'\\[',right:'\\]',display:true}],
      throwOnError: false
    });
  }
}

function buildChart(id, cfg) {
  if (built[id]) return;
  const canvas = document.getElementById(id);
  if (!canvas || !cfg) return;
  built[id] = new Chart(canvas, cfg);
}

function onSlide(i) {
  idx = Math.max(0, Math.min(SLIDES.length - 1, i));
  clearSelection();
  document.querySelectorAll('.slide').forEach((el, j) => el.classList.toggle('active', j === idx));
  const status = document.getElementById('edit-status');
  if (status) status.textContent = '单击选中文本框 · 双击编辑 · 拖锚点缩放';
  document.getElementById('slide-label').textContent = `${idx + 1} / ${SLIDES.length}` + (SLIDES[idx].title ? ' · ' + SLIDES[idx].title : '');
  document.getElementById('progress-bar').style.width = ((idx + 1) / SLIDES.length * 100) + '%';
  renderMath();
  const active = document.querySelector('.slide.active');
  if (active) {
    active.querySelectorAll('canvas[id]').forEach(canvas => {
      if (CHARTS[canvas.id]) buildChart(canvas.id, CHARTS[canvas.id]);
    });
  }
}

document.getElementById('prev').onclick = () => onSlide(idx - 1);
document.getElementById('next').onclick = () => onSlide(idx + 1);
document.addEventListener('keydown', e => {
  if (textEditing || e.target.closest('.deck-text-editing')) {
    if (['PageUp','PageDown',' '].includes(e.key) && !e.target.closest('.deck-edit-block')) {
      /* allow typing space in contenteditable */
    }
    if (e.key === 'Escape') return;
    if (textEditing && ['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) return;
    if (textEditing && e.key === ' ') return;
    if (e.target.closest('.deck-edit')) {
      if (['PageUp','PageDown'].includes(e.key)) e.stopPropagation();
      return;
    }
  }
  if (drag || pointerDrag?.started || resize) return;
  if (selectedOnSlide().length && ['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) return;
  if ((e.ctrlKey || e.metaKey) && ['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) return;
  if (e.key === 'ArrowLeft' || e.key === 'PageUp') onSlide(idx - 1);
  if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); onSlide(idx + 1); }
  if (e.key === 'f' || e.key === 'F') document.documentElement.requestFullscreen?.();
});
onSlide(0);
</script>
</body>
</html>
"""


def _nav_links_html(links: list[tuple[str, str]]) -> str:
    if not links:
        return ""
    return "".join(f'<a href="{href}">{label}</a>' for label, href in links)


def _edit_tools_html(editable: bool) -> str:
    if not editable:
        return ""
    return (
        '<span id="edit-status">单击选中文本框 · 双击编辑 · 拖锚点缩放</span>'
        '<span class="align-tools" id="align-tools" hidden>'
        '<button type="button" data-align="left" title="左对齐">左</button>'
        '<button type="button" data-align="center-h" title="水平居中">中</button>'
        '<button type="button" data-align="right" title="右对齐">右</button>'
        '<span class="align-sep"></span>'
        '<button type="button" data-align="top" title="顶对齐">上</button>'
        '<button type="button" data-align="center-v" title="垂直居中">中</button>'
        '<button type="button" data-align="bottom" title="底对齐">下</button>'
        '<span class="align-sep"></span>'
        '<button type="button" data-align="dist-h" title="横向均分">均H</button>'
        '<button type="button" data-align="dist-v" title="纵向均分">均V</button>'
        '<span class="align-sep"></span>'
        '<button type="button" data-align="front" title="置顶">↑层</button>'
        '<button type="button" data-align="back" title="置底">↓层</button>'
        '</span>'
        '<span class="edit-tools">'
        '<button type="button" id="undo-edit" title="Ctrl+Z">撤销</button>'
        '<button type="button" id="redo-edit" title="Ctrl+Y">重做</button>'
        '<button type="button" id="export-edits">导出</button>'
        '<button type="button" id="reset-edits">重置</button>'
        "</span>"
    )


def render_deck_html(
    *,
    document_title: str,
    slides: list[dict[str, Any]],
    charts: dict[str, Any],
    nav_links: list[tuple[str, str]] | None = None,
    editable: bool = True,
) -> str:
    slides_json = json.dumps(slides, ensure_ascii=False)
    charts_json = json.dumps(charts, ensure_ascii=False)
    nav_hint = "← → 翻页(未选中) · 拖动/缩放 · 双击编辑 · Ctrl+Z/Y 撤销重做" if editable else "← → 翻页 · F 全屏"
    return (
        HTML_TEMPLATE.replace("__DOC_TITLE__", document_title)
        .replace("__NAV_LINKS__", _nav_links_html(nav_links or []))
        .replace("__EDIT_TOOLS__", _edit_tools_html(editable))
        .replace("__NAV_HINT__", nav_hint)
        .replace("__SLIDES_JSON__", slides_json)
        .replace("__CHARTS_JSON__", charts_json)
        .replace("__EDITABLE__", "true" if editable else "false")
    )
