export const TOPIC_DEFINITIONS = [
  ["history-russia", "История России"],
  ["world-history", "Всемирная история"],
  ["geography-russia", "География России"],
  ["world-geography", "Мировая география"],
  ["russian-literature", "Русская литература"],
  ["world-literature", "Мировая литература"],
  ["russian-language", "Русский язык и выражения"],
  ["soviet-russian-cinema", "Кино СССР и России"],
  ["world-cinema", "Мировое кино"],
  ["tv-series", "Сериалы и телевидение"],
  ["russian-music", "Российская музыка"],
  ["world-pop-music", "Мировая популярная музыка"],
  ["classical-music", "Классическая музыка"],
  ["russian-culture", "Русская культура и традиции"],
  ["visual-art", "Изобразительное искусство"],
  ["architecture", "Архитектура"],
  ["physics", "Физика"],
  ["chemistry", "Химия"],
  ["biology", "Биология"],
  ["human-medicine", "Человек и медицина"],
  ["astronomy-space", "Астрономия и космос"],
  ["math-logic", "Математика и логика"],
  ["inventions-technology", "Изобретения и технологии"],
  ["computers-internet", "Компьютеры и интернет"],
  ["economics-money", "Экономика и деньги"],
  ["mythology-religions", "Мифология и религии мира"],
  ["world-cuisine", "Еда и кухни мира"],
  ["sports", "Спорт"],
  ["modern-video-games", "Современные видеоигры"],
  ["video-game-history", "История видеоигр, ретро и игровые консоли"]
] as const;

export const TOPIC_TITLE_BY_ID = Object.fromEntries(TOPIC_DEFINITIONS) as Readonly<
  Record<(typeof TOPIC_DEFINITIONS)[number][0], string>
>;
