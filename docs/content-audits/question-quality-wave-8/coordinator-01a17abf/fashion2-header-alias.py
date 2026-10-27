"""Only exact same-author fashion2 missing-cycle declaration; raw untouched."""
def bind(m,a,sp,ps,R):
 assert R==m.D/'source-fashion2'
 ap=m.D/'source-fashion2-peer-header-addendum/metadata.json';v=m.read(ap)
 assert v['sourceNativeId']==a['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']=='01a17ad1-7cae-7bf2-9de9-ece47ca0f4ac'
 assert v['topicId']==a['topicId']==sp['topicId']==ps['topicId']=='fashion'
 assert v['sourceOrder']==a['entries'][0]['sourceOrder']==2 and v['id']==a['entries'][0]['id']=='fashion-shirt-collar-buttons'
 assert v['cycle']==a['cycle']==sp['cycle']==0 and 'cycle' not in ps
 assert v['originalMissingHeaderFields']==['cycle'] and not v['rawBytesChanged'] and not v['sourceBodiesOrGroundsChanged'] and v['samePacketBinding']
 assert v['originalTask']==str(m.D/'source-fashion2-task.json') and m.read(v['originalTask'])['authorNativeId']==v['sourceNativeId']
 f=m.read(m.D/'fashion2-raw-freeze.json')
 for name,digest in v['rawFileSHA256Before'].items():
  assert m.raw(R/name)==digest==v['rawFileSHA256After'][name]==f['files'][name]
  assert v['originalPacketFiles'][name]=={'path':str(R/name),'sha256':digest}
 ps['cycle']=v['cycle']
 ps['technicalSameAuthorFashion2CycleHeader']={'addendum':str(ap),'addendumSHA256':m.raw(ap),'originalCycleAbsent':True,'rawUnchanged':True,'noSemanticJudgmentOrQualityCredit':True}
