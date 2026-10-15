import { test, expect } from '@playwright/test';

test('template sound/reset/storage and nested help preserve context',async({page},testInfo)=>{
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await page.getByLabel('Общая громкость',{exact:true}).fill('0');
  await page.getByLabel('Громкость музыки').fill('0.4');
  await page.reload();
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await expect(page.getByLabel('Общая громкость',{exact:true})).toHaveValue('0');
  await expect(page.getByLabel('Громкость музыки')).toHaveValue('0.4');
  await page.getByRole('button',{name:'Справка по управлению',exact:true}).click();
  await expect(page.getByRole('dialog',{name:'Управление в игре'})).toBeVisible();
  await page.getByRole('button',{name:'Геймпад',exact:true}).click();
  await page.screenshot({path:testInfo.outputPath('controls-help.png')});
  await page.keyboard.press('Escape');
  await expect(page.getByRole('button',{name:'Справка по управлению',exact:true})).toBeFocused();
  const consent = await page.getByLabel('Отправлять анонимную статистику').isChecked();
  await page.getByRole('button',{name:'Сбросить все настройки',exact:true}).click();
  await page.getByRole('button',{name:'Сбросить',exact:true}).click();
  await expect(page.getByLabel('Общая громкость',{exact:true})).toHaveValue('1');
  await expect(page.getByLabel('Громкость музыки')).toHaveValue('0.7');
  await expect(page.getByLabel('Отправлять анонимную статистику')).toBeChecked({checked:consent});
  await page.screenshot({path:testInfo.outputPath('settings.png')});
});

test('arrows visit sliders and change values without Tab; back restores invoking action',async({page})=>{
  await page.goto('/?muted=1');
  await expect(page.getByRole('button',{name:'Одиночная игра',exact:true})).toBeFocused();
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await page.keyboard.press('ArrowDown');
  await expect(page.getByLabel('Общая громкость',{exact:true})).toBeFocused();
  await page.keyboard.press('ArrowLeft');
  await expect(page.getByLabel('Общая громкость',{exact:true})).toHaveValue('0.9');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('button',{name:'Настройки',exact:true})).toBeFocused();
});

test('settings keep the screen stationary on a phone and scroll only the options',async({page},testInfo)=>{
  await page.setViewportSize({width:390,height:844});
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  await page.getByRole('button',{name:'Справка по управлению',exact:true}).scrollIntoViewIfNeeded();
  await expect(page.getByRole('button',{name:'Назад',exact:true})).toBeVisible();
  await expect(page.getByRole('button',{name:'Сбросить все настройки',exact:true})).toBeVisible();
  const bodyOverflow=await page.evaluate(()=>document.documentElement.scrollHeight>innerHeight+1);
  expect(bodyOverflow).toBe(false);
  await page.screenshot({path:testInfo.outputPath('settings-phone.png')});
});

test('pad can reach sliders, change master and open its graphical help',async({page})=>{
  await page.addInitScript(()=>{
    const pad={id:'Xbox standard',index:0,mapping:'standard',connected:true,buttons:Array.from({length:17},()=>({pressed:false,value:0,touched:false})),axes:[0,0,0,0],timestamp:0};
    (window as any).__menuPad=pad;Object.defineProperty(navigator,'getGamepads',{value:()=>[pad]});
  });
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Настройки',exact:true}).click();
  const press=async(index:number)=>{
    await page.evaluate(index=>{(window as any).__menuPad.buttons[index].pressed=true;},index);
    await page.waitForTimeout(40);
    await page.evaluate(index=>{(window as any).__menuPad.buttons[index].pressed=false;},index);
    await page.waitForTimeout(40);
  };
  await press(13);await expect(page.getByLabel('Общая громкость',{exact:true})).toBeFocused();
  await press(14);await expect(page.getByLabel('Общая громкость',{exact:true})).toHaveValue('0.9');
  await expect(page.locator('html')).toHaveAttribute('data-menu-device','pad');
  await press(1);await expect(page.getByRole('button',{name:'Настройки',exact:true})).toBeFocused();
});

