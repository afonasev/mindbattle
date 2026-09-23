import type { IncomingMessage, ServerResponse } from "node:http";

export function serveStatic(request: IncomingMessage, response: ServerResponse, distRoot: string): Promise<void>;
