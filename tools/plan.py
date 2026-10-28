"""Materialize the chapter plan from preserved video labels, never from playlist position."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SPECS = [
    ('Events, probability, and counting', 'events-and-counting', 1, [1, 2]),
    ('Conditioning, Bayes, and independence', 'conditioning-and-bayes', 1, [3, 4, 5]),
    ('Random variables and distributions', 'random-variables', 2, [1, 2, 3]),
    ('Expectation and functions of a loss', 'expectation', 2, [4, 5]),
    ('Counting claims: Bernoulli, binomial, and Poisson', 'claim-counts', 3, [1, 2]),
    ('Waiting times, gamma losses, and the normal model', 'severity-families', 3, [3, 4, 5]),
    ('Joint and conditional distributions', 'joint-distributions', 4, [1, 2, 3]),
    ('Covariance, correlation, and portfolio variance', 'dependence', 4, [4, 5]),
    ('One-dimensional transformations', 'transformations', 5, [1, 2]),
    ('Jacobians and convolution', 'jacobians-and-convolution', 5, [3, 4]),
    ('Order statistics and extreme losses', 'order-statistics', 5, [5]),
    ('Conditional expectation and total variance', 'total-moments', 6, [1, 2, 3]),
    ('Mixtures and compound models', 'mixtures-and-compounding', 6, [4, 5]),
    ('Moment and cumulant generating functions', 'generating-functions', 7, [1, 2, 3, 4, 5]),
    ('The central limit theorem and continuity correction', 'central-limit-theorem', 9, [1, 2, 3]),
    ('Aggregate approximations and model selection', 'aggregate-approximations', 9, [4, 5]),
    ('Losses, payments, and deductibles', 'deductibles', 10, [1, 2]),
    ('Policy limits, layers, and stop-loss', 'policy-layers', 10, [3, 4, 5]),
    ('Random sums and aggregate-loss moments', 'aggregate-moments', 11, [1, 2]),
    ('Severity moments and aggregate-loss design', 'aggregate-design', 11, [3, 4, 5]),
    ('An integrated probability toolkit', 'integrated-toolkit', 12, [1, 2]),
    ('Mock examination: mechanisms and worked solutions', 'mock-examination', 12, [3, 4, 5]),
]


def main():
    playlist = json.loads((ROOT / 'work/sources/playlist.json').read_text(encoding='utf-8-sig'))
    videos = []
    for position, entry in enumerate(playlist['entries'], 1):
        title = entry.get('title') or '[Unavailable playlist entry]'
        match = re.match(r'W(\d+)_L(\d+)', title)
        videos.append({'id': entry['id'], 'playlist_position': position,
                       'title': title, 'duration': entry.get('duration'),
                       'week': int(match[1]) if match else None,
                       'lesson': int(match[2]) if match else None,
                       'url': f"https://www.youtube.com/watch?v={entry['id']}",
                       'status': 'available' if entry.get('title') else 'unavailable'})
    chapters = []
    for n, (title, slug, week, lessons) in enumerate(SPECS, 1):
        chapters.append({'number': n, 'title': title,
            'file': f'chapter-{n:02d}-{slug}.html',
            'body': f'chapters/ch{n:02d}.html', 'week': week,
            'videos': [v['id'] for v in sorted(videos, key=lambda v: v['lesson'] or 0)
                       if v['week'] == week and v['lesson'] in lessons]})
    (ROOT / 'book-plan.json').write_text(json.dumps({'title': playlist['title'],
        'playlist': playlist['webpage_url'], 'chapters': chapters}, indent=2), encoding='utf-8')
    for video in videos:
        video['chapters'] = [c['number'] for c in chapters if video['id'] in c['videos']]
    (ROOT / 'source-manifest.json').write_text(json.dumps({
        'playlist': playlist['webpage_url'], 'enumerated_at': '2026-10-28',
        'recordings': videos, 'gaps': ['No W8 lesson labels occur in the supplied playlist.',
        'One unavailable entry is preserved without inferring its content.',
        'W11_L1 occurs twice; both recording identities are retained.'],
        'source_boundary': 'Machine transcripts and sampled frames; no full audiovisual review.'
        }, indent=2), encoding='utf-8')
    print(f'{len(videos)} entries, {len(chapters)} chapters, '
          f'{sum(bool(v["chapters"]) for v in videos)} assigned recordings')


if __name__ == '__main__':
    main()
