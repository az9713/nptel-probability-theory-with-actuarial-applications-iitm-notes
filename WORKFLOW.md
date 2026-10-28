# Lecture-note production workflow

This independent textbook rewrite follows the NPTEL and Stanford lecture-note
reading editions in this GitHub account. The user authorized the complete
substantial edition, public repository, GitHub Pages publication and autonomous
completion. All local work, source downloads, models, caches and temporary
outputs were kept inside the project directory.

1. Enumerate the supplied playlist, preserving every video identity, upload
   title, duration and original position. Organize the exposition by explicit
   week/lesson labels because the upload order is irregular. Retain unavailable
   entries and duplicate lesson labels without inventing missing content.
2. Acquire all available audio and verify its duration against video metadata.
   Generate local faster-whisper base.en machine transcripts using CUDA, with
   model weights and outputs under the private working directory. Caption
   retrieval failed; publisher captions were not used. Preserve audio/transcript
   hashes and source boundaries in the public source record.
3. Read each assigned transcript sequentially. Write a coherent, independently
   authored textbook with local definitions, precise hypotheses, proofs,
   interpreted calculations, counterexamples, original worked exercises and
   standalone executable examples. A related timestamp does not attribute all
   added material to the lecturer. Resolve speech-recognition ambiguities through
   explicit derivation, normalization or a labelled reconstruction. Inspect
   targeted source frames when available and material to an ambiguity.
4. Keep the same conventions throughout the insurance model: nonnegative gross
   loss X, ordinary deductible d, pre-coinsurance layer width u, insurer fraction
   c, payment Y=c min((X-d)+,u), and aggregate payment S. Distinguish a ground-up
   ceiling L from layer width L-d, and per-loss from per-payment moments.
5. Use original standard-library Python examples. Execute every saved program;
   check exact equality with the embedded source and agreement with its real
   displayed stdout. Assertions check finite teaching constructions. These
   checks do not certify general theorems or empirical model adequacy.
6. Obtain two recorded independent AI mathematical/pedagogical review rounds for
   each chapter group. Preserve the original reports, repair located findings,
   and record the current accepted body hashes. The public editorial record
   reports review scope and limitations. It does not claim human expert review,
   formal verification, or comprehensive independent source-fidelity review.
7. Wrap the directly authored HTML bodies verbatim in the common offline reader.
   Save body hashes and section timestamp locators in chapter sidecars. Bundle
   styles, controls, full-text search and MathJax. Validate actual rendered math,
   local links, source bounds, desktop/mobile layouts, solution/code controls,
   printing and interactive mathematical models.
8. Rebuild and validate a clean public export that contains no private sources.
   Commit the reviewed edition and push to the public repository. Serve the main
   branch root through GitHub Pages, then separately check served-file integrity.
   Exclude the publication report itself from its hash set to avoid self-hashing.

The supplied playlist has 58 listed entries: an introduction, 56 available
lecture uploads and one unavailable entry. There are 55 distinct week/lesson
labels because Week 11 Lesson 1 has two uploads. No Week 8 recordings appear.
The 22 topic chapters account for every available lecture upload. An original
concentration appendix supplies a bridge for missing Week 8 topics without
claiming to reconstruct unavailable recordings. The final chapter independently
restates all thirty mock-problem mechanisms and expands their solutions.

The public repository includes canonical chapter bodies, generated root HTML,
sidecars, local rendering assets, programs, build/check tools and curated
verification records. Raw audio, machine transcripts, downloaded reference
snapshots, author notes and full private editorial reports remain unpublished.
The builder and public code checks work without those private files or a network.
The public source manifest supplies the evidence needed for source bounds.

Run the reproducible checks from the repository root:

```sh
python tools/build_book.py
python tools/check_code.py
python tools/validate_book.py
python tools/browser_check.py
python tools/check_package.py
```

Rebuilding and static/code checks require Python 3. Browser checks additionally
require Python Playwright and Chrome or Edge; their profile and temporary files
are placed under the project working directory. Acquisition and transcription
scripts are optional source-production tools, rather than reader dependencies.
The public evidence records distinguish checks run on the shipped edition from
historical reports, source acquisition from source reading, and source reading
from audiovisual inspection.
