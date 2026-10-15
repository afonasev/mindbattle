import { menuDevice, useMenuNavigation } from "./menuNavigation";
import { useEffect, useId, useRef, useState, useCallback, type ButtonHTMLAttributes, type HTMLAttributes, type ReactNode } from "react";

export function ScreenSurface({ children, menuRef, menuSurface, ...props }: HTMLAttributes<HTMLElement> & { menuRef?: React.RefObject<HTMLElement | null>; menuSurface?: boolean }) {
  return <main {...props} ref={menuRef} data-menu-surface={menuSurface ? "" : undefined}>{children}</main>;
}

export function MenuAction({ variant = "secondary", className = "", onClick, children, caption, arrow = false, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { readonly variant?: "primary" | "secondary"; readonly caption?: ReactNode; readonly arrow?: boolean }) {
  const id = useId();
  const [input, setInput] = useState(menuDevice);
  useEffect(() => { const update = () => setInput(menuDevice()); window.addEventListener("menu-device", update); return () => window.removeEventListener("menu-device", update); }, []);
  const backAction = typeof children === "string" && /^(Назад|Закрыть|Отменить)$/.test(children);
  const describedBy = [props["aria-describedby"], caption ? `${id}-caption` : undefined].filter(Boolean).join(" ") || undefined;
  return <button {...props} aria-labelledby={props["aria-labelledby"] ?? (caption && !props["aria-label"] ? `${id}-label` : undefined)} aria-describedby={describedBy} type={props.type ?? "button"} className={`menu-action ${variant}-action ${caption || arrow ? "menu-action--detailed" : ""} ${className}`} onClick={(event) => { event.stopPropagation(); onClick?.(event); }}>
    <span className="menu-action-label" id={`${id}-label`}>{children}</span>
    {input.kind === "pad" && <span className={`pad-action-hint ${backAction ? "pad-action-hint--back" : ""}`} aria-hidden="true">{backAction ? input.back : input.confirm}</span>}
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
  return <header className={`game-brand screen-header ${className}`}>
    {hero ? <h1 className="screen-header-brand">Mindbattle</h1> : <strong className="screen-header-brand">Mindbattle</strong>}
    <span className="screen-header-subtitle">{subtitle}</span>
    <div className="screen-header-actions">
      {back && <MenuAction className="navigation-action" onClick={back}>Назад</MenuAction>}
      {menu && <MenuAction className="navigation-action" disabled={disabled} onClick={menu}>Меню</MenuAction>}
    </div>
  </header>;
}

export function MenuDialog({ title, label = "Меню", children, back, wide = false, className = "", footer }: { readonly className?: string; readonly footer?: ReactNode; readonly wide?: boolean; readonly title: string; readonly label?: string; readonly children: ReactNode; readonly back?: () => void }) {
  const id = useId();
  const panel = useRef<HTMLElement>(null);
  const backRef = useRef(back);
  backRef.current = back;
  const goBack = useCallback(() => backRef.current?.(), []);
  useMenuNavigation(panel, title, goBack);

  return <div ref={panel as React.RefObject<HTMLDivElement>} className="pause-backdrop" data-menu-surface role="dialog" aria-modal="true" aria-labelledby={id} onClick={(event) => event.stopPropagation()}><section className={`pause-dialog session-menu ${wide ? "session-menu--wide" : ""} ${className}`}><div className="stage-label">{label}</div><h2 id={id}>{title}</h2><div className="menu-dialog-content" data-menu-scroll-area tabIndex={0} role="region" aria-label="Содержимое">{children}</div>{footer && <div className="menu-dialog-actions">{footer}</div>}</section></div>;
}

export function SessionMenu({ title = "Игра на паузе", children, resume, settings, complaint, restart, restartLabel = "Начать заново", exit, exitLabel = "Выйти в меню", back, disabled = false, resumeDisabled = false }: {
  readonly title?: string; readonly children?: ReactNode; readonly resume?: () => void; readonly settings?: () => void; readonly complaint?: () => void; readonly restart?: () => void; readonly restartLabel?: string; readonly exit?: () => void; readonly exitLabel?: string; readonly back?: () => void; readonly disabled?: boolean; readonly resumeDisabled?: boolean;
}) {
  return <MenuDialog title={title} label="Меню игры" back={back ?? (resume && !disabled && !resumeDisabled ? resume : undefined)}>{children}<div className="menu-actions">
    {resume && <MenuAction variant="primary" disabled={disabled || resumeDisabled} onClick={resume}>Продолжить</MenuAction>}
    {complaint && <MenuAction disabled={disabled} onClick={complaint}>Пожаловаться на вопрос</MenuAction>}
    {settings && <MenuAction disabled={disabled} onClick={settings}>Настройки</MenuAction>}
    {restart && <MenuAction disabled={disabled} onClick={restart}>{restartLabel}</MenuAction>}
    {exit && <MenuAction disabled={disabled} onClick={exit}>{exitLabel}</MenuAction>}
    {back && <MenuAction onClick={back}>Назад</MenuAction>}
  </div></MenuDialog>;
}
