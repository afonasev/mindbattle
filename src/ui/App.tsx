import { useState } from "react";

const teams = [
  { letter: "З", color: "green", label: "Зелёная" },
  { letter: "С", color: "blue", label: "Синяя" },
  { letter: "Ж", color: "yellow", label: "Жёлтая" },
  { letter: "К", color: "red", label: "Красная" }
] as const;

export function App() {
  const [noticeVisible, setNoticeVisible] = useState(false);

  return (
    <main className="arena-shell">
      <div className="arena-glow" aria-hidden="true" />
      <header className="brand-lockup">
        <span className="eyebrow">Интеллектуальная битва</span>
        <h1>Mindbattle</h1>
        <p>Командная викторина для одного большого экрана</p>
      </header>

      <section className="launch-card" aria-labelledby="launch-title">
        <div className="stage-label">Прототип · foundation</div>
        <h2 id="launch-title">Арена готова к сборке</h2>
        <p>
          Технологическая основа запущена. В следующих этапах здесь появятся
          настройки команд, вопросы, таймер и настоящая партия.
        </p>
        <button type="button" onClick={() => setNoticeVisible(true)}>
          Начать игру
        </button>
        {noticeVisible && (
          <p className="foundation-notice" role="status">
            Игровой цикл будет подключён следующим OpenSpec change.
          </p>
        )}
      </section>

      <ul className="team-strip" aria-label="Команды Mindbattle">
        {teams.map((team) => (
          <li key={team.color} className={`team-chip team-chip--${team.color}`}>
            <span className="team-diamond" aria-hidden="true">
              <span>{team.letter}</span>
            </span>
            <span>{team.label}</span>
          </li>
        ))}
      </ul>

      <footer>Локально · Offline-first · 2–4 команды</footer>
    </main>
  );
}
