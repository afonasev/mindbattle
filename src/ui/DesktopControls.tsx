import { useEffect, useState } from "react";
import { desktop, type DisplaySettings } from "../desktop";
export function DesktopQuit() {
  return desktop ? (
    <button
      type="button"
      className="secondary-action"
      onClick={() => void desktop!.quit()}
    >
      Выход из игры
    </button>
  ) : null;
}
export function DesktopDisplaySettings() {
  const [value, setValue] = useState<DisplaySettings>();
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    void desktop
      ?.display()
      .then(setValue)
      .catch(() => setError("Не удалось загрузить настройки экрана"));
  }, []);
  if (!desktop) return null;
  async function save(next: DisplaySettings) {
    setBusy(true);
    setError("");
    try {
      setValue(await desktop!.setDisplay(next));
    } catch {
      setError("Не удалось изменить настройки экрана");
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="settings-group" aria-labelledby="desktop-display-title">
      <h3 id="desktop-display-title">Экран</h3>
      {value && (
        <>
          <label className="desktop-setting">
            Режим экрана
            <select
              aria-label="Режим экрана"
              disabled={busy}
              value={value.fullscreen ? "full" : "window"}
              onChange={(e) =>
                void save({ ...value, fullscreen: e.target.value === "full" })
              }
            >
              <option value="window">Оконный</option>
              <option value="full">Полный экран</option>
            </select>
          </label>
          <label className="desktop-setting">
            Разрешение окна
            <select
              aria-label="Разрешение окна"
              disabled={busy || value.fullscreen}
              value={`${value.width}x${value.height}`}
              onChange={(e) => {
                const [width, height] = e.target.value.split("x").map(Number);
                void save({ ...value, width, height });
              }}
            >
              {[
                "1024x768",
                "1280x720",
                "1366x768",
                "1600x900",
                "1920x1080",
                "2560x1440",
                "3840x2160",
              ].map((size) => (
                <option key={size} value={size}>
                  {size.replace("x", " × ")}
                </option>
              ))}
            </select>
          </label>
          {value.fullscreen && (
            <p>Полный экран использует разрешение монитора.</p>
          )}
        </>
      )}
      {error && <p role="alert">{error}</p>}
    </section>
  );
}
