import { useEffect, useRef, type RefObject } from "react";
import { detectGamepadProfile } from "../adapters/gamepadProfiles";

export type MenuDevice = { kind: "pointer" | "keyboard" | "pad"; confirm: string; back: string };
let device: MenuDevice = { kind: "pointer", confirm: "▼", back: "▶" };
export const menuDevice = () => device;
const surfaceMemory = new Map<string, { label: string; scroll: number[] }>();
const publishDevice = (next: MenuDevice) => {
  if (JSON.stringify(device) === JSON.stringify(next)) return;
  device = next;
  document.documentElement.dataset.menuDevice = next.kind;
  window.dispatchEvent(new Event("menu-device"));
};
const identity = (el: HTMLElement) => el.getAttribute("aria-label") || el.querySelector(".menu-action-label")?.textContent || el.textContent || "";
const controls = (root: HTMLElement) => [...root.querySelectorAll<HTMLElement>('button:not(:disabled),input:not(:disabled),select:not(:disabled),textarea:not(:disabled),a[href],[data-menu-scroll-area]')].filter(el => (!el.hasAttribute('data-menu-scroll-area') || el.scrollHeight > el.clientHeight + 1) && el.getClientRects().length && el.closest('[data-menu-surface]') === root);
export const textControl = (el: Element | null): el is HTMLInputElement | HTMLTextAreaElement => el instanceof HTMLTextAreaElement || el instanceof HTMLInputElement && !["range", "checkbox", "radio", "button", "submit"].includes(el.type);

