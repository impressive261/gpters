# Katharine · Fly Korean

## Start
Open `index.html` after extracting the complete folder. Keep audio, scripts and PDFs in their relative folders. The hosted HTTPS version is preferable on phones; microphone recording and offline installation need a secure browser.

Start with **Today**. Five new words/day and twenty cards/session are the defaults. Speak before revealing. Again means forgotten; Hard means recalled with effort. Recognition and production have independent histories. Good/Easy recognition unlocks production at the following local midnight. Reverse cards are separated across days, not unlocked only after long-term mastery.

Use **Speaking & print** for one daily page. At most eight prompts per file. Highlight unknown words and write meanings in the far-right column. Fold the column away for a second speaking pass. Optional extension grammar is excluded by default. The app selects one sheet locally; it does not email or message the student automatically.

## Contents
308 vocabulary entries (original 250 + 58 sentence-derived additions), 78 explicit dictionary/polite pairs, 26 sentence patterns, 33 grammar forms, 406 conversation prompts, all 150 original oral word-test prompts, 52 sentence-production prompts, a final speaking mission and the original also/only contrast drill. See `build_summary.json` for exact final PDF counts.

## Real pronunciation recordings
694 generated Korean neural MP3s: 308 headwords + 78 polite forms + 308 examples. Voice: Microsoft Edge online neural speech `ko-KR-SunHiNeural`, generated through `edge-tts` 7.2.3, rate -10%. `audio-manifest.json` records exact text and filenames. Device speech is a visibly labelled fallback only. No student API key is required.

Paid fal/ElevenLabs generation was not used: the connected account had no balance. No credits were purchased and no accounts were switched. The delivered voice is a high-quality neural voice, not a claim that it objectively ranks first among all services. Technical decoding checks do not equal human listening to every clip.

## Privacy and backup
Progress is local to this browser and origin, not synced to another device or the teacher. Clearing site data, changing browsers, private browsing and storage pressure may erase it. Export JSON backups regularly. Moving from a preview address to the final website requires export/import. Notes and microphone recordings are never uploaded; recordings are temporary and are not in backups. Only the first name and generic lesson content are in the public repository.

## Learning engine
The scheduler is SM-2-inspired, not FSRS. Secure means an interval of at least seven days, Good/Easy answers on two different dates, and not overdue. It is not guaranteed mastery or a calibrated memory probability. Typed answers only report exact matches; alternative correct translations are self-assessed. No unvalidated automatic pronunciation score, advertising, analytics or leaderboard.

## Research-informed design
Features were benchmarked against official documentation, not an independent universal ranking:
- Anki: review/new limits, sibling burying and scheduling controls: https://docs.ankiweb.net/deck-options
- Quizlet Learn: written answers, answer-language choice, starred terms and audio: https://help.quizlet.com/hc/en-us/articles/360030986971-Studying-with-Learn
- RemNote SM-2 explanation: learning/review stages and interval adjustments: https://help.remnote.com/en/articles/6026144-the-anki-sm-2-spaced-repetition-algorithm
- Speech tooling: https://github.com/rany2/edge-tts

## Rebuild and tests
Source is in the sibling `katharine-src` directory. Run `python katharine-src/run.py` from the repository root. This applies curated notes and correct source-chapter labels before the vocabulary audit. Python dependencies: reportlab, pymupdf, playwright. System font: fonts-nanum. Never distribute font files separately; PDFs embed normal subsets. The GitHub workflow runs source audit, audio/PDF validation and desktop/mobile browser regression tests.

## Native GitHub Pages
This app is isolated at `katharine/`; the existing repository root app is not replaced. The repository owner must enable **Settings → Pages → Source: GitHub Actions** if Pages is disabled, then run **Deploy static app to Pages**. The connector cannot grant itself administration permissions. A repository commit or a successful material build does not by itself prove that the public Pages website is live.
