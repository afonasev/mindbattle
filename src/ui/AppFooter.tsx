const version = document.querySelector<HTMLMetaElement>('meta[name="mindbattle:version"]')?.content.split("+")[0] || "Разработка";
const publication = document.querySelector<HTMLMetaElement>('meta[name="mindbattle:published-at"]')?.content;
const publishedAt = publication && Number.isFinite(Date.parse(publication)) ? new Date(publication) : undefined;
const publicationLabel = publishedAt ? new Intl.DateTimeFormat("ru-RU", {
  year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", timeZoneName: "short",
}).format(publishedAt) : undefined;

export function AppFooter() {
  return <footer className="app-release-footer" aria-label="Версия приложения">
    <span>Версия {version}</span>
    {publishedAt ? <span>Опубликована <time dateTime={publishedAt.toISOString()}>{publicationLabel}</time></span> : <span>Ещё не опубликована</span>}
  </footer>;
}
