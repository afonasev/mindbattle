import { describe,it,expect } from 'vitest';
import { decodePreferences, DEFAULT_PREFERENCES } from '../../src/adapters/storage';
import { AudioController, type AudioSource } from '../../src/adapters/audio';

describe('template preference contracts',()=>{
  it('migrates legacy mute to zero master and preserves all channel values',()=>{
    expect(decodePreferences({...DEFAULT_PREFERENCES,masterVolume:undefined,muted:true,musicVolume:0,effectsVolume:.4})).toEqual({...DEFAULT_PREFERENCES,masterVolume:0,muted:false,musicVolume:0,effectsVolume:.4});
  });
  it('repairs fields independently and preserves explicit false/zero',()=>{
    expect(decodePreferences({masterVolume:0,musicVolume:NaN,effectsVolume:0,highContrast:false,textSize:'large'})).toEqual({...DEFAULT_PREFERENCES,masterVolume:0,musicVolume:.7,effectsVolume:0,textSize:'large'});
  });
  it('master multiplies active effects and music, and zero stops new playback',()=>{
    const sources:AudioSource[]=[];
    const audio=new AudioController({create:()=>{const source={volume:1,currentTime:0,loop:false,play:()=>{},pause:()=>{}};sources.push(source);return source;}},{...DEFAULT_PREFERENCES,masterVolume:.5},0,false);
    audio.play('answer-locked');expect(sources[0].volume).toBeCloseTo(.35);
    audio.update({...DEFAULT_PREFERENCES,masterVolume:.2});expect(sources[0].volume).toBeCloseTo(.14);
    audio.play('menu-theme');expect(sources[1].volume).toBeCloseTo(.2*.7*.25);
    audio.update({...DEFAULT_PREFERENCES,masterVolume:0});expect(sources[0].volume).toBe(0);expect(sources[1].volume).toBe(0);expect(audio.play('answer-locked')).toBe(false);audio.stopEvents();audio.stopMusic();
  });
});