test('desktop update UI distinguishes available, download/cancel and prepared restart',async({page})=>{
 await page.addInitScript(()=>{
  const listeners:((status:any)=>void)[]=[];const available:((ready:boolean,version?:string)=>void)[]=[];
  (window as any).mindbattleDesktop={version:1,status:async()=>({ready:false,shellVersion:'1.0.5',updateStatus:{phase:'available',version:'1.0.6'}}),
   onUpdateStatus:(fn:any)=>{listeners.push(fn);return()=>{};},onUpdate:(fn:any)=>{available.push(fn);return()=>{};},ready:async()=>{},safeToUpdate:async()=>{},quit:async()=>{},
   display:async()=>({width:1280,height:720,fullscreen:false}),
   downloadUpdate:async()=>{listeners.forEach(fn=>fn({phase:'downloading',version:'1.0.6',completed:1,total:4}));return true;},
   cancelDownload:async()=>{listeners.forEach(fn=>fn({phase:'available',version:'1.0.6'}));},applyUpdate:async()=>true,
   releaseHistory:async()=>[{tag:'v1.0.6',version:'1.0.6',date:'2026-10-15T00:00:00Z',notes:'Улучшено меню.'},{tag:'v1.0.5',version:'1.0.5',date:'2026-10-10T00:00:00Z',notes:'Установленная версия.'}]
  };
  (window as any).__prepare=()=>{listeners.forEach(fn=>fn({phase:'ready',version:'1.0.6'}));available.forEach(fn=>fn(true,'1.0.6'));};
 });
 await page.goto('/?muted=1');
 await expect(page.getByRole('button',{name:'Обновить',exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Обновить',exact:true}).click();
 await expect(page.getByText('Скачиваем обновление · 25%',{exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Отменить скачивание',exact:true}).click();
 await expect(page.getByRole('button',{name:'Обновить',exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Что нового',exact:true}).click();
 await expect(page.getByText('Улучшено меню.',{exact:true})).toBeVisible();
 await page.getByRole('combobox').selectOption('v1.0.5');
 await expect(page.getByText('Установленная версия.',{exact:true})).toBeVisible();
 await page.keyboard.press('Escape');
 await page.evaluate(()=>{(window as any).__prepare();});
 await expect(page.getByRole('button',{name:'Перезапустить',exact:true})).toBeVisible();
 await expect(page.getByText('Применится при следующем запуске игры.',{exact:true})).toBeVisible();
});

for(const [width,height] of [[800,600],[360,640],[1920,1080]]) test(`template settings fit ${width}x${height}`,async({page},testInfo)=>{
 await page.setViewportSize({width,height});await page.goto('/?muted=1');await page.getByRole('button',{name:'Настройки',exact:true}).click();
 await expect(page.getByRole('button',{name:'Назад',exact:true})).toBeVisible();await expect(page.getByRole('button',{name:'Сбросить все настройки',exact:true})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollHeight <= innerHeight+1 && document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.screenshot({path:testInfo.outputPath(`settings-${width}x${height}.png`)});
});

test('pad types a network room title without a physical keyboard',async({page})=>{
 await page.addInitScript(()=>{
  const pad={id:'Xbox standard',index:0,mapping:'standard',connected:true,buttons:Array.from({length:17},()=>({pressed:false,value:0,touched:false})),axes:[0,0,0,0],timestamp:0};
  (window as any).__menuPad=pad;Object.defineProperty(navigator,'getGamepads',{value:()=>[pad]});
 });
 await page.goto('/network?muted=1');await page.getByLabel('Название игры',{exact:true}).click();
 const press=async(index:number)=>{await page.evaluate(index=>{(window as any).__menuPad.buttons[index].pressed=true;},index);await page.waitForTimeout(40);await page.evaluate(index=>{(window as any).__menuPad.buttons[index].pressed=false;},index);await page.waitForTimeout(40);};
 await press(0);await expect(page.getByRole('dialog',{name:'Ввод текста'})).toBeVisible();
 for(let i=0;i<4;i++)await press(13);
 await expect(page.getByRole('button',{name:'й',exact:true})).toBeFocused();await press(0);
 for(let i=0;i<6;i++)await press(12);
 await expect(page.getByRole('button',{name:'Готово',exact:true})).toBeFocused();await press(0);
 await expect(page.getByRole('dialog',{name:'Ввод текста'})).toBeHidden();await expect(page.getByLabel('Название игры',{exact:true})).toHaveValue('й');
 await press(1);await expect(page).toHaveURL(/\/\?muted=1$/);
});
