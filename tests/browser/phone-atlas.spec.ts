import { test, expect } from '@playwright/test';
import { writeFileSync, readFileSync } from 'node:fs';
import { snapshot } from './qa-phoneSnapshot';
import quiz from '../../src/content/topics/video-game-history.json' with { type: 'json' };
import type { NetworkSnapshot } from '../../src/network/protocol';

const positions = ['up','right','down','left'] as const;
const q = quiz.questions.find(q => q.id === 'video-game-history-playstation-japan-year')!;
function state(phase: NetworkSnapshot['phase'], leader = true): NetworkSnapshot {
  const s = snapshot(12);
  const players = s.players.map((p,i) => ({...p,name:i === 0 ? 'Александр' : `Игрок ${i+1}`}));
  const teams = s.view!.teams.map(t => ({...t,name:'Александр',reserveMs:42_000,score:400,answerPosition:positions[q.correctIndex],result:'correct' as const}));
  return {...s, phase, isLeader:leader, players, leaderName:leader ? 'Александр':'Игрок 2', chooserName:'Игрок 2', difficulty:'medium',
    titles:{topic:'История видеоигр',other:'Океаны и моря',third:'Литература'},
    view:{...s.view!,phase:phase==='lobby'?'reveal':phase,teams,topicCandidates:['topic','other','third'],chooser:s.selfId,
      question:{id:q.id,topicId:'topic',prompt:q.prompt,options:Object.fromEntries(positions.map((p,i)=>[p,q.answers[i].text])) as Record<typeof positions[number],string>,
        correctPosition:positions[q.correctIndex],source:q.source,explanation:[q.explanation],answerNotes:positions.map((p,i)=>({position:p,answer:q.answers[i].text,note:q.answers[i].note}))}},
    revealedChoices:s.revealedChoices!.map((t,i)=>({...t,name:players[i].name,answerPosition:i===11?null:i===0?positions[q.correctIndex]:positions[i%4],result:i===11?'no-answer':i===0||i%4===q.correctIndex?'correct':'wrong'}))};
}
function answer(variant:'open'|'accepted'|'expired'|'reserve'|'spectator') {
  const s=state('answering',false); const {correctPosition,explanation,answerNotes,...question}=s.view!.question!;
  return {...s, canAnswer:variant!=='expired'&&variant!=='spectator',ownAnswer:variant==='accepted'?'up' as const:undefined,spectating:variant==='spectator',tieBreakNumber:variant==='spectator'?1:undefined,
    view:{...s.view!,question,baseRemainingMs:variant==='reserve'?0:15_000,
      teams:s.view!.teams.map(t=>({...t,hasAnswered:variant==='accepted',result:undefined,answerPosition:undefined,reserveMs:variant==='expired'?0:42_000,remainingMs:variant==='accepted'?undefined:variant==='expired'?0:variant==='reserve'?42_000:15_000}))}};
}
function results(finished:boolean,leader:boolean) {
  const s=state(finished?'finished':'standings',leader);
  return {...s,view:{...s.view!,question:undefined,winnerId:finished?s.selfId:undefined,standings:s.players.map((p,i)=>({teamId:p.id,rank:p.departed?0:i+1,score:1200-i*100,correct:4,incorrect:2,noAnswer:1}))}};
}
function revealResult(result:'wrong'|'no-answer'): NetworkSnapshot {
  const s=state('reveal',false);const position=result==='wrong'?'up' as const:null;
  return {...s,view:{...s.view!,teams:s.view!.teams.map(t=>({...t,result,answerPosition:position,hasAnswered:result==='wrong',reserveMs:result==='no-answer'?0:t.reserveMs}))},
    revealedChoices:s.revealedChoices!.map((t,i)=>i===0?{...t,result,answerPosition:position}:t)};
}
function feedback(stage:'choice'|'reasons'|'done',leader=true) {
  const s=state('difficulty-feedback',leader);
  return {...s,view:{...s.view!,question:undefined,feedback:{eventId:'atlas-feedback',questionId:q.id,assignedDifficulty:'medium' as const,stage,hasComplaint:stage==='choice'?null:true,complaintReasons:stage==='reasons'?['unclear-wording' as const]:[],complaintNote:'',cursor:0}}};
}
const topic=state('normal-topic');
const veto=state('bonus-veto');
const cases:Array<{id:string;title:string;s:NetworkSnapshot|null;overlay?:string;terminal?:string;accessible?:boolean}> = [
  {id:'01-entry',title:'Подключение',s:null},
  {id:'02-lobby',title:'Ожидание старта',s:{...state('lobby',false),view:undefined}},
  {id:'03-topic-choice',title:'Вы выбираете тему',s:{...topic,canChoose:true}},
  {id:'04-topic-wait',title:'Тему выбирает другой игрок',s:{...topic,canChoose:false}},
  {id:'05-veto',title:'Исключение бонусной темы',s:{...veto,canVeto:true}},
  {id:'06-veto-selected',title:'Запрет принят',s:{...veto,canVeto:true,ownVeto:'topic',vetoes:[{playerId:veto.selfId!,name:'Александр',topicId:'topic'}]}},
  {id:'07-veto-wait',title:'Ожидание чужих запретов',s:{...veto,canVeto:false}},
  {id:'08-confirmation',title:'Отсчёт перед вопросом',s:{...state('topic-confirmation'),view:{...state('topic-confirmation').view!,question:undefined,topicId:'topic',confirmationRemainingMs:3000}}},
  {id:'09-answer',title:'Выбор ответа',s:answer('open')},
  {id:'10-answer-accepted',title:'Ответ принят',s:answer('accepted')},
  {id:'11-reserve',title:'Расход запаса',s:answer('reserve')},
  {id:'12-expired',title:'Время истекло',s:answer('expired')},
  {id:'13-reveal-leader',title:'Раскрытие · ведущий',s:state('reveal')},
  {id:'14-reveal-player',title:'Раскрытие · участник',s:state('reveal',false)},
  {id:'15-feedback',title:'Отзыв · ведущий',s:feedback('choice')},
  {id:'16-feedback-reasons',title:'Причины жалобы',s:feedback('reasons')},
  {id:'17-feedback-wait',title:'Ожидание отзыва',s:feedback('choice',false)},
  {id:'18-feedback-save',title:'Сохранение отзыва',s:feedback('done')},
  {id:'19-feedback-error',title:'Ошибка отправки отзыва',s:{...feedback('done'),feedbackError:'Проверка восстановления'},overlay:'error'},
  {id:'20-standings-leader',title:'Итоги этапа · ведущий',s:results(false,true)},
  {id:'21-standings-player',title:'Итоги этапа · участник',s:results(false,false)},
  {id:'22-final-topic',title:'Исключение финальных тем',s:{...state('final-veto'),tieBreakNumber:1,canVeto:false}},
  {id:'23-final-answer',title:'Финальный вопрос',s:{...answer('open'),tieBreakNumber:1}},
  {id:'24-spectator',title:'Наблюдатель финала',s:answer('spectator')},
  {id:'25-finished-leader',title:'Победитель · ведущий',s:results(true,true)},
  {id:'26-finished-player',title:'Победитель · участник',s:results(true,false)},
  {id:'27-one-left',title:'Остался один игрок',s:{...results(true,true),endReason:'one-player-left'}},
  {id:'28-scoreboard',title:'Текущий счёт',s:{...state('reveal',false),scoreboard:state('reveal').players.map((p,i)=>({teamId:p.id,name:p.name,rank:i+1,score:400-i*10,departed:p.departed}))},overlay:'scoreboard'},
  {id:'29-menu',title:'Меню участника',s:state('reveal',false),overlay:'menu'},
  {id:'30-settings',title:'Настройки',s:state('reveal',false),overlay:'settings'},
  {id:'31-pause-leader',title:'Общая пауза · ведущий',s:{...state('reveal'),paused:true}},
  {id:'32-pause-wait',title:'Общая пауза · участник',s:{...state('reveal',false),paused:true}},
  {id:'33-disconnected',title:'Другой игрок отключился',s:{...state('reveal'),paused:true,disconnected:[{id:'player-2',name:'Игрок 2',connected:false,departed:false}]}},
  {id:'34-display-lost',title:'Общий экран отключился',s:{...state('reveal'),paused:true,displayConnected:false}},
  {id:'35-room-closed',title:'Комната закрыта',s:state('reveal'),terminal:'expired'},
  {id:'36-other-tab',title:'Открыто в другой вкладке',s:state('reveal'),terminal:'replaced'},
  {id:'37-join-error',title:'Неверный код комнаты',s:null,overlay:'join-error'},
  {id:'38-final-reveal',title:'Раскрытие финального вопроса',s:{...state('reveal'),tieBreakNumber:1}},
  {id:'39-reveal-wrong',title:'Раскрытие · неверный ответ',s:revealResult('wrong')},
  {id:'40-reveal-no-answer',title:'Раскрытие · нет ответа',s:revealResult('no-answer')}
];

