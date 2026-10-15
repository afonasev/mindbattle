export interface DisplaySettings {
  width: number;
  height: number;
  fullscreen: boolean;
  auto?: boolean;
}
export interface DesktopUpdateStatus {
  phase: "idle" | "checking" | "downloading" | "available" | "paused" | "verifying" | "download-error" | "ready" | "current" | "error";
  version?: string;
  publishedAt?: string;
  completed?: number;
  total?: number;
  message?: string;
}
export interface DesktopBridge {
  version: 1;
  status(): Promise<{ ready: boolean; shellVersion: string; platform?: string; architecture?: string; channel?: string; updateVersion?: string; updatePublishedAt?: string; updateStatus?: DesktopUpdateStatus }>;
  checkUpdate?(): Promise<{ ready: boolean }>; // Legacy shells only.
  downloadUpdate?(): Promise<boolean>;
  cancelDownload?(): Promise<void>;
  releaseHistory?(): Promise<readonly { tag: string; version: string; date: string; notes: string }[]>;
  onUpdateStatus?(listener: (status: DesktopUpdateStatus) => void): () => void;
  onUpdate(listener: (ready: boolean, version?: string, publishedAt?: string) => void): () => void;
  applyUpdate(): Promise<boolean>;
  safeToUpdate(safe: boolean): void | Promise<void>;
  ready(): Promise<void>;
  display(): Promise<DisplaySettings>;
  displayOptions?(): Promise<readonly { width:number; height:number }[]>;
  confirmDisplay?(): Promise<DisplaySettings>;
  cancelDisplay?(): Promise<DisplaySettings>;
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
