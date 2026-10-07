import type { NetworkSnapshot } from "../../src/network/protocol";
const positions = ["up", "right", "down", "left"] as const;
export const seed = "phone-reveal-qa-v1";
export function snapshot(count: number): NetworkSnapshot {
  const players = Array.from({length:count}, (_, index) => ({id:`player-${index + 1}` as const, name:`Александр ${index + 1} Константинопольский`, connected:true, departed:index === count - 1}));
  const cards = players.map((p,index) => ({...p, score:index * 100, reserveMs:60_000, correct:2, incorrect:1, noAnswer:0, hasAnswered:index < count - 1, result:index === count - 1 ? "no-answer" as const : index % 4 === 0 ? "correct" as const : "wrong" as const, answerPosition:index === count - 1 ? null : positions[index % 4]}));
  return {
    code:"1234", title:"Тестовая игра", passwordProtected:false, epoch:1, phaseRevision:1, serverTime:0, role:"player", selfId:players[0].id,
    isLeader:true, leaderName:players[0].name, settings:{questionCount:9, answerTimeMs:20_000}, players,
    displayConnected:true, disconnected:[], phase:"reveal", paused:false, titles:{topic:"История науки", other:"Мировая культура", third:"География"}, canChoose:false, canVeto:false, canAnswer:false, questionNumber:3,
    revealedChoices:cards,
    view:{phase:"reveal", paused:false, teams:[cards[0]], question:{id:seed, topicId:"topic", prompt:"Какой из четырёх вариантов соответствует описанию научного открытия?", options:{up:"Верный вариант",right:"Второй вариант",down:"Третий вариант",left:"Четвёртый вариант"}, correctPosition:"up", explanation:["Основное объяснение раскрывается после завершения ответов всех участников."], answerNotes:positions.map((position,index)=>({position,answer:["Верный вариант","Второй вариант","Третий вариант","Четвёртый вариант"][index],note:"Подробная справка описывает конкретный вариант ответа и помогает разобраться в вопросе. Она остаётся читаемой на узком экране, переносится на несколько строк и доступна вместе со справками ко всем остальным вариантам."}))}}
  };
}