for(const width of [360,760]) test(`mobile network complete presentation atlas ${width}`, async ({page},info)=>{
  test.setTimeout(120_000);
  await page.setViewportSize({width,height:800});
  await page.emulateMedia({reducedMotion:'reduce'});
  let current=cases[0];const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/api/network/stream?*',route=>route.fulfill({contentType:'text/event-stream',body:current.terminal?`event: ${current.terminal}\ndata: {}\n\n`:`event: connected\ndata: {"generation":1}\n\ndata: ${JSON.stringify(current.s)}\n\n`}));
  await page.route('**/api/network/join',route=>route.fulfill({status:404,json:{error:'Комната не найдена'}}));
  await page.route('**/api/network/heartbeat?*',route=>route.fulfill({json:{ok:true}}));
  const pictures:Array<{id:string;title:string;path:string}>=[];
  for (const item of [...cases,...cases.filter(c=>['03-topic-choice','09-answer','13-reveal-leader'].includes(c.id)).map(c=>({...c,id:'a'+c.id,title:c.title+' · крупный текст / контраст',accessible:true}))]) {
    current=item;
    await page.goto('/network?muted=1');
    await page.evaluate(({credential,accessible})=>{
      if(credential)localStorage.setItem('mindbattle-network-credentials-v1',JSON.stringify([{code:'1234',token:'mobile-atlas',role:'player'}]));else localStorage.removeItem('mindbattle-network-credentials-v1');
      localStorage.setItem('mindbattle-network-preferences-v1',JSON.stringify({muted:true,musicVolume:0,effectsVolume:0,textSize:accessible?'large':'normal',highContrast:accessible,reducedMotion:true}));
    },{credential:!!item.s,accessible:!!item.accessible});
    await page.reload();
    if(item.s) await expect(page.getByRole('button',{name:item.terminal?'Вернуться к подключению':'Меню',exact:true})).toBeVisible();
    else await expect(page.getByRole('heading',{name:'Вступить в игру'})).toBeVisible();
    if(item.overlay==='join-error'){await page.getByLabel('Код комнаты').fill('9999');await page.getByLabel('Ваше имя').fill('Александр');await page.getByRole('button',{name:'Подключиться',exact:true}).click();await expect(page.getByRole('alert')).toContainText('Комната не найдена');}
    if(item.overlay==='scoreboard')await page.getByRole('button',{name:'Показать текущий счёт'}).click();
    if(item.overlay==='menu'||item.overlay==='settings'){
      await page.getByRole('button',{name:'Меню',exact:true}).click();
      if(item.overlay==='settings')await page.getByRole('button',{name:'Настройки',exact:true}).click();
    }
    if(item.id==='09-answer'){await expect(page.locator('.network-player-card .network-reserve strong')).toHaveText('15 с');await expect(page.locator('.network-reserve-balance')).toHaveText('Запас 42 с');}
    if(item.s?.phase==='answering')await expect(page.locator('.network-cards')).not.toContainText('Время:');
    if(item.id==='03-topic-choice'){
      await expect(page.getByText('Выберите тему',{exact:true})).toHaveCount(1);
      await expect(page.getByText('Выберите тему вопроса',{exact:true})).toHaveCount(0);
    }
    if(item.s?.view?.teams.length&&!item.terminal){
      await expect(page.locator('.network-header .network-reserve')).toHaveCount(0);
      await expect(page.locator('.network-player-card .network-reserve')).toHaveCount(['standings','finished'].includes(item.s.phase)?0:1);
      expect(await page.locator('.network-header').evaluate(e=>e.getBoundingClientRect().height)).toBeLessThanOrEqual(80);
    }
    await page.evaluate(()=>document.fonts.ready);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
    expect(errors).toEqual([]);
    const path=info.outputPath(`${item.id}-${width}.png`);await page.screenshot({path,fullPage:true});pictures.push({id:item.id,title:item.title,path});
  }
  const cards=pictures.map(p=>`<article><h2>${p.id.slice(0,2)}. ${p.title}</h2><a href="${p.id}-${width}.png"><img src="data:image/png;base64,${readFileSync(p.path).toString('base64')}"></a></article>`).join('');
  const style=`body{margin:0;background:#0a111c;color:#eaf4ff;font:14px system-ui;padding:24px}h1{font-size:24px}section{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}article{background:#142031;padding:12px;border-radius:10px}h2{font-size:14px;margin:0 0 12px}img{width:100%;height:auto;display:block}a{color:inherit}@media(max-width:800px){section{grid-template-columns:repeat(2,minmax(0,1fr))}}`;
  writeFileSync(info.outputPath(`gallery-${width}.html`),`<!doctype html><meta charset="utf-8"><title>Мобильный сетевой интерфейс</title><style>${style}</style><h1>Мобильный сетевой интерфейс · ${width}px · все состояния</h1><p>Детерминированные UI-снимки; звук выключен. Полные изображения встроены; клик открывает PNG.</p><section>${cards}</section>`);
  writeFileSync(info.outputPath(`manifest-${width}.json`),JSON.stringify(pictures,null,2));
  // A compact contact sheet for reviewing the main flow without losing the full PNGs.
  await page.setViewportSize({width:1140,height:1000});
  const selected=pictures.filter(p=>['03-topic-choice','04-topic-wait','09-answer','10-answer-accepted','13-reveal-leader','20-standings-leader'].includes(p.id));
  await page.setContent(`<style>${style}img{height:600px;object-fit:contain;object-position:top}section{grid-template-columns:repeat(3,1fr)}</style><h1>Основные состояния · ${width}px</h1><section>${selected.map(p=>`<article><h2>${p.title}</h2><img src="data:image/png;base64,${readFileSync(p.path).toString('base64')}"></article>`).join('')}</section>`);
  await page.screenshot({path:info.outputPath(`overview-${width}.png`),fullPage:true});
});
