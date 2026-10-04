import { useEffect, useRef, useState } from "react";
import { onPwaUpdate, updateGame } from "../main";
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
  useEffect(() => onPwaUpdate((available, nextVersion) => { setReady(available); setVersion(nextVersion); }), []);
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
  if (!ready) return null;
  return <div className="menu-update">
    <MenuAction arrow caption={version ? `Версия ${version}` : "Обновить игру"} disabled={phase !== "idle"} aria-busy={phase !== "idle"} onClick={() => void update()}>
      {phase === "checking" ? "Проверяем…" : phase === "applying" ? "Обновляем…" : "Появилось новое обновление"}
    </MenuAction>
    {message && <p className="menu-update-message" role={error ? "alert" : "status"}>{message}</p>}
  </div>;
}
