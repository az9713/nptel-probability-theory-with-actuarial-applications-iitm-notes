"""Render the public README from final inventory counts and source identities."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='https://az9713.github.io/nptel-probability-theory-with-actuarial-applications-iitm-notes/'


def main():
    completion=json.loads((ROOT/'completion.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'source-manifest.json').read_text(encoding='utf-8'))
    hours=sum(v['duration'] or 0 for v in manifest['recordings'] if v['chapters'])/3600
    table='\n'.join(f'| {c["number"]} | [{c["title"]}]({BASE+c["file"]}) | {c["week"]} |' for c in completion['chapters'])
    text=f'''# Probability Theory with Actuarial Applications — a textbook rewrite

**[Read the live textbook]({BASE})**

[![Preview of the probability textbook](assets/site-preview.png)]({BASE})

An independent, substantial rewrite and expansion of Prof. Neelesh S. Upadhye's
IIT Madras NPTEL course, [Probability Theory with Actuarial Applications](https://nptel.ac.in/courses/111106929).
The [supplied YouTube playlist](https://www.youtube.com/playlist?list=PLyqSpQzTE6M-6uZtCcdhLS-HiXzQ43Bw2)
sets the coverage; the notes develop their own explanations, definitions,
derivations, interpreted calculations, original examples and worked exercises.

**Complete for every available lecture upload in the supplied playlist:**
{completion['chapter_count']} topic chapters covering 56 uploads ({hours:.1f} hours), approximately
{completion['words']:,} words of chapter text including formulas and exercises but excluding
code/output, {completion['worked_exercises']} chapter exercises with full solutions, and 23 executed
standalone Python programs. A separate original concentration appendix adds five
worked exercises. The final chapter expands all thirty mock-examination problems.

The supplied playlist has 58 listed entries: an introduction, 56 available lecture
uploads, and one unavailable entry. Its teaching labels are out of upload order;
Week 11 Lesson 1 has two distinct uploads, both retained and read. **No Week 8
recordings appear.** The original appendix supplies a proved concentration/LLN
bridge without claiming to reconstruct those missing lectures.

## Read the chapters

| Chapter | Reading edition | Source week |
|---|---|---|
{table}

Explore the [study guide]({BASE}study-guide.html),
[recording and source map]({BASE}source-map.html),
[interactive laboratory]({BASE}numerical-lab.html),
[concentration appendix]({BASE}appendix-concentration.html), and
[primary references]({BASE}references.html).

## What the edition adds

- Explicit assumptions, local notation, full derivations and interpreted checks.
- A consistent loss-to-payment-to-aggregate modeling sequence, distinguishing
  per-loss and per-payment moments, mixed and compound models, and a ground-up
  ceiling from a payment cap.
- Original standalone programs with meaningful assertions, exact source parity,
  and their actual output beside the explanation.
- Worked exercises that test derivation, support, dependence, limiting cases and
  model selection, with complete expandable solutions.
- Three interactive mathematical models: insurance layers and compound-Poisson
  moments, Bayesian updating with a rare class, and correlated diversification.
- An offline reader with local MathJax, full-text search, dark/light themes, text
  controls, code copying, previous/next links, mobile layouts and printable solutions.

A timestamp locates related lecture material; it does not imply that the lecturer
supplied every added derivation, example, correction, program or exercise.
Research and course sources remain attributed to their original authors.

## Evidence and its limits

All 57 available recordings, including the introduction, have locally generated
faster-whisper base.en machine transcripts. Assigned transcripts were read
sequentially by the chapter authors. Publisher-caption retrieval failed, so those
captions were not used. All acquired audio durations match video metadata, and
all transcript audio hashes match the retained media. Two targeted source frames
confirmed ambiguous mock-problem weights and density notation. **Comprehensive
slide/audiovisual review is not claimed.**

Every chapter and the appendix has two recorded independent AI mathematical and
pedagogical review rounds. Latest accepted body hashes bind the final reviewed
files; all recorded actionable findings were repaired. This is not human expert
certification, comprehensive independent source-fidelity review, or formal verification.

The [workflow](WORKFLOW.md), [source evidence](source-validation-summary.json),
[editorial record](editorial-review-summary.json), [content inventory](completion.json),
[code checks](validation/code-checks.json), [static checks](validation/book-checks.json),
[offline reader checks](validation/reader-checks.json),
[clean-export checks](validation/source-free-checks.json), and
[package checks](validation/package-checks.json) record the actual scope and results.
Numerical checks establish finite examples under stated assumptions, rather than
empirical realism or general mathematical proofs. Publication integrity is
recorded separately after GitHub Pages deployment.

## Use offline or rebuild

Download the repository ZIP, extract it, and open the root index.html. The reader,
mathematics, navigation, search and controls work offline. Linked recordings and
external references require an internet connection.

From the repository root:

    python tools/build_book.py
    python tools/check_code.py
    python tools/validate_book.py
    python tools/browser_check.py
    python tools/check_package.py

Rebuilding and static/code checks use Python's standard library. Browser checks
also require Python Playwright and Chrome or Edge. Programs are standalone: run,
for example, python code/ch17.py. No private source files are needed to rebuild
or run the public examples. Source acquisition/transcription tools are optional
production tools, with additional dependencies listed separately.

Raw audio, transcripts, downloaded reference snapshots, author briefs and full
private review reports remain unpublished. The public package contains the
rewritten textbook, canonical chapter bodies, generated reading pages, sidecars,
local assets, source locators, programs, tools and curated evidence. File byte
identities are preserved in Git. GitHub Pages serves the main branch root.
'''
    (ROOT/'README.md').write_text(text,encoding='utf-8')
    print(f'README: {completion["words"]:,} chapter words; {completion["worked_exercises"]} solved chapter exercises; {hours:.2f} lecture hours')

if __name__=='__main__':main()
