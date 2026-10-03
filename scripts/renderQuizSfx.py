"""Render the selected quiz SFX. Run with the installed audio Python runtime.
--generate --runtime PATH generates missing Stable Audio sources; otherwise render
only checked-in sources. No weights or model downloads are part of this script.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'assets/audio/quiz-sfx-v1'
OUTPUT = ROOT / 'public/audio/quiz-sfx-v1'
SR = 44100

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def finish(data, target=-23):
    data = data.copy() - data.mean(axis=0)
    n = min(round(.008*SR), len(data))
    data[:n] *= np.linspace(0, 1, n)[:, None]
    n = min(round(.16*SR), len(data)//3)
    data[-n:] *= np.linspace(1, 0, n)[:, None]
    rms = np.sqrt(np.mean(data**2))
    data *= min(10**(target/20)/max(rms, 1e-9), .74/max(np.abs(data).max(), 1e-9))
    return data

def pulse(seconds, frequency, decay, seed):
    t = np.arange(round(seconds*SR))/SR
    rng = np.random.default_rng(seed)
    # Rounded low body with a soft textured attack, deliberately not a melody.
    body = np.sin(2*np.pi*frequency*t) + .18*np.sin(2*np.pi*frequency*2.01*t)
    noise = rng.normal(0, 1, len(t))
    noise = np.convolve(noise, np.ones(24)/24, mode='same')
    mono = body*np.exp(-decay*t) + .14*noise*np.exp(-60*t)
    stereo = np.column_stack([mono, mono])
    for delay, gain in [(.031,.13), (.067,.07)]:
        n = round(delay*SR)
        stereo[n:,1] += mono[:-n]*gain
    return stereo

def utility(name):
    parameters = {
        'answer-locked': (.12, 430, 46, 63201, -29),
        'countdown': (.18, 320, 30, 63202, -27),
        'timer-last-second': (.20, 250, 35, 63203, -27),
        'screen-transition': (.30, 210, 15, 63204, -29),
        'question-start': (.60, 160, 9, 63205, -25),
        'reserve-start': (.80, 110, 6, 63206, -25),
    }
    seconds, freq, decay, seed, target = parameters[name]
    data = pulse(seconds, freq, decay, seed)
    if name == 'reserve-start':
        n = round(.23*SR)
        data[n:] += .45*pulse(seconds-.23, freq*1.5, decay, seed+20)
    return finish(data, target)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--runtime', type=Path)
    args = parser.parse_args()
    metadata = json.loads((SOURCES/'sources.json').read_text())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tracks = {}
    for item in metadata['tracks']:
        source = SOURCES/(item['id']+'.wav')
        if not source.exists():
            if not args.generate or not args.runtime:
                raise RuntimeError('Missing source: '+str(source))
            command = [str(args.runtime/'.venv/bin/python'), 'scripts/sa3_mlx.py', '--dit', 'sm-music', '--decoder', 'same-s', '--seconds', str(item['seconds']), '--steps', '8', '--cfg', '1', '--seed', str(item['seed']), '--prompt', item['prompt'], '--out', str(source)]
            subprocess.run(command, cwd=args.runtime, check=True, stdout=subprocess.DEVNULL)
        if item.get('source_sha256') and sha(source) != item['source_sha256']:
            raise RuntimeError('Source hash differs: '+str(source))
        item['source_sha256'] = sha(source)
        data, rate = sf.read(source, always_2d=True)
        assert rate == SR and data.shape[1] == 2
        tracks[item['id']] = finish(data)
    for name in ['answer-locked','countdown','timer-last-second','screen-transition','question-start','reserve-start']:
        tracks[name] = utility(name)
    tracks['reveal-all'] = tracks.pop('correct')
    tracks['reveal-none'] = tracks.pop('wrong')
    tracks['reveal-some'] = tracks.pop('mixed')
    # Legacy generic reveal remains a neutral cue; current UI uses outcome cues.
    tracks['reveal'] = tracks['reveal-some']
    manifest = {'version':'quiz-sfx-v1','sample_rate':SR,'channels':2,'source_manifest':'assets/audio/quiz-sfx-v1/sources.json','renderer':'scripts/renderQuizSfx.py','tracks':[]}
    for name, data in tracks.items():
        path = OUTPUT/(name+'.wav')
        sf.write(path, data, SR, subtype='PCM_16')
        manifest['tracks'].append({'cue':name,'asset':path.name,'duration_ms':round(len(data)/SR*1000),'sha256':sha(path),'peak_dbfs':round(20*np.log10(max(np.abs(data).max(),1e-9)),3),'rms_dbfs':round(20*np.log10(max(np.sqrt(np.mean(data**2)),1e-9)),3)})
    (SOURCES/'sources.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    (OUTPUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Rendered',len(tracks),'quiz SFX; sources and hashes preserved.')

if __name__ == '__main__':
    main()
