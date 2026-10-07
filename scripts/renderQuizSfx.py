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

def utility(recipe, sources):
    """Edit recorded arena textures; do not generate oscillator/noise placeholders.

    Recipes retain source regions, timing, speed, filtering and layer gains.
    Both channels share the time mapping, preserving the recorded stereo image.
    Short envelopes keep repeated ticks clean and remove crop-edge clicks.
    """
    output = np.zeros((round(recipe['duration_ms'] * SR / 1000), 2))
    for layer in recipe['layers']:
        start = round(layer['start_ms'] * SR / 1000)
        length = round(layer['length_ms'] * SR / 1000)
        grain = sources[layer['source']][start:start + length].copy()
        if len(grain) != length:
            raise ValueError('Source region out of bounds: ' + recipe['cue'])
        if layer.get('reverse'):
            grain = grain[::-1]
        width = layer.get('lowpass_frames', 1)
        if width > 1:
            grain = np.column_stack([np.convolve(grain[:, ch], np.ones(width)/width, mode='same') for ch in range(2)])
        frames = round(layer['duration_ms'] * SR / 1000)
        positions = np.linspace(0, len(grain) - 1, frames)
        grain = np.column_stack([np.interp(positions, np.arange(len(grain)), grain[:, ch]) for ch in range(2)])
        attack = min(round(.004 * SR), frames // 4)
        release = min(round(.065 * SR), frames // 3)
        grain[:attack] *= np.linspace(0, 1, attack)[:, None]
        grain[-release:] *= np.linspace(1, 0, release)[:, None]
        offset = round(layer['offset_ms'] * SR / 1000)
        if offset + frames > len(output):
            raise ValueError('Layer exceeds cue duration: ' + recipe['cue'])
        output[offset:offset + frames] += grain * layer['gain']
    return finish(output, recipe['rms_dbfs'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--runtime', type=Path)
    args = parser.parse_args()
    metadata = json.loads((SOURCES/'sources.json').read_text())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tracks = {}
    recorded_sources = {}
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
        recorded_sources[item['id']] = data
        tracks[item['id']] = finish(data)
    for recipe in metadata['utility_recipes']:
        tracks[recipe['cue']] = utility(recipe, recorded_sources)
    tracks['reveal-all'] = tracks.pop('correct')
    tracks['reveal-none'] = tracks.pop('wrong')
    tracks['reveal-some'] = tracks.pop('mixed')
    # Legacy generic reveal remains a neutral cue; current UI uses outcome cues.
    tracks['reveal'] = tracks['reveal-some']
    manifest = {'version':'quiz-sfx-v1','sample_rate':SR,'channels':2,'source_manifest':'assets/audio/quiz-sfx-v1/sources.json','renderer':'scripts/renderQuizSfx.py','utility_renderer':metadata['utility_renderer'],'tracks':[]}
    for name, data in tracks.items():
        path = OUTPUT/(name+'.wav')
        sf.write(path, data, SR, subtype='PCM_16')
        manifest['tracks'].append({'cue':name,'asset':path.name,'duration_ms':round(len(data)/SR*1000),'sha256':sha(path),'peak_dbfs':round(20*np.log10(max(np.abs(data).max(),1e-9)),3),'rms_dbfs':round(20*np.log10(max(np.sqrt(np.mean(data**2)),1e-9)),3)})
    (SOURCES/'sources.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    (OUTPUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Rendered',len(tracks),'quiz SFX; sources and hashes preserved.')

if __name__ == '__main__':
    main()
