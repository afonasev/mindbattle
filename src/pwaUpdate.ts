export function canApplyPwaUpdate(matchActive: boolean, soloPhase: string | null): boolean {
  return !matchActive && (soloPhase === null || soloPhase === "finished");
}
