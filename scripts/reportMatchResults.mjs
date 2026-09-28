import { readResults, resultReport } from '../server/resultReport.mjs';
const path = process.argv[2] ?? process.env.MINDBATTLE_RESULTS_PATH ?? 'data/match-results.ndjson';
try {
  const { events, corruptLines } = await readResults(path);
  console.log(JSON.stringify({ source: path, corruptLines, ...resultReport(events) }, null, 2));
} catch (error) { console.error(error.message); process.exitCode = 1; }
