export interface Scope { units: string[] | null; browser: [string, string, number?][] | null; projects?: string[] }
export const scopes: Record<string, Scope>;
export function selectedSpec(scope: Scope, file: string, title: string): boolean;