export function useMenuNavigation(ref: RefObject<HTMLElement | null>, key: string, back?: () => void) {
  const saved = useRef(surfaceMemory);
  useEffect(() => {
    const root = ref.current;
    if (!root) return;
    const previous = document.activeElement;
    const active = () => {
      const modal = [...document.querySelectorAll<HTMLElement>('[aria-modal="true"][data-menu-surface]')].at(-1);
      return modal ? modal === root : root.isConnected && !document.querySelector('[aria-modal="true"]');
    };
    const reveal = (el: HTMLElement) => {
      el.focus({ preventScroll: true });
      const container = el.closest<HTMLElement>('.menu-scroll,.settings-grid,.menu-dialog-content,.network-room-list');
      if (container) {
        const item = el.getBoundingClientRect(), bounds = container.getBoundingClientRect();
        if (item.top < bounds.top) container.scrollTop -= bounds.top - item.top + 12;
        else if (item.bottom > bounds.bottom) container.scrollTop += item.bottom - bounds.bottom + 12;
      }
    };
    const scrollArea = (delta: number) => {
      const el = document.activeElement;
      if (!(el instanceof HTMLElement) || !el.hasAttribute('data-menu-scroll-area')) return false;
      const before = el.scrollTop; el.scrollTop += delta * 80;
      return before !== el.scrollTop;
    };
    const move = (delta: number) => {
      const items = controls(root), i = items.indexOf(document.activeElement as HTMLElement);
      const next = items[(i + delta + items.length) % items.length];
      if (next) reveal(next);
    };
    const adjust = (delta: number) => {
      const el = document.activeElement;
      if (el instanceof HTMLInputElement && el.type === 'range') {
        if (delta > 0) el.stepUp(); else el.stepDown();
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
      }
      if (el instanceof HTMLSelectElement) {
        const options = [...el.options].filter(option => !option.disabled);
        const index = options.findIndex(option => option.value === el.value);
        el.value = options[Math.max(0, Math.min(options.length - 1, index + delta))]?.value ?? el.value;
        el.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
      }
      return false;
    };
    const memory = saved.current.get(key);
    const first = controls(root).find(el => identity(el) === memory?.label) ?? controls(root).find(el => !el.hasAttribute("data-menu-scroll-area")) ?? controls(root)[0];
    if (memory) [...root.querySelectorAll<HTMLElement>(".menu-scroll,.settings-grid,.menu-dialog-content")].forEach((el,i) => { el.scrollTop = memory.scroll[i] ?? 0; });
    if (active() && first) reveal(first);
    let editing: HTMLElement | null = null;
    const keydown = (event: KeyboardEvent) => {
      if (!active()) return;
      publishDevice({ ...device, kind: 'keyboard' });
      const text = textControl(document.activeElement);
      const arrow = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.code);
      if (text) {
        if (editing === document.activeElement) {
          if (event.code === 'Escape') { event.preventDefault(); event.stopImmediatePropagation(); editing = null; }
          return;
        }
        if (event.code === 'Enter') { event.preventDefault(); event.stopImmediatePropagation(); editing = document.activeElement as HTMLElement; return; }
        if (!arrow && !['Escape','Tab'].includes(event.code)) { editing = document.activeElement as HTMLElement; return; }
      }
      if (arrow) {
        event.preventDefault(); event.stopImmediatePropagation();
        const delta = ['ArrowUp', 'ArrowLeft'].includes(event.code) ? -1 : 1;
        if (['ArrowUp','ArrowDown'].includes(event.code) && scrollArea(delta)) return;
        if (!['ArrowLeft', 'ArrowRight'].includes(event.code) || !adjust(delta)) move(delta);
      } else if (event.code === 'Escape' && back) {
        event.preventDefault(); event.stopImmediatePropagation(); if (!event.repeat) back();
      } else if (event.code === 'Tab') {
        event.preventDefault(); event.stopImmediatePropagation(); move(event.shiftKey ? -1 : 1);
      } else if (event.repeat && ['Enter', 'Space'].includes(event.code)) {
        event.preventDefault(); event.stopImmediatePropagation();
      }
    };
    let lastIndex = 0;
    const remember = () => {
      lastIndex = Math.max(0, controls(root).indexOf(document.activeElement as HTMLElement));
      const selected = document.activeElement;
      if (selected instanceof HTMLElement && root.contains(selected)) saved.current.set(key, { label: identity(selected), scroll: [...root.querySelectorAll<HTMLElement>('.menu-scroll,.settings-grid,.menu-dialog-content')].map(el=>el.scrollTop) });
    };
    root.addEventListener('focusin', remember);
    const observer = new MutationObserver(() => {
      if (!active()) return;
      const items = controls(root);
      if (items.length && !items.includes(document.activeElement as HTMLElement)) reveal(items[Math.min(lastIndex,items.length-1)]);
    });
    observer.observe(root,{childList:true,subtree:true,attributes:true,attributeFilter:['disabled','hidden']});
    const pointer = (event: PointerEvent) => {
      if (!active()) return;
      if (event.type === 'pointermove' && !event.movementX && !event.movementY) return;
      publishDevice({ ...device, kind: 'pointer' });
      const el = (event.target as Element).closest<HTMLElement>('button,input,select,textarea,a[href]');
      if (event.type === 'pointerdown') editing = textControl(el) ? el : null;
      if (el && controls(root).includes(el) && !textControl(el)) el.focus({ preventScroll: true });
    };
    const prior = new Map<number, boolean[]>();
    let direction = 0, nextRepeat = 0, frame = 0;
    const poll = (time: number) => {
      for (const pad of (typeof navigator.getGamepads === 'function' ? navigator.getGamepads() : [])) {
        if (!pad) continue;
        const buttons = pad.buttons.map(b => b.pressed);
        const before = prior.get(pad.index) ?? buttons;
        prior.set(pad.index, buttons);
        if (!active()) continue;
        const pressed = buttons.findIndex((b, i) => b && !before[i]);
        const axisX = Math.abs(pad.axes[0] ?? 0) > .65 ? Math.sign(pad.axes[0]) : 0;
        const axisY = Math.abs(pad.axes[1] ?? 0) > .65 ? Math.sign(pad.axes[1]) : 0;
        const d = buttons[12] || axisY < 0 ? -2 : buttons[13] || axisY > 0 ? 2 : buttons[14] || axisX < 0 ? -1 : buttons[15] || axisX > 0 ? 1 : 0;
        if (pressed < 0 && !d) { direction = 0; continue; }
        const profile = detectGamepadProfile(pad.id, pad.mapping);
        const labels = profile === 'xbox' ? ['A','B'] : profile === 'playstation' ? ['✕','○'] : profile === 'nintendo' ? ['B','A'] : ['▼','▶'];
        publishDevice({ kind: 'pad', confirm: labels[0], back: labels[1] });
        if (d && (d !== direction || time >= nextRepeat)) {
          const delta = d < 0 ? -1 : 1;
          if (!(Math.abs(d) === 2 && scrollArea(delta)) && (Math.abs(d) !== 1 || !adjust(delta))) move(delta);
          nextRepeat = time + (d !== direction ? 350 : 130); direction = d;
        }
        if (pressed === 0) {
          const el = document.activeElement;
          if (textControl(el)) window.dispatchEvent(new CustomEvent('menu-edit-text', { detail: el }));
          else if (el instanceof HTMLSelectElement) adjust(1);
          else if (el instanceof HTMLElement && controls(root).includes(el)) el.click();
        } else if (pressed === 1) { if (back) back(); else controls(root).find(el => /^(Назад|Закрыть|Отменить)$/.test(identity(el)))?.click(); }
      }
      frame = requestAnimationFrame(poll);
    };
    frame = requestAnimationFrame(poll);
    window.addEventListener('keydown', keydown, true);
    root.addEventListener('pointermove', pointer);
    root.addEventListener('pointerdown', pointer);
    const blur = () => { document.documentElement.dataset.menuDevice = 'pointer'; };
    window.addEventListener('blur', blur);
    return () => {
      const selected = document.activeElement;
      if (selected instanceof HTMLElement && root.contains(selected)) saved.current.set(key, { label: identity(selected), scroll: [...root.querySelectorAll<HTMLElement>(".menu-scroll,.settings-grid,.menu-dialog-content")].map(el => el.scrollTop) });
      cancelAnimationFrame(frame); window.removeEventListener('keydown', keydown, true);
      observer.disconnect(); root.removeEventListener('focusin', remember); root.removeEventListener('pointermove', pointer); root.removeEventListener('pointerdown', pointer);
      window.removeEventListener('blur', blur);
      if (previous instanceof HTMLElement && previous.isConnected && previous !== document.body) previous.focus({ preventScroll: true });
      document.documentElement.dataset.menuDevice = 'pointer';
    };
  }, [key, back, ref]);
}
