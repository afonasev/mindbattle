import { useRef, useState } from "react";
import { GAMEPAD_GLYPHS, type GamepadProfile } from "../adapters/gamepadProfiles";
import { MenuAction, MenuDialog } from "./menuUi";

const SOLO_ART = "/images/controls-simplified-v2.png";
const KEY_ART = "/images/controls-keycaps-v2.png";
const PAD_ART = "/images/controls-devices-v1.png";
const DIRECTIONS = ["north", "east", "south", "west"] as const;
const POSITIONS = { north: "Верхний ответ", east: "Правый ответ", south: "Нижний ответ", west: "Левый ответ" };

// Transparent generated sprites follow the approved keycap style. Full source art
// stays versioned; SVG viewBox only selects the relevant sprite at display time.
const BOXES = { wasd:"8 170 369 255", arrows:"392 170 377 255", ad:"800 231 321 159", horizontal:"1210 231 320 159", enter:"18 674 349 161", space:"402 674 349 161", shift:"784 674 359 161", esc:"1258 674 174 161" } as const;
function KeyArt({ kind, label }: { kind: keyof typeof BOXES; label: string }) {
  return <svg className="simple-key-art" viewBox={BOXES[kind]} role="img" aria-label={label}>
    <image href={KEY_ART} width="1536" height="1024" />
  </svg>;
}

function PadArt({ glyph, pauseLabel }: { glyph: typeof GAMEPAD_GLYPHS.xbox.answer; pauseLabel: string }) {
  const marks = [
    [948,571,glyph.north],[986,610,glyph.east],[948,648,glyph.south],[908,610,glyph.west],
    [584,584,"↑"],[611,609,"→"],[583,638,"↓"],[556,609,"←"],[885,550,pauseLabel],
  ] as const;
  return <svg className="simple-pad-art" viewBox="440 487 650 405" role="img" aria-label={`Геймпад: ${glyph.north} сверху, ${glyph.east} справа, ${glyph.south} снизу, ${glyph.west} слева`}>
    <image href={PAD_ART} width="1536" height="1024" />
    {marks.map(([x,y,text],i)=><text className="simple-pad-label" key={i} x={x} y={y} textAnchor="middle" dominantBaseline="central" fontSize={i===8?21:28}>{text}</text>)}
  </svg>;
}


function ControlsPoster({ back, team, arrows, gamepad }: { back: () => void; team: () => void; arrows: () => void; gamepad: () => void }) {
  const [zoom,setZoom] = useState(false);
  const [missing,setMissing] = useState(false);
  const viewport = useRef<HTMLDivElement>(null);
  const pan = (direction: number) => viewport.current?.scrollBy({left:direction*220,behavior:"smooth"});
  return <MenuDialog wide className="controls-poster-dialog" title="Управление в игре" back={back} footer={<div className="poster-footer">
    {zoom && <MenuAction className="poster-pan" aria-label="Сдвинуть картинку влево" onClick={()=>pan(-1)}>←</MenuAction>}
    <MenuAction onClick={back}>Назад</MenuAction>
    {!missing && <MenuAction onClick={()=>setZoom(value=>!value)} aria-pressed={zoom}>{zoom?"Вместить":"Увеличить"}</MenuAction>}
    {zoom && <MenuAction className="poster-pan" aria-label="Сдвинуть картинку вправо" onClick={()=>pan(1)}>→</MenuAction>}
  </div>}>
    <div className="poster-help">
      <div className="poster-toolbar"><div className="help-tabs"><MenuAction aria-pressed>Клавиатура и мышь</MenuAction><MenuAction onClick={gamepad}>Геймпад</MenuAction></div>
        <label>Набор клавиш<select value="wasd" onChange={arrows}><option value="wasd">WASD</option><option value="arrows">Стрелки</option></select></label>
      </div>
      <div ref={viewport} className="poster-viewport" data-menu-scroll-area tabIndex={0} role="region" aria-label="Картинка управления: прокрутка">
        {missing ? <div className="poster-fallback"><p role="status">Не удалось загрузить иллюстрацию управления.</p><p>W — верхний ответ; D — правый; S — нижний; A — левый.</p><p>A и D — тема и риск. Enter — подтвердить и продолжить. Esc — пауза.</p><MenuAction onClick={team}>Командная игра</MenuAction></div> : <div className={`poster-frame ${zoom?"poster-frame--zoom":""}`}>
          <img className="controls-ready-poster" src={SOLO_ART} width="1536" height="1024" draggable={false} onError={()=>setMissing(true)} alt="Управление: одиночная игра. W — верхний ответ, D — правый, S — нижний, A — левый. A и D — тема и риск. Enter — подтвердить и продолжить. Esc — пауза. Ответы также можно выбирать мышью или касанием." />
          <MenuAction className="poster-mode poster-mode--solo" aria-pressed><span className="poster-sr-only">Одиночная игра</span></MenuAction>
          <MenuAction className="poster-mode poster-mode--team" onClick={team}><span className="poster-sr-only">Командная игра</span></MenuAction>
        </div>}
      </div>
    </div>
  </MenuDialog>;
}

