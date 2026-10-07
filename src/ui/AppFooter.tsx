import { useLayoutEffect, useRef } from "react";

const version = document.querySelector<HTMLMetaElement>('meta[name="mindbattle:version"]')?.content.split("+")[0] || "Разработка";
const publication = document.querySelector<HTMLMetaElement>('meta[name="mindbattle:published-at"]')?.content;
const publishedAt = publication && Number.isFinite(Date.parse(publication)) ? new Date(publication) : undefined;
const publicationLabel = publishedAt ? new Intl.DateTimeFormat("ru-RU", {
  year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", timeZoneName: "short",
}).format(publishedAt) : undefined;

export function AppFooter() {
  const ref = useRef<HTMLElement>(null);
  useLayoutEffect(() => {
    const footer = ref.current;
    if (!footer) return;
    const root = document.documentElement;
    const previous = root.style.getPropertyValue("--app-footer-height");
    const measure = () => root.style.setProperty("--app-footer-height", `${footer.getBoundingClientRect().height}px`);
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(footer);
    return () => {
      observer.disconnect();
      if (previous) root.style.setProperty("--app-footer-height", previous);
      else root.style.removeProperty("--app-footer-height");
    };
  }, []);
  return <footer ref={ref} className="app-release-footer" aria-label="Версия приложения">
    <span>Версия {version}</span>
    {publishedAt ? <span>Опубликована <time dateTime={publishedAt.toISOString()}>{publicationLabel}</time></span> : <span>Ещё не опубликована</span>}
  </footer>;
}
