import { useEffect, useState } from 'react';
import { statisticsEnabled } from '../statistics/preference';
import { setStatisticsEnabled } from '../statistics/control';
export function useStatistics() {
  const [enabled, setEnabled] = useState(statisticsEnabled);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  useEffect(() => {
    const refresh = () => setEnabled(statisticsEnabled());
    window.addEventListener('storage', refresh); window.addEventListener('mindbattle-statistics', refresh);
    return () => { window.removeEventListener('storage', refresh); window.removeEventListener('mindbattle-statistics', refresh); };
  }, []);
  return { enabled, pending, error, setEnabled: async (value: boolean) => {
    setEnabled(value); setPending(true); setError('');
    try { await setStatisticsEnabled(value); }
    catch (e) { setError(e instanceof Error ? e.message : 'Не удалось изменить настройку статистики.'); }
    finally { setEnabled(statisticsEnabled()); setPending(false); }
  } };
}