export function ControlsHelp({ back }: { back: () => void }) {
  const [device,setDevice] = useState<"keyboard" | "pad">("keyboard");
  const [mode,setMode] = useState<"solo" | "team">("solo");
  const [layout,setLayout] = useState<"wasd" | "arrows">("wasd");
  const [family,setFamily] = useState<GamepadProfile>("xbox");
  const [failed,setFailed] = useState<string[]>([]);
  const glyph = GAMEPAD_GLYPHS[family].answer;
  const pauseLabel = family==="playstation"?"Options":family==="nintendo"?"+":"Start";
  const arrows = layout==="arrows";
  const missing = (device==="pad"?[PAD_ART]:[KEY_ART]).some(p=>failed.includes(p));
  const keys = arrows?["↑","→","↓","←"]:["W","D","S","A"];
  const confirm = mode==="solo"?"Enter":arrows?"Правый Shift":"Space";
  if (device==="keyboard" && mode==="solo" && layout==="wasd") return <ControlsPoster back={back} team={()=>setMode("team")} arrows={()=>setLayout("arrows")} gamepad={()=>setDevice("pad")} />;
  return <MenuDialog wide title="Управление в игре" back={back} footer={<MenuAction onClick={back}>Назад</MenuAction>}>
    <div className="help-tabs"><MenuAction onClick={()=>setDevice("keyboard")} aria-pressed={device==="keyboard"}>Клавиатура и мышь</MenuAction><MenuAction onClick={()=>setDevice("pad")} aria-pressed={device==="pad"}>Геймпад</MenuAction></div>
    <div className="simple-help-modes" aria-label="Режим игры"><MenuAction onClick={()=>setMode("solo")} aria-pressed={mode==="solo"}>Одиночная игра</MenuAction><MenuAction onClick={()=>setMode("team")} aria-pressed={mode==="team"}>Командная игра</MenuAction></div>
    {[SOLO_ART,KEY_ART,PAD_ART].map(src=><img hidden key={src} src={src} alt="" onError={()=>setFailed(old=>old.includes(src)?old:[...old,src])} />)}
    <div className="simple-help">
      {device==="keyboard" ? <div className="simple-help-picker"><label>Набор клавиш<select value={layout} onChange={e=>setLayout(e.target.value as typeof layout)}><option value="wasd">WASD</option><option value="arrows">Стрелки</option></select></label></div> : <div className="simple-help-picker"><label>Обозначения контроллера<select value={family} onChange={e=>setFamily(e.target.value as GamepadProfile)}><option value="xbox">Xbox</option><option value="playstation">PlayStation</option><option value="nintendo">Nintendo</option><option value="universal">По положению кнопок</option></select></label></div>}
      <h3>Выберите ответ</h3>
      {missing && <p role="status">Не удалось загрузить иллюстрацию управления. Подписи действий доступны ниже.</p>}
      {device==="keyboard" ? <>
        <div className="simple-answer-diagram" aria-label={`Ответы: ${layout}`}>
          {DIRECTIONS.map((d,i)=><span className={`simple-answer-label simple-answer-label--${d}`} key={d}><kbd>{keys[i]}</kbd>{POSITIONS[d]}</span>)}
          {!missing && <KeyArt kind={arrows?"arrows":"wasd"} label={arrows?"Стрелки: вверх, вправо, вниз, влево":"Клавиши W сверху, D справа, S снизу, A слева"} />}
        </div>
        <div className="simple-help-actions">
          <div><div className="simple-action-art">{!missing?<KeyArt kind={arrows?"horizontal":"ad"} label={arrows?"Клавиши влево и вправо":"Клавиши A и D"} />:<kbd>{arrows?"← →":"A D"}</kbd>}</div><span>{mode==="solo"?"Тема и риск":"Выбор темы"}</span></div>
          <div><div className="simple-action-art">{!missing ? <KeyArt kind={mode==="solo"?"enter":arrows?"shift":"space"} label={confirm}/>:<kbd>{confirm}</kbd>}</div><span>Подтвердить · дальше</span>{mode==="team" && <small>{confirm}</small>}</div>
          {mode==="team" && <div><div className="simple-action-art"><kbd>{arrows?"↑":"W"}</kbd></div><span>Отменить выбор в бонусе</span></div>}
          <div><div className="simple-action-art">{!missing?<KeyArt kind="esc" label="Клавиша Esc"/>:<kbd>Esc</kbd>}</div><span>Пауза</span></div>
        </div>
        <p className="simple-help-note">{mode==="solo"?"Ответы также можно выбирать мышью или касанием.":"Каждая команда использует назначенный ей набор клавиш."}</p>
      </> : <>
        {!missing && <PadArt glyph={glyph} pauseLabel={pauseLabel} />}
        <div className="simple-pad-map">{DIRECTIONS.map(d=><div key={d}><kbd>{glyph[d]}</kbd><span>{POSITIONS[d]}</span></div>)}</div>
        <div className="simple-help-actions simple-help-actions--pad">
          <div><kbd>D-pad ← →</kbd><span>{mode==="solo"?"Тема и риск":"Выбор темы"}</span></div>
          <div><kbd>{glyph.south}</kbd><span>Подтвердить · дальше</span></div>
          {mode==="team"?<div><kbd>D-pad ↑</kbd><span>Отменить выбор в бонусе</span></div>:<div><kbd>{pauseLabel}</kbd><span>Пауза</span></div>}
        </div>
        <p className="simple-help-note">Крестовина также выбирает ответ по его положению.</p>
      </>}
    </div>
  </MenuDialog>;
}
