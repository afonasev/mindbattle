const { contextBridge, ipcRenderer } = require("electron");
contextBridge.exposeInMainWorld("mindbattleDesktop", {
  version: 1,
  status: () => ipcRenderer.invoke("desktop:status"),
  checkUpdate: () => ipcRenderer.invoke("desktop:check-update"),
  onUpdate: (listener) => {
    const handler = (_event, ready) => listener(ready);
    ipcRenderer.on("desktop:update", handler);
    return () => ipcRenderer.removeListener("desktop:update", handler);
  },
  applyUpdate: () => ipcRenderer.invoke("desktop:apply"),
  safeToUpdate: (safe) => ipcRenderer.send("desktop:safe", safe === true),
  ready: () => ipcRenderer.invoke("desktop:ready"),
  display: () => ipcRenderer.invoke("desktop:display"),
  setDisplay: (settings) => ipcRenderer.invoke("desktop:set-display", settings),
  quit: () => ipcRenderer.invoke("desktop:quit"),
});
