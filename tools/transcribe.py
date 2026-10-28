"""Transcribe privately using workspace-contained model files and output paths."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'work' / 'sources'
MODEL = ROOT / 'work' / 'cache' / 'whisper-base.en'


def main():
    # NVIDIA runtime wheels are read-only installed dependencies. All outputs stay local.
    import site
    handles = []
    for base in site.getsitepackages():
        for folder in (Path(base) / 'nvidia').glob('*/bin'):
            if folder.is_dir():
                handles.append(os.add_dll_directory(str(folder)))
    from faster_whisper import WhisperModel, BatchedInferencePipeline
    model = WhisperModel(str(MODEL) if MODEL.exists() else 'base.en',
                         device='cuda', compute_type='int8_float16',
                         download_root=str(ROOT / 'work' / 'cache'))
    pipeline = BatchedInferencePipeline(model=model)
    playlist = json.loads((SOURCE / 'playlist.json').read_text(encoding='utf-8-sig'))
    priority = {'9CLUXGcp1aE', 'UFj7535SNqM', '1-z2lfInbp0'}
    ordered = sorted(playlist['entries'], key=lambda x: (
        0 if x['id'] in priority else 1,
        int((x.get('title') or 'W99_L99').split('_')[0][1:])
        if (x.get('title') or '').startswith('W') else 99,
        x.get('title') or ''))
    failures = []
    for entry in ordered:
        video_id = entry['id']
        out = SOURCE / f'{video_id}.transcript.json'
        if out.exists():
            continue
        media = None
        if not entry.get('title'):
            continue
        for attempt in range(1):
            media = next((p for ext in ['m4a']
                          if (p := SOURCE / f'{video_id}.{ext}').exists()), None)
            if media is not None:
                break
        if media is None:
            continue
        started = time.monotonic()
        try:
            segments, info = pipeline.transcribe(str(media), batch_size=8,
                language='en', beam_size=3, vad_filter=True,
                initial_prompt='Probability theory, actuarial applications, random variable, '
                'expectation, variance, Poisson, binomial, moment generating function.')
            rows = [{'start': round(s.start, 2), 'end': round(s.end, 2),
                     'text': s.text.strip()} for s in segments]
            record = {'id': video_id, 'title': entry['title'],
                      'method': 'faster-whisper base.en, CUDA int8_float16, beam 3, batch 8',
                      'source_audio_sha256': hashlib.sha256(media.read_bytes()).hexdigest(),
                      'duration': info.duration, 'segments': rows}
            out.write_text(json.dumps(record, indent=2), encoding='utf-8')
            text = '\n'.join(f"[{int(s['start']) // 60:02d}:{int(s['start']) % 60:02d}] {s['text']}"
                             for s in rows)
            (SOURCE / f'{video_id}.transcript.txt').write_text(text, encoding='utf-8')
            print(f"DONE {video_id} {len(rows)} segments {time.monotonic()-started:.1f}s", flush=True)
        except Exception as exc:
            failures.append({'id': video_id, 'error': str(exc)})
            print(f'FAILED {video_id}: {exc}', flush=True)
    (SOURCE / 'transcription-failures.json').write_text(json.dumps(failures, indent=2))


if __name__ == '__main__':
    main()
