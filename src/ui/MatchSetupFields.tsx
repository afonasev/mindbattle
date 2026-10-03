import type { ReactNode } from "react";

const QUESTION_COUNTS = [9, 15, 21] as const;
const ANSWER_TIMES = [10_000, 20_000, 30_000] as const;

function SetupChoice({ label, value, options, change, compact, disabled }: {
  readonly label: string; readonly value: number; readonly options: readonly { readonly value: number; readonly label: string }[]; readonly change: (value: number) => void; readonly compact: boolean; readonly disabled: boolean;
}) {
  if (compact) return <label>{label}<select aria-label={label} value={value} disabled={disabled} onChange={(event) => change(Number(event.target.value))}>{options.map(option => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>;
  return <fieldset><legend>{label}</legend>{options.map(option => <button type="button" key={option.value} disabled={disabled} className={value === option.value ? "is-selected" : ""} onClick={() => change(option.value)}>{option.label}</button>)}</fieldset>;
}

export function MatchSetupFields({ questionCount, answerTimeMs, setQuestionCount, setAnswerTimeMs, teamCount, setTeamCount, compact = false, disabled = false, children }: {
  readonly questionCount: number; readonly answerTimeMs: number; readonly setQuestionCount: (value: typeof QUESTION_COUNTS[number]) => void; readonly setAnswerTimeMs: (value: typeof ANSWER_TIMES[number]) => void; readonly teamCount?: 2 | 3 | 4; readonly setTeamCount?: (value: 2 | 3 | 4) => void; readonly compact?: boolean; readonly disabled?: boolean; readonly children?: ReactNode;
}) {
  return <div className={compact ? "network-settings" : "segmented-settings"}>
    <SetupChoice label="Вопросов" value={questionCount} options={QUESTION_COUNTS.map(value => ({ value, label: String(value) }))} change={(value) => setQuestionCount(value as typeof QUESTION_COUNTS[number])} compact={compact} disabled={disabled} />
    {teamCount !== undefined && setTeamCount && <SetupChoice label="Команд" value={teamCount} options={[2, 3, 4].map(value => ({ value, label: String(value) }))} change={(value) => setTeamCount(value as 2 | 3 | 4)} compact={compact} disabled={disabled} />}
    <SetupChoice label={compact ? "Время на ответ" : "На ответ"} value={answerTimeMs} options={ANSWER_TIMES.map(value => ({ value, label: `${value / 1000} ${compact ? "секунд" : "c"}` }))} change={(value) => setAnswerTimeMs(value as typeof ANSWER_TIMES[number])} compact={compact} disabled={disabled} />
    {children}
  </div>;
}
