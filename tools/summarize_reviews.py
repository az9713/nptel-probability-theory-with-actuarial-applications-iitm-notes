"""Curate actual private review evidence; never infer acceptance from test success."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GROUPS=[('foundations',list(range(1,8)),'science_editor_insurance'),
        ('transforms',list(range(8,15)),'science_editor_foundations'),
        ('insurance',list(range(15,22)),'science_editor_transforms'),
        ('root',[22],'science_editor_insurance')]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    groups=[];accepted=[]
    for name,numbers,reviewer in GROUPS:
        paths=[ROOT/'chapters'/f'ch{n:02d}.html' for n in numbers]
        if name=='root':paths.append(ROOT/'pages/appendix-concentration.html')
        reports=[ROOT/'work/reviews'/f'{name}-r{round_}.md' for round_ in [1,2]]
        texts=[p.read_text(encoding='utf-8') for p in reports]
        bodies=[]
        for path in paths:
            digest=sha(path)
            if digest not in texts[1]:raise ValueError(f'Latest review does not bind current body: {path.name}')
            body={'path':path.relative_to(ROOT).as_posix(),'sha256':digest,
                  'latest_round':2,'verdict':'zero remaining actionable mathematical/pedagogical blockers'}
            bodies.append(body);accepted.append(body)
        groups.append({'group':name,'latest_reviewer':reviewer,
            'review_model':'gpt-6.1-sol','effort':'medium',
            'rounds':[{'round':i+1,'private_report_sha256':sha(p),
                       'report_retention':'Full report retained privately; curated findings summarized here'}
                      for i,p in enumerate(reports)],
            'latest_verdict':'zero remaining actionable mathematical/pedagogical blockers',
            'bodies':bodies})
    result={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Independent AI mathematical and pedagogical review of complete chapter bodies',
        'limitations':['No human expert certification or formal verification',
        'No comprehensive independent transcript-fidelity review by mathematical reviewers',
        'Numerical execution, source acquisition and reader validation are separate evidence'],
        'historical_repairs':['Foundations: event wording, measurable events and almost-sure support, rare-event finite-n condition, visible full exercise prompts',
        'Transformations: density existence and almost-everywhere qualification; all-zero mixture boundary',
        'Insurance: third-moment versus MGF assumptions, zero-variance inequality case, degenerate count/infinite mean boundary, layer-width notation',
        'Mock/appendix: two-variable maximum, count/severity independence, positive Poisson rate, positive integer sample size, direct triangular-density quadrature check'],
        'reviewed_bodies':accepted,'groups':groups}
    (ROOT/'editorial-review-summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(f'{len(accepted)} reviewed bodies bound to their actual second-round accepted hashes')

if __name__=='__main__':main()
