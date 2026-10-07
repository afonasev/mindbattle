import { useEffect, useState } from 'react';
import type { ComplaintReason } from '../domain/types';
import { browserFeedback, complaintEvent } from '../feedback/outbox';
import type { ComplaintContext } from '../feedback/types';
import type { LegacyComplaintDraft } from '../domain/types';
import { difficultyLabel } from './difficulty';
import { MenuAction, MenuDialog } from './menuUi';

const reasons: readonly [ComplaintReason, string][] = [
  ['too-easy', 'Слишком лёгкий'], ['too-hard', 'Слишком сложный'],
  ['weak-answer-options', 'Неправильные ответы очевидны'], ['unclear-wording', 'Непонятная формулировка'],
  ['suspected-error', 'Фактическая ошибка'], ['ambiguous-answer', 'Неоднозначный ответ'],
  ['uninteresting-for-quiz', 'Неинтересный для викторины']
];
export function ComplaintDialog({ context, initial, close }: { readonly context: ComplaintContext; readonly initial?: LegacyComplaintDraft; readonly close: () => void }) {
  const [selected, setSelected] = useState<readonly ComplaintReason[]>(initial?.complaintReasons ?? []);
  const [note, setNote] = useState(initial?.complaintNote ?? '');
  const [alreadySaved, setAlreadySaved] = useState(false);
  useEffect(() => { let active = true; void browserFeedback().has(context.eventId).then(saved => { if (active) setAlreadySaved(saved); }).catch(() => {}); return () => { active = false; }; }, [context.eventId]);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  function toggle(reason: ComplaintReason) {
    setSelected(value => value.includes(reason) ? value.filter(item => item !== reason) : [...value.filter(item => !(reason === 'too-easy' && item === 'too-hard') && !(reason === 'too-hard' && item === 'too-easy')), reason]);
  }
  async function save() {
    setPending(true); setError('');
    try { await browserFeedback().submit(complaintEvent(context, selected, note)); close(); }
    catch { setError('Не удалось сохранить жалобу на устройстве. Попробуйте ещё раз или отмените.'); }
    finally { setPending(false); }
  }
  if (alreadySaved) return <MenuDialog title="Жалоба сохранена" label="Жалоба" back={close}><p>Жалоба на этот вопрос уже сохранена и будет отправлена при доступном интернете.</p><MenuAction onClick={close}>Вернуться к ответам</MenuAction></MenuDialog>;
  return <MenuDialog title="Пожаловаться на вопрос" label="Жалоба" back={pending ? undefined : close} wide className="complaint-dialog">
    <p>Сложность: {difficultyLabel(context.assignedDifficulty)}</p>
    <div className="menu-actions complaint-reasons">{reasons.map(([reason, label]) => <MenuAction key={reason} aria-label={label} aria-pressed={selected.includes(reason)} disabled={pending} onClick={() => toggle(reason)}>{selected.includes(reason) ? '✓ ' : ''}{label}</MenuAction>)}</div>
    <label className="feedback-note">Заметка (необязательно, до 500 символов)<textarea value={note} maxLength={500} disabled={pending} onChange={event => setNote(event.target.value)} /></label>
    <p>Жалоба сохранится на устройстве и отправится при доступном интернете.</p>
    {error && <p role="alert">{error}</p>}
    <div className="menu-actions"><MenuAction variant="primary" disabled={pending || (!selected.length && !note.trim())} onClick={() => void save()}>{pending ? 'Сохраняем…' : 'Сохранить жалобу'}</MenuAction><MenuAction disabled={pending} onClick={close}>Отмена</MenuAction></div>
  </MenuDialog>;
}
