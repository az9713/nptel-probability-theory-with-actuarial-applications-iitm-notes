"""Private source acquisition; run from the repository root. No source media is published."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time
import requests

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'work' / 'sources'


def acquire(entry):
    video_id = entry['id']
    if not entry.get('title'):
        return {'id': video_id, 'status': 'unavailable in playlist enumeration'}
    if (SOURCE / f'{video_id}.m4a').exists():
        return {'id': video_id, 'status': 'audio present'}
    info_path = SOURCE / f'{video_id}.info.json'
    try:
        if not info_path.exists():
            command = ['yt-dlp', '--cache-dir', str(ROOT / 'work' / 'cache'),
                       '--no-progress', '--no-playlist', '--skip-download',
                       '--write-info-json', '-o', str(SOURCE / '%(id)s.%(ext)s'),
                       f'https://www.youtube.com/watch?v={video_id}']
            with (SOURCE / f'{video_id}.download.log').open('w', encoding='utf-8') as log:
                subprocess.run(command, stdout=log, stderr=log, cwd=ROOT, check=True)
        info = json.loads(info_path.read_text(encoding='utf-8'))
        formats = [f for fid in ['139', '140'] for f in info['formats'] if f['format_id'] == fid]
        last_error = None
        for fmt in formats:
            size = fmt['filesize']
            partial = SOURCE / f'{video_id}.range-{fmt["format_id"]}.part'
            try:
                offset = partial.stat().st_size if partial.exists() else 0
                with partial.open('ab') as output:
                    start = offset
                    while start < size:
                        chunk = 524288
                        for attempt in range(4):
                            end = min(start + chunk, size) - 1
                            try:
                                response = requests.get(fmt['url'] + f'&range={start}-{end}', timeout=20)
                                response.raise_for_status()
                                if len(response.content) != end - start + 1:
                                    raise ValueError(f'Range size mismatch at {start}')
                                output.write(response.content)
                                start = end + 1
                                break
                            except Exception:
                                chunk //= 2
                                if attempt == 3:
                                    raise
                                time.sleep(0.5)
                partial.replace(SOURCE / f'{video_id}.m4a')
                return {'id': video_id, 'status': 'downloaded', 'bytes': size,
                        'format': fmt['format_id']}
            except Exception as exc:
                last_error = exc
        raise last_error
    except Exception as exc:
        return {'id': video_id, 'status': 'failed', 'error': str(exc)[:200]}


if __name__ == '__main__':
    playlist = json.loads((SOURCE / 'playlist.json').read_text(encoding='utf-8-sig'))
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(acquire, playlist['entries']):
            results.append(result)
            print(json.dumps(result), flush=True)
            (SOURCE / 'acquisition-status.json').write_text(json.dumps(results, indent=2))
