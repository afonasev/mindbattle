import { useEffect, useId, useRef, type ButtonHTMLAttributes, type HTMLAttributes, type ReactNode } from "react";

export function ScreenSurface({ children, ...props }: HTMLAttributes<HTMLElement>) {
  return <main {...props}>{children}</main>;
}

export function MenuAction({ variant = "secondary", className = "", onClick, children, caption, arrow = false, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { readonly variant?: "primary" | "secondary"; readonly caption?: ReactNode; readonly arrow?: boolean }) {
  const id = useId();
  const describedBy = [props["aria-describedby"], caption ? `${id}-caption` : undefined].filter(Boolean).join(" ") || undefined;
  return <button {...props} aria-labelledby={props["aria-labelledby"] ?? (caption && !props["aria-label"] ? `${id}-label` : undefined)} aria-describedby={describedBy} type={props.type ?? "button"} className={`menu-action ${variant}-action ${caption || arrow ? "menu-action--detailed" : ""} ${className}`} onClick={(event) => { event.stopPropagation(); onClick?.(event); }}>
    <span className="menu-action-label" id={`${id}-label`}>{children}</span>
    {caption && <span className="menu-action-caption" id={`${id}-caption`}>{caption}</span>}
    {arrow && <span className="menu-action-arrow" aria-hidden="true">→</span>}
  </button>;
}

export function ScreenHeader({ subtitle, back, menu, disabled = false, hero = false, className = "" }: { readonly subtitle?: ReactNode; readonly back?: () => void; readonly menu?: () => void; readonly disabled?: boolean; readonly hero?: boolean; readonly className?: string }) {
  useEffect(() => {
    if (!back) return;
    const keyboard = (event: KeyboardEvent) => {
      if (event.code === "Escape" && !event.repeat && !document.querySelector('[aria-modal="true"]')) { event.preventDefault(); back(); }
    };
    window.addEventListener("keydown", keyboard);
    return () => window.removeEventListener("keydown", keyboard);
  }, [back]);
  return <header className={hero ? "brand-lockup brand-lockup--menu" : `game-brand screen-header ${className}`}>
    {hero ? <><span className="eyebrow">Интеллектуальная битва</span><h1>Mindbattle</h1><p>Все решит эрудиция</p></> : <><strong>Mindbattle</strong><span className="screen-header-subtitle">{subtitle}</span></>}
    {back && <MenuAction className="navigation-action" onClick={back}>Назад</MenuAction>}
    {menu && <MenuAction className="navigation-action" disabled={disabled} onClick={menu}>Меню</MenuAction>}
  </header>;
}

export function MenuDialog({ title, label = "Меню", children, back, wide = false }: { readonly wide?: boolean; readonly title: string; readonly label?: string; readonly children: ReactNode; readonly back?: () => void }) {
  const id = useId();
  const panel = useRef<HTMLElement>(null);
  const backRef = useRef(back);
  backRef.current = back;
  useEffect(() => {
    const previous = document.activeElement;
    panel.current?.querySelector<HTMLElement>("button:not(:disabled), input, select")?.focus();
    const keyboard = (event: KeyboardEvent) => {
      if (event.code === "Escape") { event.preventDefault(); event.stopImmediatePropagation(); backRef.current?.(); }
      if (event.code === "Tab") {
        const items = [...(panel.current?.querySelectorAll<HTMLElement>('button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), a[href]') ?? [])];
        const first = items[0], last = items.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
      }
    };
    window.addEventListener("keydown", keyboard, true);
    return () => { window.removeEventListener("keydown", keyboard, true); if (previous instanceof HTMLElement && previous.isConnected) previous.focus(); };
  }, []);
  return <div className="pause-backdrop" role="dialog" aria-modal="true" aria-labelledby={id} onClick={(event) => event.stopPropagation()}><section ref={panel} className={`pause-dialog session-menu ${wide ? "session-menu--wide" : ""}`}><div className="stage-label">{label}</div><h2 id={id}>{title}</h2>{children}</section></div>;
}

export function SessionMenu({ title = "Игра на паузе", children, resume, settings, restart, restartLabel = "Начать заново", exit, exitLabel = "Выйти в меню", back, disabled = false, resumeDisabled = false }: {
  readonly title?: string; readonly children?: ReactNode; readonly resume?: () => void; readonly settings?: () => void; readonly restart?: () => void; readonly restartLabel?: string; readonly exit?: () => void; readonly exitLabel?: string; readonly back?: () => void; readonly disabled?: boolean; readonly resumeDisabled?: boolean;
}) {
  return <MenuDialog title={title} label="Меню игры" back={back ?? (resume && !disabled && !resumeDisabled ? resume : undefined)}>{children}<div className="menu-actions">
    {resume && <MenuAction variant="primary" disabled={disabled || resumeDisabled} onClick={resume}>Продолжить</MenuAction>}
    {settings && <MenuAction disabled={disabled} onClick={settings}>Настройки</MenuAction>}
    {restart && <MenuAction disabled={disabled} onClick={restart}>{restartLabel}</MenuAction>}
    {exit && <MenuAction disabled={disabled} onClick={exit}>{exitLabel}</MenuAction>}
    {back && <MenuAction onClick={back}>Назад</MenuAction>}
  </div></MenuDialog>;
}
