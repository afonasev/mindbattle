import { describe, expect, it } from 'vitest';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createFeedbackStore } from '../../server/feedbackStore.mjs';
describe('historical complaint delivery', () => {
  it('keeps trusted old catalogs and idempotency across restart without accepting invented revisions', async () => {
    const directory=await mkdtemp(join(tmpdir(),'mindbattle-complaint-history-'));
    try {
      const options={filePath:join(directory,'feedback.ndjson'),questions:new Map([['new-question','hard']]),catalogRevision:'new-catalog'};
      const old={schemaVersion:3,eventId:'old-event',matchId:'match',catalogRevision:'old-catalog',questionId:'old-question',assignedDifficulty:'easy',hasComplaint:true,complaintReasons:['suspected-error']};
      const first=await createFeedbackStore({...options,historicalCatalogs:{'old-catalog':{'old-question':'easy'}}});
      expect(await first.append(old)).toEqual({status:'created'});
      const restarted=await createFeedbackStore(options);
      expect(await restarted.append(old)).toEqual({status:'duplicate'});
      expect(await restarted.append({...old,eventId:'old-event-2'})).toEqual({status:'created'});
      expect(await restarted.append({...old,eventId:'bad',catalogRevision:'invented'})).toMatchObject({status:'invalid'});
      expect(await restarted.append({...old,eventId:'wrong',assignedDifficulty:'hard'})).toMatchObject({status:'invalid'});
      expect((await readFile(options.filePath,'utf8')).trim().split('\n')).toHaveLength(2);
      expect(restarted.summary()).toMatchObject({historicalLines:1,corruptedLines:0});
    } finally { await rm(directory,{recursive:true}); }
  });
  it('rejects mutation of a registered catalog revision', async () => {
    const directory=await mkdtemp(join(tmpdir(),'mindbattle-complaint-history-'));
    try {
      const options={filePath:join(directory,'feedback.ndjson'),questions:new Map([['q','easy']]),catalogRevision:'catalog'};
      await createFeedbackStore(options);
      await expect(createFeedbackStore({...options,questions:new Map([['q','hard']])})).rejects.toThrow('Conflicting');
    } finally {await rm(directory,{recursive:true});}
  });
});
