import { useState } from "react";
import { GAMEPAD_GLYPHS, type GamepadProfile } from "../adapters/gamepadProfiles";
import { MenuAction, MenuDialog } from "./menuUi";

const SOURCE = "/images/controls-devices-v1.png";
const DIRECTIONS = ["north", "east", "south", "west"] as const;
const POSITIONS = { north: "Верхний ответ", east: "Правый ответ", south: "Нижний ответ", west: "Левый ответ" };
// Coordinates refer to the immutable 1536×1024 generated source asset.
// Button names come from the same family profiles as runtime answer hints.
function DeviceCrop({ viewBox, label, marks }: {
  viewBox: string; label: string; marks: readonly { x: number; y: number; text: string; size?: number }[];
}) {
  return <svg className="help-device" viewBox={viewBox} role="img" aria-label={label}>
    <image href={SOURCE} width="1536" height="1024" />
    {marks.map(({ x, y, text, size = 25 }) => <g key={`${x}-${y}`}>
      <text x={x} y={y} textAnchor="middle" dominantBaseline="central" fontSize={size} className="help-device-label">{text}</text>
    </g>)}
  </svg>;
}

export function ControlsHelp({ back }: { back: () => void }) {
  const [page, setPage] = useState<"keyboard" | "pad">("keyboard");
  const [family, setFamily] = useState<GamepadProfile>("xbox");
  const [missing, setMissing] = useState(false);
  const glyph = GAMEPAD_GLYPHS[family].answer;
  const pauseLabel = family === "playstation" ? "Options" : family === "nintendo" ? "+" : "Start";
  return <MenuDialog wide title="Управление в игре" back={back} footer={<MenuAction onClick={back}>Назад</MenuAction>}>
    <div className="help-tabs"><MenuAction onClick={() => setPage("keyboard")} aria-pressed={page === "keyboard"}>Клавиатура и мышь</MenuAction><MenuAction onClick={() => setPage("pad")} aria-pressed={page === "pad"}>Геймпад</MenuAction></div>
    <img hidden src={SOURCE} alt="" onError={() => setMissing(true)} />
    {missing && <p role="status">Не удалось загрузить иллюстрацию управления. Откройте справку снова после восстановления файлов игры.</p>}
    <div className="controls-help-content">
      {page === "keyboard" ? <>
        <h3>Клавиши ответов</h3>
        <p>Нажмите клавишу со стороны нужного ответа на экране.</p>
        <div className="help-answer-groups">
          <section className="help-control-card"><h4>WASD</h4>
            {!missing && <DeviceCrop viewBox="170 201 170 87" label="Клавиши W сверху, D справа, S снизу, A слева" marks={[{ x:244,y:225,text:"W" },{ x:297,y:263,text:"D" },{ x:252,y:263,text:"S" },{ x:205,y:263,text:"A" }]} />}
            <div className="help-answer-map">{DIRECTIONS.map((d,i)=><div key={d}><kbd>{["W","D","S","A"][i]}</kbd><span>{POSITIONS[d]}</span></div>)}</div>
          </section>
          <section className="help-control-card"><h4>Стрелки</h4>
            {!missing && <DeviceCrop viewBox="851 276 165 100" label="Клавиши стрелок вверх, вправо, вниз и влево" marks={[{ x:932,y:300,text:"↑" },{ x:980,y:342,text:"→" },{ x:934,y:342,text:"↓" },{ x:887,y:342,text:"←" }]} />}
            <div className="help-answer-map">{DIRECTIONS.map((d,i)=><div key={d}><kbd>{["↑","→","↓","←"][i]}</kbd><span>{POSITIONS[d]}</span></div>)}</div>
          </section>
        </div>
        <p>В командной игре WASD и стрелки принадлежат разным назначенным командам. В одиночной игре можно использовать любой набор.</p>
        <div className="help-action-grid">
          <section className="help-control-card"><h4>Выбор и продолжение</h4>
            {!missing && <DeviceCrop viewBox="269 315 340 60" label="Клавиша Space" marks={[{ x:439,y:343,text:"Space",size:27 }]} />}
            <div className="help-key-pair">{!missing && <><DeviceCrop viewBox="737 242 109 43" label="Клавиша Enter" marks={[{ x:798,y:263,text:"Enter",size:19 }]} /><DeviceCrop viewBox="718 281 127 37" label="Правый Shift" marks={[{ x:783,y:300,text:"Shift",size:19 }]} /></>}</div>
            <p><kbd>Space</kbd> — подтверждение и продолжение для команды WASD; <kbd>правый Shift</kbd> — для команды со стрелками.</p>
            <p>В одиночной игре <kbd>A / ←</kbd> и <kbd>D / →</kbd> меняют тему или риск; <kbd>Enter / Space</kbd> подтверждают выбор и продолжают после ответа.</p>
            <p>В командной игре <kbd>A / ←</kbd> и <kbd>D / →</kbd> меняют тему; в бонусе <kbd>W / ↑</kbd> отменяют свой выбор.</p>
          </section>
          <section className="help-control-card"><h4>Пауза и мышь</h4>
            <div className="help-small-devices">{!missing && <><DeviceCrop viewBox="109 124 67 52" label="Клавиша Esc" marks={[{ x:144,y:145,text:"Esc",size:17 }]} /><DeviceCrop viewBox="1270 130 205 285" label="Левая кнопка мыши: выбор экранного ответа" marks={[{ x:1325,y:182,text:"ЛКМ",size:22 }]} /></>}</div>
            <p><kbd>Esc</kbd> — пауза партии.</p><p><kbd>ЛКМ / касание</kbd> — выбрать ответ и игровые действия на экране в одиночной и сетевой игре.</p>
          </section>
        </div>
      </> : <>
        <label className="help-family">Обозначения контроллера<select value={family} onChange={e=>setFamily(e.target.value as GamepadProfile)}><option value="xbox">Xbox</option><option value="playstation">PlayStation</option><option value="nintendo">Nintendo</option><option value="universal">По положению кнопок</option></select></label>
        {!missing && <DeviceCrop viewBox="440 487 650 405" label={`Геймпад: ${glyph.north} сверху, ${glyph.east} справа, ${glyph.south} снизу, ${glyph.west} слева; крестовина слева; ${pauseLabel} справа от сенсорной панели`} marks={[
          { x:948,y:571,text:glyph.north,size:30 },{ x:986,y:610,text:glyph.east,size:30 },{ x:948,y:648,text:glyph.south,size:30 },{ x:908,y:610,text:glyph.west,size:30 },
          { x:584,y:584,text:"↑",size:24 },{ x:611,y:609,text:"→",size:24 },{ x:583,y:638,text:"↓",size:24 },{ x:556,y:609,text:"←",size:24 },{ x:885,y:550,text:pauseLabel,size:21 }
        ]} />}
        <h3>Кнопки ответов</h3>
        <div className="help-answer-map help-answer-map--pad">{DIRECTIONS.map(d=><div key={d}><kbd>{glyph[d]}</kbd><span>{POSITIONS[d]}</span></div>)}</div>
        <div className="help-action-grid">
          <section className="help-control-card"><h4>Выбор темы и риска</h4><p><kbd>D-pad ← / →</kbd> — сменить вариант.</p><p><kbd>{glyph.south}</kbd> (нижняя кнопка) — подтвердить выбор и продолжить после ответа.</p><p>В командном бонусе <kbd>D-pad ↑</kbd> — отменить свой выбор.</p></section>
          <section className="help-control-card"><h4>Одиночная игра</h4><p><kbd>Start / Options / +</kbd> — пауза.</p><p>На вопрос также можно ответить стрелками крестовины: расположение соответствует ответам на экране.</p></section>
        </div>
      </>}
    </div>
  </MenuDialog>;
}
