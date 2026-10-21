import type { Page } from '@playwright/test';
export function expectAfterMount(
  page: Pick<Page, 'waitForFunction'>,
  selector: string,
  assertion: (options: { timeout: number }) => Promise<unknown>,
  timeout?: number
): Promise<void>;
