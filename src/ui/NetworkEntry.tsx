import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { navigate } from "../main";
import { forgetCredential, networkRequest, savedCredential, savedCredentials } from "../network/client";
import type { Credential, LobbyCatalog, LobbyRoom } from "../network/protocol";
import { MenuAction, ScreenHeader } from "./menuUi";

function Lock() { return <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/><path d="M12 14v3"/></svg>; }
function PasswordField({ value, change, optional = false }: { value: string; change: (value: string) => void; optional?: boolean }) {
  const [visible, setVisible] = useState(false);
  return <label>Пароль {optional && <span className="network-field-optional">необязательно</span>}<span className="network-password-field"><input aria-label={optional ? "Пароль игры (необязательно)" : "Пароль игры"} type={visible ? "text" : "password"} value={value} maxLength={128} autoComplete={optional ? "new-password" : "off"} placeholder={optional ? "Оставьте пустым для открытой игры" : "Введите пароль игры"} onChange={e => change(e.target.value)}/><button type="button" aria-label={visible ? "Скрыть пароль" : "Показать пароль"} onClick={() => setVisible(!visible)}><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg></button></span></label>;
}
export function NetworkEntry({ mobile, busy, enter, restore, largeText, submissionError }: {
  mobile: boolean; busy: boolean; largeText: boolean; submissionError: string;
  enter: (data: { title: string; password: string } | { code: string; name: string; password: string }, create: boolean) => Promise<void>;
  restore: (credential: Credential) => void;
}) {
  const [mode, setMode] = useState<"catalog" | "create" | "join">(mobile ? "catalog" : "create");
  const [catalog, setCatalog] = useState<LobbyCatalog | null>(null);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<LobbyRoom | null>(null);
  const [unavailable, setUnavailable] = useState(false);
  const [title, setTitle] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [refresh, setRefresh] = useState(0);
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(6);
  const list = useRef<HTMLDivElement>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  const mountedMode = useRef(mode);
  useEffect(() => {
    if (mountedMode.current !== mode) heading.current?.focus();
    mountedMode.current = mode;
  }, [mode]);
  useEffect(() => {
    if (mode === "create") return;
    const abort = new AbortController();
    let active = false;
    const poll = async () => {
      if (active) return;
      active = true;
      try {
        const credentials = savedCredentials();
        const next = await networkRequest<LobbyCatalog>("catalog", { credentials }, undefined, abort.signal);
        if (!Array.isArray(next.rooms) || !Array.isArray(next.ownRooms) || !Array.isArray(next.invalidIndexes)) throw new Error("Не удалось прочитать список игр");
        if (abort.signal.aborted) return;
        for (const index of next.invalidIndexes) if (Number.isInteger(index) && credentials[index]) forgetCredential(credentials[index]);
        setCatalog(next);
        setError("");
        if (mode === "join" && selected) {
          const response = await fetch(`/api/network/room?code=${encodeURIComponent(selected.code)}`, { signal: abort.signal, cache: "no-store" });
          if (!response.ok) { setUnavailable(true); }
          else { setSelected(await response.json() as LobbyRoom); setUnavailable(false); }
        }
      } catch (e) { if (!abort.signal.aborted) setError((e as Error).message); }
      finally { active = false; }
    };
    void poll();
    const timer = setInterval(() => void poll(), 2000);
    return () => { abort.abort(); clearInterval(timer); };
  }, [mode, selected?.code, refresh]);
  const ownRooms = catalog?.ownRooms.filter(r => r.role === (mobile ? "player" : "display")) ?? [];
  const rooms = catalog?.rooms.filter(r => !ownRooms.some(own => own.code === r.code)) ?? [];
  useLayoutEffect(() => {
    if (mode !== "catalog" || !list.current) return;
    const measure = () => {
      if (!list.current) return;
      const top = list.current.getBoundingClientRect().top;
      const footer = document.querySelector(".app-release-footer")?.getBoundingClientRect().height ?? 0;
      const bottom = (window.visualViewport?.height ?? innerHeight) - footer - 56;
      const rowHeight = Math.max(57, ...Array.from(list.current.querySelectorAll(".network-room-row")).map(row => row.getBoundingClientRect().height + (innerHeight <= 760 ? 5 : 7)));
      setPageSize(Math.max(1, Math.min(12, Math.floor((bottom - top) / rowHeight))));
    };
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(list.current);
    window.addEventListener("resize", measure);
    window.visualViewport?.addEventListener("resize", measure);
    return () => { observer.disconnect(); window.removeEventListener("resize", measure); window.visualViewport?.removeEventListener("resize", measure); };
  }, [mode, rooms.length, ownRooms.length, largeText]);
  const pages = Math.max(1, Math.ceil(rooms.length / pageSize));
  const currentPage = Math.min(page, pages - 1);
  const select = (room: LobbyRoom) => { setSelected(room); setUnavailable(false); setPassword(""); setMode("join"); };
  const back = () => { if (mode === "join" || (mode === "create" && mobile)) { setMode("catalog"); setSelected(null); setPassword(""); } else navigate("/"); };
  return <>
    <ScreenHeader className="network-header" subtitle="Сетевая игра" back={back} disabled={busy}/>
    {error && <div className="network-catalog-error" role="alert"><span>{error}</span><MenuAction onClick={() => setRefresh(r => r + 1)}>Обновить список</MenuAction></div>}
    {mode === "create" ? <section className="network-create-layout">
      <div className="network-create-intro"><span className="network-eyebrow">Один экран. Вся компания.</span><h1 ref={heading} tabIndex={-1}>Соберите<br/>свою игру.</h1><p>Назовите комнату и пригласите друзей.<br/>Они найдут её в лобби на своих телефонах.</p><div className="network-create-details"><span>До 12 игроков</span><span>Через интернет</span></div></div>
      <section className="network-form-panel"><h2>Новая игра</h2>{submissionError && <p className="network-error" role="alert">{submissionError}</p>}<form onSubmit={e => { e.preventDefault(); void enter({ title, password }, true); }}><label>Название игры<input aria-label="Название игры" value={title} onChange={e => setTitle(e.target.value)} required maxLength={120} placeholder="Например, Вечер эрудитов" autoComplete="off"/></label><PasswordField value={password} change={setPassword} optional/><p className="network-form-hint">Игра с паролем тоже будет видна в лобби.</p><MenuAction type="submit" variant="primary" disabled={busy || !title.trim()}>Создать сетевую игру</MenuAction></form><p className="network-form-note">Этот экран станет общим экраном партии</p></section>
      {!mobile && <MenuAction className="network-show-catalog" onClick={() => setMode("catalog")}>Мои игры</MenuAction>}
    </section> : mode === "join" && selected ? <section className="network-join-layout"><span className="network-eyebrow">Выбранная игра</span><h1 ref={heading} tabIndex={-1}>{selected.title}</h1><div className="network-room-tags"><span>{selected.playerCount} / 12 игроков</span><span>{selected.passwordProtected ? <><Lock/> По паролю</> : "Вход свободный"}</span></div><p className="network-current-leader">{selected.leaderName ? <>Ведущий: <strong>{selected.leaderName}</strong></> : "Ведущий пока не выбран"}</p><section className="network-form-panel"><h2>Присоединиться</h2>{submissionError && <p className="network-error" role="alert">{submissionError}</p>}{unavailable && <p className="network-error" role="alert">Игра уже началась или закрыта. Выберите другую комнату.</p>}<form onSubmit={e => { e.preventDefault(); void enter({ code: selected.code, name, password }, false); }}><label>Ваше имя<input aria-label="Ваше имя" value={name} onChange={e => setName(e.target.value)} required maxLength={48} autoComplete="nickname"/></label>{selected.passwordProtected && <PasswordField value={password} change={setPassword}/>}<MenuAction variant="primary" type="submit" disabled={busy || unavailable || !name.trim() || selected.playerCount >= 12}>Подключиться</MenuAction></form></section></section> : <section className="network-catalog-layout"><span className="network-eyebrow">Играйте вместе</span><h1 ref={heading} tabIndex={-1}>Выберите игру</h1><p>Найдите свою компанию и вступите в игру.</p>
      {!!ownRooms.length && <><h2 className="network-list-label">Мои игры</h2><div className="network-own-rooms">{ownRooms.map(room => <MenuAction key={room.code} className="network-room-row network-room-own" onClick={() => { const credential = savedCredential(room.code, room.role); if (credential) restore(credential); }} disabled={busy}><span className="network-room-description"><strong>{room.title}</strong><small>{room.phase === "playing" ? "Игра идёт" : "Ждём начала"}{room.selfName ? ` · Вы — ${room.selfName}` : " · Общий экран"}</small></span><span className="network-room-return">Вернуться →</span></MenuAction>)}</div></>}
      <div className="network-catalog-heading"><h2 className="network-list-label">Открытые комнаты</h2><span>{rooms.length} игр</span><button type="button" aria-label="Обновить список" onClick={() => setRefresh(r => r + 1)}>↻</button></div>
      {!catalog ? <p role="status">Загружаем игры…</p> : !rooms.length ? <p className="network-empty-catalog">Пока нет открытых игр. Создайте комнату на общем экране — она появится здесь.</p> : <><div ref={list} className="network-room-list">{rooms.slice(currentPage * pageSize, (currentPage + 1) * pageSize).map(room => <MenuAction key={room.code} className="network-room-row" onClick={() => select(room)} disabled={busy || !mobile}><span className="network-room-description"><strong>{room.title}</strong><small>{room.playerCount} / 12 игроков<span aria-hidden="true"> · </span>{room.passwordProtected ? <><Lock/> По паролю</> : "Вход свободный"}</small></span><span aria-hidden="true" className="network-room-chevron">›</span></MenuAction>)}</div><nav className="network-list-pages" aria-label="Страницы комнат"><MenuAction aria-label="Предыдущая страница" disabled={currentPage === 0} onClick={() => setPage(currentPage - 1)}>‹</MenuAction><span>{currentPage + 1} / {pages}</span><MenuAction aria-label="Следующая страница" disabled={currentPage + 1 >= pages} onClick={() => setPage(currentPage + 1)}>›</MenuAction></nav></>}
      {!mobile && <MenuAction onClick={() => setMode("create")}>Создать сетевую игру</MenuAction>}
    </section>}
  </>;
}
