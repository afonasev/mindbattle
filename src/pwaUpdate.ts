export function canApplyPwaUpdate(matchActive: boolean, soloPhase: string | null): boolean {
  return !matchActive && (soloPhase === null || soloPhase === "finished");
}

export async function checkForPwaUpdate(
  registration: Pick<ServiceWorkerRegistration, "update"> | undefined
): Promise<void> {
  await registration?.update();
}
