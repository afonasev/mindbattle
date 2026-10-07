import type { NetworkSnapshot } from "../network/protocol";

export function phoneStatus(snapshot: NetworkSnapshot): { required: boolean; text: string } | null {
  if (snapshot.role !== "player" || snapshot.paused) return null;
  switch (snapshot.phase) {
    case "normal-topic":
      return snapshot.canChoose
        ? { required: true, text: "Выберите тему вопроса" }
        : { required: false, text: `Выбирает ${snapshot.chooserName ?? "другой игрок"}. Вы ждёте` };
    case "bonus-veto":
    case "final-veto":
      if (!snapshot.canVeto) return { required: false, text: "Другие игроки исключают темы. Вы ждёте" };
      return snapshot.ownVeto
        ? { required: false, text: `Вы исключили «${snapshot.titles[snapshot.ownVeto] ?? snapshot.ownVeto}». Ждём остальных. Можно заменить или снять запрет` }
        : { required: true, text: "Выберите тему, которую хотите исключить" };
    case "answering":
      if (snapshot.spectating) return { required: false, text: "Вы наблюдаете финальную битву. Ждём ответов участников" };
      if (snapshot.ownAnswer) return { required: false, text: "Ответ принят. Ждём остальных. Его можно изменить до раскрытия" };
      return snapshot.canAnswer
        ? { required: true, text: "Выберите ответ" }
        : { required: false, text: "Время ответа истекло. Ждём остальных" };
    case "topic-confirmation":
      return { required: false, text: snapshot.isLeader ? "Ждём начала вопроса. Можно коснуться экрана, чтобы пропустить отсчёт" : "Ждём начала вопроса" };
    case "reveal":
    case "standings":
      return snapshot.isLeader
        ? { required: true, text: "Нажмите «Дальше», когда все готовы" }
        : { required: false, text: `Ждём ведущего: ${snapshot.leaderName}` };
    case "difficulty-feedback":
      return snapshot.isLeader
        ? { required: snapshot.view?.feedback?.stage !== "done", text: snapshot.view?.feedback?.stage === "done" ? "Сохраняем отзыв…" : "Выберите общий отзыв о вопросе" }
        : { required: false, text: `Ведущий ${snapshot.leaderName} собирает общий отзыв. Вы ждёте` };
    case "finished":
      return snapshot.isLeader
        ? { required: true, text: "Выберите: сыграть ещё или выйти в меню" }
        : { required: false, text: `Ждём ведущего: ${snapshot.leaderName}` };
    default: return null;
  }
}
