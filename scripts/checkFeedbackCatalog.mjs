import {
  assertCompatibleFeedbackCatalogs,
  historicalFeedbackCatalogs,
  readFeedbackCatalog
} from '../server/feedbackCatalog.mjs';

try {
  const [mode, baselineRoot, ...extra] = process.argv.slice(2);
  let registry;
  if (mode === '--registry-stdin' && baselineRoot === undefined) {
    let input = '';
    for await (const chunk of process.stdin.setEncoding('utf8')) input += chunk;
    registry = JSON.parse(input);
    if (!registry || Array.isArray(registry) || typeof registry !== 'object') {
      throw new Error('Expected a feedback catalog registry object on stdin');
    }
  } else if (mode === '--baseline' && baselineRoot && extra.length === 0) {
    const baseline = await readFeedbackCatalog(baselineRoot);
    registry = { [baseline.catalogRevision]: Object.fromEntries(baseline.questions) };
  } else {
    throw new Error('Usage: node scripts/checkFeedbackCatalog.mjs --registry-stdin | --baseline <checkout>');
  }

  const { catalogRevision, questions } = await readFeedbackCatalog();
  const current = { [catalogRevision]: Object.fromEntries(questions) };
  const historical = historicalFeedbackCatalogs();
  assertCompatibleFeedbackCatalogs(historical, current);
  assertCompatibleFeedbackCatalogs(registry, { ...historical, ...current });
  console.log(`Feedback catalog compatible: ${catalogRevision}`);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
