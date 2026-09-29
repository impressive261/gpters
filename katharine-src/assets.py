from pathlib import Path
import json
A=Path(__file__).resolve().parent.parent/'katharine'
(A/'icon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect width="192" height="192" rx="40" fill="#23594e"/><path d="M42 60h62v66H88V76H42zm85-13h16v40h18v16h-18v45h-16z" fill="#f0f4df"/></svg>')
(A/'manifest.webmanifest').write_text(json.dumps(dict(name='Katharine · Fly Korean',short_name='Fly Korean',start_url='./',scope='./',display='standalone',background_color='#f7f8f3',theme_color='#23594e',icons=[dict(src='icon.svg',sizes='any',type='image/svg+xml',purpose='any')]),ensure_ascii=False))
(A/'.nojekyll').touch()
(A/'sw.js').write_text('''/* Scope is katharine/ only. Never delete unrelated caches or learner storage. */
const SHELL='katharine-shell-v1',AUDIO='katharine-audio-v1',ROOT=new URL('./',self.location),CORE=['./','index.html','styles.css','scheduler.js','app.js','data.js','audio-manifest.js','audio-manifest.json','icon.svg','manifest.webmanifest'];
self.addEventListener('install',e=>e.waitUntil(caches.open(SHELL).then(c=>c.addAll(CORE))));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==ROOT.origin||!u.pathname.startsWith(ROOT.pathname))return;
if(u.pathname.includes('/audio/')||u.pathname.includes('/pdfs/')){e.respondWith(caches.open(AUDIO).then(async c=>{const old=await c.match(e.request);if(old)return old;const r=await fetch(e.request);if(r.ok)c.put(e.request,r.clone());return r;}));return;}
e.respondWith(fetch(e.request).then(r=>{if(r.ok){const copy=r.clone();caches.open(SHELL).then(c=>c.put(e.request,copy));}return r;}).catch(async()=>{const c=await caches.open(SHELL);return await c.match(e.request)||(e.request.mode==='navigate'?await c.match('index.html'):Response.error());}));});
''')
(A/'README.md').write_text('''# Katharine · Fly Korean

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
Source is in the sibling `katharine-src` directory. Run enrich.py, questions.py, patterns.py, build.py and assets.py in that order. Python dependencies: reportlab, pymupdf, playwright. System font: fonts-nanum. Never distribute font files separately; PDFs embed normal subsets. The GitHub workflow runs source audit, audio/PDF validation and desktop/mobile browser regression tests.

## Native GitHub Pages
This app is isolated at `katharine/`; the existing repository root app is not replaced. The repository owner must enable **Settings → Pages → Source: GitHub Actions** if Pages is disabled, then run **Deploy static app to Pages**. The connector cannot grant itself administration permissions. A repository commit or a successful material build does not by itself prove that the public Pages website is live.
''')
print('Offline assets and guide generated')
