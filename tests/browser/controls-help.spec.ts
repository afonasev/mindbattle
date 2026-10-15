import { test, expect } from '@playwright/test';

for (const [width,height] of [[1280,900],[360,640]]) test(`specific control legends fit ${width}x${height}`,async({page},info)=>{
  await page.setViewportSize({width,height});
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await page.getByRole('button',{name:'Справка по управлению',exact:true}).click();
  const dialog=page.getByRole('dialog',{name:'Управление в игре'});
  await expect(dialog.getByRole('img',{name:'Клавиши W сверху, D справа, S снизу, A слева'})).toBeVisible();
  const keyboard=dialog.locator('.help-device-label');
  await expect(keyboard).toHaveText(['W','D','S','A','↑','→','↓','←','Space','Enter','Shift','Esc','ЛКМ']);
  for (const image of await dialog.locator('svg').all()) {
    const size=await image.boundingBox();expect(size!.width).toBeGreaterThan(40);
  }
  await page.screenshot({path:info.outputPath(`keyboard-${width}.png`)});
  await dialog.getByText('ЛКМ / касание',{exact:true}).scrollIntoViewIfNeeded();
  await page.screenshot({path:info.outputPath(`keyboard-actions-${width}.png`)});
  await dialog.getByRole('button',{name:'Геймпад',exact:true}).click();
  const family=dialog.getByLabel('Обозначения контроллера');
  for(const [value,glyphs] of [['xbox',['Y','B','A','X']],['playstation',['△','○','×','□']],['nintendo',['X','A','B','Y']]] as const){
    await family.selectOption(value);
    await expect(dialog.locator('.help-device-label').first()).toHaveText(glyphs[0]);
    await expect(dialog.locator('.help-device-label').last()).toHaveText(value==='playstation'?'Options':value==='nintendo'?'+':'Start');
    await expect(dialog.locator('.help-answer-map kbd')).toHaveText([...glyphs]);
    if(value==='xbox') await page.screenshot({path:info.outputPath(`pad-${width}.png`)});
  }
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth && document.documentElement.scrollHeight<=innerHeight+1)).toBe(true);
  await expect(dialog.getByRole('button',{name:'Назад',exact:true})).toBeInViewport();
  await dialog.getByText('Start / Options / +',{exact:true}).scrollIntoViewIfNeeded();
  await expect(dialog.getByText('Start / Options / +',{exact:true})).toBeInViewport();
  await page.screenshot({path:info.outputPath(`pad-actions-${width}.png`)});
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
