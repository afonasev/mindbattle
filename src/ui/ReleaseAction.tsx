import { useEffect, useState } from "react";
import { desktop, downloadPlatform } from "../desktop";
import { applyPwaUpdate, onPwaUpdate } from "../main";
export function ReleaseAction({ safe = true }: { safe?: boolean }) {
  const [ready, setReady] = useState(false);
  const [url, setUrl] = useState<string>();
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => onPwaUpdate(setReady), []);
  useEffect(() => {
    desktop?.safeToUpdate(safe);
    return () => desktop?.safeToUpdate(false);
  }, [safe]);
  useEffect(() => {
    if (desktop) return;
    const platform = downloadPlatform(
      navigator.userAgent,
      navigator.platform,
      navigator.maxTouchPoints,
    );
    if (!platform) return;
    const abort = new AbortController();
    void fetch("/desktop/downloads.json", {
      signal: abort.signal,
      cache: "no-cache",
    })
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        const entry = data?.[platform];
        if (
          typeof entry?.url === "string" &&
          /^\/desktop\/installers\/[a-zA-Z0-9_.-]+$/.test(entry.url)
        )
          setUrl(entry.url);
      })
      .catch(() => {});
    return () => abort.abort();
  }, []);
  if (!safe) return null;
  return (
    <>
      {ready ? (
        <button
          className="pwa-update release-action"
          type="button"
          title="Доступно обновление · Обновить"
          aria-label="Доступно обновление · Обновить"
          disabled={busy}
          onClick={() => {
            setBusy(true);
            void applyPwaUpdate()
              .catch(() =>
                setError("Обновление не применилось. Попробуйте ещё раз."),
              )
              .finally(() => setBusy(false));
          }}
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M20 7v5h-5M4 17v-5h5M6.1 7a7 7 0 0 1 11.6-1L20 9M4 15l2.3 3a7 7 0 0 0 11.6-1" />
          </svg>
        </button>
      ) : (
        url && (
          <a
            className="pwa-update release-action"
            href={url}
            title="Скачать игру"
            aria-label="Скачать игру"
          >
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5" />
            </svg>
          </a>
        )
      )}
      {error && (
        <p className="release-error" role="alert">
          {error}
        </p>
      )}
    </>
  );
}
