import { createHash } from 'node:crypto';
import { test, expect } from '@playwright/test';

for (const [width,height] of [[1280,900],[360,640]]) test(`specific control legends fit ${width}x${height}`,async({page},info)=>{
  await page.setViewportSize({width,height});
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await page.getByRole('button',{name:'Справка по управлению',exact:true}).click();
  const dialog=page.getByRole('dialog',{name:'Управление в игре'});
  const poster=dialog.locator('.controls-ready-poster');
  await expect(poster).toBeVisible();
  await expect(poster).toHaveAttribute('src','/images/controls-simplified-v2.png');
  await expect(poster).toHaveAccessibleName(/W — верхний ответ, D — правый, S — нижний, A — левый/);
  await expect(poster).toHaveAccessibleName(/Enter — подтвердить и продолжить. Esc — пауза/);
  await expect(dialog.locator('svg,.simple-answer-label,.simple-help-actions')).toHaveCount(0);
  const image=await page.request.get('/images/controls-simplified-v2.png');
  expect(createHash('sha256').update(await image.body()).digest('hex')).toBe('5a4821bc3b89e60a26f3e8a50016a0e839621997aadad3dff253a23f70bddbd1');
  expect(await poster.evaluate((img:HTMLImageElement)=>[img.naturalWidth,img.naturalHeight])).toEqual([1536,1024]);
  await expect(dialog.getByRole('status')).toHaveCount(0);
  await page.screenshot({path:info.outputPath(`keyboard-${width}.png`)});
  await dialog.getByRole('button',{name:'Увеличить',exact:true}).click();
  const viewport=dialog.getByRole('region',{name:'Картинка управления: прокрутка',exact:true});
  expect((await poster.boundingBox())!.width).toBeGreaterThanOrEqual(1000);
  await expect(dialog.getByRole('button',{name:'Назад',exact:true})).toBeInViewport();
  if(width===360){
    await dialog.getByRole('button',{name:'Сдвинуть картинку вправо'}).click();
    await expect.poll(()=>viewport.evaluate(e=>e.scrollLeft)).toBeGreaterThan(100);
    await dialog.getByRole('button',{name:'Сдвинуть картинку влево'}).click();
    await expect.poll(()=>viewport.evaluate(e=>e.scrollLeft)).toBeLessThan(20);
  }
  await page.screenshot({path:info.outputPath(`poster-zoom-${width}.png`)});
  await dialog.getByRole('button',{name:'Вместить',exact:true}).click();
  await dialog.getByRole('button',{name:'Командная игра',exact:true}).click();
  await expect(dialog.getByText('Тема и риск',{exact:true})).toHaveCount(0);
  await expect(dialog.getByText('Отменить выбор в бонусе',{exact:true})).toBeVisible();
  await dialog.getByLabel('Набор клавиш').selectOption('arrows');
  await expect(dialog.locator('.simple-answer-label')).toHaveText(['↑Верхний ответ','→Правый ответ','↓Нижний ответ','←Левый ответ']);
  await expect(dialog.getByRole('img',{name:'Правый Shift',exact:true})).toBeVisible();
  await page.screenshot({path:info.outputPath(`team-arrows-${width}.png`)});
  await dialog.getByRole('button',{name:'Геймпад',exact:true}).click();
  const family=dialog.getByLabel('Обозначения контроллера');
  for(const [value,glyphs] of [['xbox',['Y','B','A','X']],['playstation',['△','○','×','□']],['nintendo',['X','A','B','Y']]] as const){
    await family.selectOption(value);
    await expect(dialog.locator('.simple-pad-label').first()).toHaveText(glyphs[0]);
    await expect(dialog.locator('.simple-pad-label').last()).toHaveText(value==='playstation'?'Options':value==='nintendo'?'+':'Start');
    await expect(dialog.locator('.simple-pad-map kbd')).toHaveText([...glyphs]);
  }
  await expect(dialog.locator('.simple-help-actions').getByText('Пауза',{exact:true})).toHaveCount(0);
  await dialog.getByRole('button',{name:'Одиночная игра',exact:true}).click();
  await expect(dialog.locator('.simple-help-actions').getByText('Пауза',{exact:true})).toBeVisible();
  await expect(dialog.getByText('Отменить выбор в бонусе',{exact:true})).toHaveCount(0);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth && document.documentElement.scrollHeight<=innerHeight+1)).toBe(true);
  await expect(dialog.getByRole('button',{name:'Назад',exact:true})).toBeInViewport();
  await page.screenshot({path:info.outputPath(`pad-${width}.png`)});
  await page.keyboard.press('Escape');
  await expect(page.getByRole('button',{name:'Справка по управлению',exact:true})).toBeFocused();
});

test('pause settings and nested help keep both return actions reachable',async({page})=>{
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Одиночная игра',exact:true}).click();
  await page.keyboard.press('Escape');
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await expect(page.getByRole('button',{name:'Назад',exact:true})).toBeInViewport();
  await page.getByRole('button',{name:'Справка по управлению',exact:true}).click();
  await page.getByRole('dialog',{name:'Управление в игре'}).getByRole('button',{name:'Назад',exact:true}).click();
  await expect(page.getByRole('button',{name:'Назад',exact:true})).toBeInViewport();
  await page.getByRole('button',{name:'Назад',exact:true}).click();
  await expect(page.getByRole('button',{name:'Продолжить',exact:true})).toBeVisible();
});

test('missing artwork is reported while bindings remain readable',async({page})=>{
  await page.route('**/images/controls-simplified-v2.png',route=>route.abort());
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await page.getByRole('button',{name:'Справка по управлению',exact:true}).click();
  await expect(page.getByRole('status')).toContainText('Не удалось загрузить');
  await expect(page.locator('.poster-fallback')).toContainText('W — верхний ответ; D — правый; S — нижний; A — левый');
  await expect(page.locator('.poster-fallback')).toContainText('Enter — подтвердить и продолжить. Esc — пауза');
  await expect(page.getByRole('dialog',{name:'Управление в игре'}).getByRole('button',{name:'Назад',exact:true})).toBeInViewport();
});

test('virtual pad switches help mode and returns to the invoking settings action',async({page})=>{
  await page.addInitScript(()=>{
    const pad={id:'Xbox standard',index:0,mapping:'standard',connected:true,buttons:Array.from({length:17},()=>({pressed:false,value:0,touched:false})),axes:[0,0,0,0],timestamp:0};
    (window as any).__helpPad=pad;Object.defineProperty(navigator,'getGamepads',{value:()=>[pad]});
  });
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await page.getByRole('button',{name:'Справка по управлению',exact:true}).click();
  const press=async(index:number)=>{await page.evaluate(i=>{(window as any).__helpPad.buttons[i].pressed=true;},index);await page.waitForTimeout(50);await page.evaluate(i=>{(window as any).__helpPad.buttons[i].pressed=false;},index);await page.waitForTimeout(50);};
  const team=page.getByRole('button',{name:'Командная игра',exact:true});
  for(let i=0;i<10 && !await team.evaluate(e=>e===document.activeElement);i++) await press(13);
  await expect(page.getByRole('button',{name:'Командная игра',exact:true})).toBeFocused();
  await press(0);
  await expect(page.getByRole('button',{name:'Командная игра',exact:true})).toHaveAttribute('aria-pressed','true');
  await expect(page.getByText('Отменить выбор в бонусе',{exact:true})).toBeVisible();
  await press(1);
  await expect(page.getByRole('button',{name:'Справка по управлению',exact:true})).toBeFocused();
});
