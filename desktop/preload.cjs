const { contextBridge, ipcRenderer } = require("electron");
contextBridge.exposeInMainWorld("mindbattleDesktop", {
  version: 1,
  status: () => ipcRenderer.invoke("desktop:status"),
  downloadUpdate: () => ipcRenderer.invoke("desktop:download"),
  cancelDownload: () => ipcRenderer.invoke("desktop:cancel-download"),
  releaseHistory: () => ipcRenderer.invoke("desktop:history"),
  onUpdateStatus: (listener) => {
    const handler = (_event, status) => listener(status);
    ipcRenderer.on("desktop:update-status", handler);
    return () => ipcRenderer.removeListener("desktop:update-status", handler);
  },
  onUpdate: (listener) => {
    const handler = (_event, ready, version, publishedAt) => listener(ready, version, publishedAt);
    ipcRenderer.on("desktop:update", handler);
    return () => ipcRenderer.removeListener("desktop:update", handler);
  },
  applyUpdate: () => ipcRenderer.invoke("desktop:apply"),
  safeToUpdate: (safe) => ipcRenderer.invoke("desktop:safe", safe === true),
  ready: () => ipcRenderer.invoke("desktop:ready"),
  displayOptions: () => ipcRenderer.invoke("desktop:display-options"),
  confirmDisplay: () => ipcRenderer.invoke("desktop:confirm-display"),
  cancelDisplay: () => ipcRenderer.invoke("desktop:cancel-display"),
  display: () => ipcRenderer.invoke("desktop:display"),
  setDisplay: (settings) => ipcRenderer.invoke("desktop:set-display", settings),
  quit: () => ipcRenderer.invoke("desktop:quit"),
});
