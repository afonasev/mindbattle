import { test, expect } from "@playwright/test";
import type { NetworkSnapshot } from "../../src/network/protocol";
const positions = ["up", "right", "down", "left"] as const;
const seed = "phone-reveal-qa-v1";
function snapshot(count: number): NetworkSnapshot {
  const players = Array.from({length:count}, (_, index) => ({id:`player-${index + 1}` as const, name:`Александр ${index + 1} Константинопольский`, connected:true, departed:index === count - 1}));
  const cards = players.map((p,index) => ({...p, score:index * 100, reserveMs:60_000, correct:2, incorrect:1, noAnswer:0, hasAnswered:index < count - 1, result:index === count - 1 ? "no-answer" as const : index % 4 === 0 ? "correct" as const : "wrong" as const, answerPosition:index === count - 1 ? null : positions[index % 4]}));
  return {
    code:"1234", epoch:1, phaseRevision:1, serverTime:0, role:"player", selfId:players[0].id,
    isLeader:true, leaderName:players[0].name, settings:{questionCount:9, answerTimeMs:20_000}, players,
    displayConnected:true, disconnected:[], phase:"reveal", paused:false, titles:{topic:"История науки", other:"Мировая культура", third:"География"}, canChoose:false, canVeto:false, canAnswer:false, questionNumber:3,
    revealedChoices:cards,
    view:{phase:"reveal", paused:false, teams:[cards[0]], question:{id:seed, topicId:"topic", prompt:"Какой из четырёх вариантов соответствует описанию научного открытия?", options:{up:"Верный вариант",right:"Второй вариант",down:"Третий вариант",left:"Четвёртый вариант"}, correctPosition:"up", explanation:["Основное объяснение раскрывается после завершения ответов всех участников."], answerNotes:positions.map((position,index)=>({position,answer:["Верный вариант","Второй вариант","Третий вариант","Четвёртый вариант"][index],note:"Подробная справка описывает конкретный вариант ответа и помогает разобраться в вопросе. Она остаётся читаемой на узком экране, переносится на несколько строк и доступна вместе со справками ко всем остальным вариантам."}))}}
  };
}
for (const width of [360,760]) for (const count of [2,12]) {
  test(`phone reveal and states: ${width}px / ${count} players / ${seed}`, async ({page}, info) => {
    await page.setViewportSize({width,height:800});
    await page.emulateMedia({reducedMotion:"reduce"});
    let current = snapshot(count);
    await page.addInitScript(() => {
      localStorage.setItem("mindbattle-network-credentials-v1", JSON.stringify([{code:"1234", token:"qa-fixture",role:"player"}]));
      localStorage.setItem("mindbattle-network-preferences-v1", JSON.stringify({volume:0,muted:true,textSize:"normal",highContrast:false,reducedMotion:true}));
    });
    await page.route("**/api/network/stream?*", route => route.fulfill({contentType:"text/event-stream", body:`event: connected\ndata: {"generation":1}\n\ndata: ${JSON.stringify(current)}\n\n`}));
    await page.route("**/api/network/heartbeat?*", route => route.fulfill({json:{ok:true}}));
    await page.goto("/network?muted=1");
    await expect(page.locator(".network-explanation p strong")).toHaveCount(4);
    await expect(page.locator(".network-answers .wrong")).toHaveCount(count === 2 ? 0 : 3);
    await expect(page.locator(".network-answers small").first()).toContainText("Александр 1");
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({path:info.outputPath(`${seed}-reveal-${width}-${count}.png`),fullPage:true});
    current = {...current, phase:"standings", revealedChoices:undefined, view:{...current.view!,phase:"standings",question:undefined,standings:current.players.map((p,index)=>({teamId:p.id,rank:p.departed ? 0 : 1,score:100,correct:1,incorrect:2,noAnswer:1}))}};
    await page.reload();
    await expect(page.locator(".network-standings > div")).toHaveCount(count);
    await expect(page.locator(".network-standing--self")).toContainText("Александр 1 Константинопольский · Вы");
    await expect(page.locator(".network-standings")).toContainText("Выбыл");
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({path:info.outputPath(`${seed}-standings-${width}-${count}.png`),fullPage:true});
    current = {...current, phase:"bonus-veto", canVeto:true, titles:{topic:"История науки",other:"Мировая культура",third:"География"},view:{...current.view!,phase:"bonus-veto",standings:undefined,topicCandidates:["topic","other","third"]}};
    await page.reload();
    await expect(page.locator(".network-turn-status--required")).toHaveText("Выберите тему, которую хотите исключить");
    await expect(page.locator(".network-topics button").first()).toBeEnabled();
    await page.screenshot({path:info.outputPath(`${seed}-veto-action-${width}-${count}.png`),fullPage:true});
    current = {...current, ownVeto:"topic",vetoes:[{playerId:current.selfId!,name:current.leaderName,topicId:"topic"}]};
    await page.reload();
    await expect(page.locator(".network-turn-status--waiting")).toContainText("Вы исключили «История науки»");
    await expect(page.getByRole("button",{name:"Снять запрет",exact:true})).toBeEnabled();
    await expect(page.locator(".network-topics button").nth(1)).toBeEnabled();
    await page.screenshot({path:info.outputPath(`${seed}-veto-confirmed-${width}-${count}.png`),fullPage:true});
    current = {...current, canVeto:false, ownVeto:undefined};
    await page.reload();
    await expect(page.locator(".network-turn-status--waiting")).toHaveText("Другие игроки исключают темы. Вы ждёте");
    for (const button of await page.locator(".network-topics button").all()) await expect(button).toBeDisabled();
  });
}
