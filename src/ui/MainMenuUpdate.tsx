import { useEffect, useRef, useState } from "react";
import { onPwaUpdate, onDesktopUpdateStatus, updateGame } from "../main";
import { type DesktopUpdateStatus } from "../desktop";
import { MenuAction } from "./menuUi";

export function MainMenuUpdate() {
  const active = useRef(false);
  const pending = useRef(false);
  const restartTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const [phase, setPhase] = useState<"idle" | "checking" | "applying">("idle");
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);
  const [ready, setReady] = useState(false);
  const [version, setVersion] = useState<string>();
  const [publishedAt, setPublishedAt] = useState<string>();
  const [status, setStatus] = useState<DesktopUpdateStatus>({ phase: "idle" });
  useEffect(() => onPwaUpdate((available, nextVersion, publication) => { setReady(available); setVersion(nextVersion); setPublishedAt(publication); }), []);
  useEffect(() => onDesktopUpdateStatus(setStatus), []);
  useEffect(() => { active.current = true; return () => { active.current = false; clearTimeout(restartTimer.current); }; }, []);
  async function update() {
    if (pending.current) return;
    pending.current = true;
    setPhase("checking");
    setMessage("");
    setError(false);
    let restarting = false;
    try {
      const result = await updateGame(() => active.current, () => setPhase("applying"));
      if (active.current && result === "current") setReady(false);
      if (active.current && result === "applied") {
        restarting = true;
        setMessage("Перезапускаем игру…");
        restartTimer.current = setTimeout(() => {
          pending.current = false;
          setPhase("idle");
          setError(true);
          setMessage("Игра не перезапустилась. Нажмите «Обновить» ещё раз.");
        }, 15_000);
      }
    } catch (cause) {
      if (active.current) {
        setError(true);
        const detail = cause instanceof Error ? cause.message.replace(/^Error invoking remote method[^:]*: Error: /, "") : "";
        setMessage(/^[А-ЯЁ]/.test(detail) ? detail : "Не удалось обновить игру. Проверьте подключение и попробуйте ещё раз.");
      }
    } finally {
      if (!restarting) {
        pending.current = false;
        if (active.current) setPhase("idle");
      }
    }
  }
  const downloading = status.phase === "downloading";
  const failed = status.phase === "error";
  const progress = downloading && status.total ? Math.floor(100 * (status.completed ?? 0) / status.total) : undefined;
  if (!ready) {
    if (status.phase === 'checking') return <p className="menu-update-status" role="status">Проверяем обновления…</p>;
    if (downloading) return <p className="menu-update-status" role="status">{progress === 100 ? 'Проверяем скачанные файлы…' : `Скачиваем обновление · ${progress ?? 0}% файлов`}</p>;
    if (failed) return <p className="menu-update-status" role="status">Не удалось проверить обновления. Повторим автоматически.</p>;
    return null;
  }
  const publication = publishedAt && Number.isFinite(Date.parse(publishedAt)) ? new Date(publishedAt) : undefined;
  const publicationLabel = publication ? new Intl.DateTimeFormat('ru-RU', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', timeZoneName: 'short' }).format(publication) : undefined;
  const label = phase === "applying" ? "Обновляем…" : phase === "checking" ? "Проверяем…" : "Обновить";
  return <div className="menu-update">
    <MenuAction className="menu-update-ready" arrow caption={<><span>{version ? `Версия ${version.split("+")[0]}` : 'Новая версия'}</span><span>{publication ? <>Опубликована <time dateTime={publication.toISOString()}>{publicationLabel}</time></> : 'Дата публикации не указана'}</span></>} disabled={phase !== "idle"} aria-busy={phase !== "idle"} onClick={() => void update()}>
      {label}
    </MenuAction>
    {message && <p className="menu-update-message" role={error ? "alert" : "status"}>{message}</p>}
  </div>;
}
