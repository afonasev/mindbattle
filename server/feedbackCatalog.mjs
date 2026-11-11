import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gunzipSync } from 'node:zlib';
import feedbackCatalogs from './feedbackCatalogs.json' with { type: 'json' };

const projectRoot = fileURLToPath(new URL('..', import.meta.url));

export async function readFeedbackCatalog(root = projectRoot) {
  const dir = join(root, 'src/content');
  const { revision: catalogRevision } = JSON.parse(await readFile(join(dir, 'revision.json'), 'utf8'));
  const topics = join(dir, 'topics');
  const questions = new Map();
  for (const name of await readdir(topics)) {
    if (!name.endsWith('.json')) continue;
    const topic = JSON.parse(await readFile(join(topics, name), 'utf8'));
    for (const question of topic.questions) questions.set(question.id, question.difficulty);
  }
  return { catalogRevision, questions };
}

export function historicalFeedbackCatalogs() {
  const manifests = JSON.parse(gunzipSync(Buffer.from(feedbackCatalogs.mapsGzip, 'base64')).toString('utf8'));
  return Object.fromEntries(Object.entries(feedbackCatalogs.revisions).map(([revision, key]) => [revision, manifests[key]]));
}

export function assertCompatibleFeedbackCatalogs(registry, incoming) {
  const canonical = map => JSON.stringify(Object.entries(map).sort(([a], [b]) => a.localeCompare(b)));
  for (const [revision, manifest] of Object.entries(incoming)) {
    if (Object.hasOwn(registry, revision) && canonical(registry[revision]) !== canonical(manifest)) {
      throw new Error(`Conflicting feedback catalog manifest: ${revision}`);
    }
  }
}
