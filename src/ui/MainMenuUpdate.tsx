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
  const [status, setStatus] = useState<DesktopUpdateStatus>({ phase: "idle" });
  useEffect(() => onPwaUpdate((available, nextVersion) => { setReady(available); setVersion(nextVersion); }), []);
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
  const backgroundBusy = status.phase === "checking" || downloading;
  const failed = status.phase === "error";
  if (!ready && !backgroundBusy && !failed) return null;
  const progress = downloading && status.total ? Math.floor(100 * (status.completed ?? 0) / status.total) : undefined;
  const label = phase === "applying" ? "Обновляем…" : downloading ? "Скачиваем обновление…" : phase === "checking" || backgroundBusy ? "Проверяем…" : ready ? "Появилось новое обновление" : "Повторить проверку";
  const nextVersion = version ?? status.version;
  return <div className="menu-update">
    <MenuAction arrow caption={nextVersion ? `Версия ${nextVersion.split("+")[0]}` : "Обновить игру"} disabled={phase !== "idle" || backgroundBusy} aria-busy={phase !== "idle" || backgroundBusy} onClick={() => void update()}>
      {label}
    </MenuAction>
    {downloading && <p className="menu-update-message" role="status">{progress === 100 ? "Проверяем скачанные файлы…" : `Скачано ${progress ?? 0}% файлов`}</p>}
    {(message || failed) && <p className="menu-update-message" role={error || failed ? "alert" : "status"}>{message || status.message}</p>}
  </div>;
}
