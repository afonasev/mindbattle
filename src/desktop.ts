export interface DisplaySettings {
  width: number;
  height: number;
  fullscreen: boolean;
}
export interface DesktopBridge {
  version: 1;
  status(): Promise<{ ready: boolean; shellVersion: string }>;
  checkUpdate?(): Promise<{ ready: boolean }>;
  onUpdate(listener: (ready: boolean) => void): () => void;
  applyUpdate(): Promise<boolean>;
  safeToUpdate(safe: boolean): void;
  ready(): Promise<void>;
  display(): Promise<DisplaySettings>;
  setDisplay(settings: DisplaySettings): Promise<DisplaySettings>;
  quit(): Promise<void>;
}
declare global {
  interface Window {
    mindbattleDesktop?: DesktopBridge;
  }
}
export const desktop =
  typeof window === "undefined" ? undefined : window.mindbattleDesktop;
export function downloadPlatform(
  ua: string,
  platform: string,
  touch: number,
): "mac" | "windows" | null {
  if (
    /Android|iPhone|iPad|iPod/i.test(ua) ||
    (/Mac/i.test(platform) && touch > 1)
  )
    return null;
  if (/Mac/i.test(platform || ua)) return "mac";
  if (/Win/i.test(platform || ua)) return "windows";
  return null;
}
