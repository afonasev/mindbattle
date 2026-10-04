import { describe, expect, it, vi } from "vitest";
import { runManualUpdate, withUpdateTimeout } from "../../src/gameUpdate";
import { findPwaUpdate } from "../../src/pwaUpdate";

function registration() {
  const worker = Object.assign(new EventTarget(), { state: "installing" });
  const reg = Object.assign(new EventTarget(), { waiting: null as unknown, installing: null as unknown, update: vi.fn(async () => {}) });
  return { worker, reg: reg as unknown as ServiceWorkerRegistration, mutable: reg };
}

describe("manual game update", () => {
  it("does not apply on a successful empty check or failed check", async () => {
    const apply = vi.fn();
    const args = { apply, isSafe: () => true, onApplying: vi.fn() };
    expect(await runManualUpdate({ ...args, check: async () => false })).toBe("current");
    await expect(runManualUpdate({ ...args, check: async () => { throw Error("offline"); } })).rejects.toThrow("offline");
    expect(apply).not.toHaveBeenCalled();
  });
  it("rechecks safety after the asynchronous download", async () => {
    let safe = true;
    const apply = vi.fn();
    expect(await runManualUpdate({ check: async () => { safe = false; return true; }, apply, isSafe: () => safe, onApplying: vi.fn() })).toBe("deferred");
    expect(apply).not.toHaveBeenCalled();
  });
  it("applies a ready update once and propagates application failure", async () => {
    const apply = vi.fn(async () => {});
    const onApplying = vi.fn();
    expect(await runManualUpdate({ check: async () => true, apply, isSafe: () => true, onApplying })).toBe("applied");
    expect(apply).toHaveBeenCalledOnce();
    expect(onApplying).toHaveBeenCalledOnce();
    await expect(runManualUpdate({ check: async () => true, apply: async () => { throw Error("unsafe"); }, isSafe: () => true, onApplying })).rejects.toThrow("unsafe");
  });
  it("bounds registration waits", async () => {
    await expect(withUpdateTimeout(new Promise(() => {}), 1)).rejects.toThrow("слишком много времени");
  });
});

describe("PWA download readiness", () => {
  it("applies a waiting worker without requiring a network check", async () => {
    const { reg, mutable } = registration();
    mutable.waiting = {};
    expect(await findPwaUpdate(reg)).toBe(true);
    expect(mutable.update).not.toHaveBeenCalled();
  });
  it("waits for precache installation after update() resolves", async () => {
    const { reg, mutable, worker } = registration();
    mutable.update.mockImplementation(async () => {
      mutable.installing = worker;
      reg.dispatchEvent(new Event("updatefound"));
    });
    let settled = false;
    const result = findPwaUpdate(reg).then(ready => { settled = true; return ready; });
    await Promise.resolve(); await Promise.resolve();
    expect(settled).toBe(false);
    mutable.waiting = worker; mutable.installing = null; worker.state = "installed";
    worker.dispatchEvent(new Event("statechange"));
    expect(await result).toBe(true);
  });
  it("distinguishes first installation from a waiting update", async () => {
    const { reg, mutable, worker } = registration();
    mutable.installing = worker;
    const result = findPwaUpdate(reg);
    await Promise.resolve();
    mutable.installing = null; worker.state = "activated"; worker.dispatchEvent(new Event("statechange"));
    expect(await result).toBe(false);
  });
  it("returns current only after a successful check", async () => {
    const { reg, mutable } = registration();
    expect(await findPwaUpdate(reg)).toBe(false);
    mutable.update.mockRejectedValue(Error("offline"));
    await expect(findPwaUpdate(reg)).rejects.toThrow("offline");
  });
  it("rejects redundant workers and cleans listeners on timeout", async () => {
    const { reg, mutable, worker } = registration();
    mutable.installing = worker;
    const result = findPwaUpdate(reg);
    worker.state = "redundant"; worker.dispatchEvent(new Event("statechange"));
    await expect(result).rejects.toThrow("Не удалось загрузить");
    worker.state = "installing";
    const remove = vi.spyOn(worker, "removeEventListener");
    await expect(findPwaUpdate(reg, 1)).rejects.toThrow("слишком много времени");
    expect(remove).toHaveBeenCalledWith("statechange", expect.any(Function));
  });
});
