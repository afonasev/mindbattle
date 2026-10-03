import { MenuAction, MenuDialog } from "./menuUi";

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
  return <MenuDialog title="Отправка фидбэка временно недоступна" label="Фидбэк">
    <p>Можно повторить отправку или продолжить игру без неё.</p>
    <div className="menu-actions">
      <MenuAction className={selected === "retry" ? "feedback-unavailable-selected" : ""} variant={selected === "retry" ? "primary" : "secondary"} onFocus={() => onSelect("retry")} onClick={onRetry}>Повторить</MenuAction>
      <MenuAction className={selected === "skip" ? "feedback-unavailable-selected" : ""} variant={selected === "skip" ? "primary" : "secondary"} onFocus={() => onSelect("skip")} onClick={onSkip}>Пропустить</MenuAction>
    </div>
  </MenuDialog>;
}
