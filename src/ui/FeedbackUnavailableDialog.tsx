import { useEffect, useRef } from "react";

export type FeedbackRecoveryChoice = "retry" | "skip";

export function FeedbackUnavailableDialog({
  selected,
  onSelect,
  onRetry,
  onSkip,
}: {
  readonly selected: FeedbackRecoveryChoice;
  readonly onSelect: (choice: FeedbackRecoveryChoice) => void;
  readonly onRetry: () => void;
  readonly onSkip: () => void;
}) {
  const firstButton = useRef<HTMLButtonElement>(null);
  const lastButton = useRef<HTMLButtonElement>(null);
  useEffect(() => firstButton.current?.focus(), []);
  return (
    <div className="feedback-unavailable-backdrop">
      <section className="feedback-unavailable-dialog" role="dialog" aria-modal="true" aria-labelledby="feedback-unavailable-title" onKeyDown={(event) => {
        if (event.key !== "Tab") return;
        event.preventDefault();
        const atFirst = document.activeElement === firstButton.current;
        (atFirst ? lastButton : firstButton).current?.focus();
      }}>
        <h2 id="feedback-unavailable-title">Отправка фидбэка временно недоступна</h2>
        <p>Можно повторить отправку или продолжить игру без неё.</p>
        <div className="feedback-unavailable-actions">
          <button ref={firstButton} type="button" className={selected === "retry" ? "feedback-unavailable-selected" : ""} onFocus={() => onSelect("retry")} onClick={onRetry}>Повторить</button>
          <button ref={lastButton} type="button" className={selected === "skip" ? "feedback-unavailable-selected" : ""} onFocus={() => onSelect("skip")} onClick={onSkip}>Пропустить</button>
        </div>
      </section>
    </div>
  );
}
