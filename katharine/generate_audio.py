"""Generate real Korean neural MP3s. Never label browser fallback as generated audio.
Only standard public Edge TTS is used; no API credentials are embedded.
"""
from pathlib import Path
import asyncio, base64, gzip, hashlib, json, os, sys, time
import edge_tts
ROOT = Path(__file__).resolve().parent
VOICE = 'ko-KR-SunHiNeural'
RATE = '-10%'

def read_data():
    data = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))
    if 'words_gzip_base64' in data:
        data = json.loads(gzip.decompress(base64.b64decode(data['words_gzip_base64'])))
        (ROOT / 'data.json').write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    return data

async def main():
    data = read_data()
    out = ROOT / 'audio'
    out.mkdir(exist_ok=True)
    manifest_path = ROOT / 'audio-manifest.json'
    try:
        old = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError):
        old = {}
    manifest = {'provider': 'Microsoft Edge online neural TTS', 'voice': VOICE,
                'rate': RATE, 'generated': {}, 'failed': [], 'version': 1,
                'qualityNote': 'Neural voice; not a claim of independently measured best-in-class quality.'}
    texts = {}
    for word in data['words']:
        for kind, text in [('word', word['ko']), ('polite', word.get('yo', '')), ('example', word['example'])]:
            if text:
                texts[word['id'] + '-' + kind] = text
    sem = asyncio.Semaphore(3)
    stop = asyncio.Event()
    async def generate(key, text):
        digest = hashlib.sha256((VOICE + '|' + RATE + '|' + text).encode()).hexdigest()
        filename = key + '-' + digest[:10] + '.mp3'
        target = out / filename
        if target.exists() and target.stat().st_size > 1000:
            manifest['generated'][key] = {'url': 'audio/' + filename, 'text': text, 'sha256': digest, 'bytes': target.stat().st_size}
            return
        async with sem:
            if stop.is_set():
                manifest['failed'].append({'key': key, 'error': 'Stopped after service rejection'})
                return
            for attempt in range(3):
                tmp = target.with_suffix('.part')
                try:
                    await asyncio.wait_for(edge_tts.Communicate(text, VOICE, rate=RATE).save(str(tmp)), timeout=75)
                    if tmp.stat().st_size < 1000:
                        raise RuntimeError('Empty or unexpectedly short audio response')
                    tmp.replace(target)
                    manifest['generated'][key] = {'url': 'audio/' + filename, 'text': text, 'sha256': digest, 'bytes': target.stat().st_size}
                    print('GENERATED', key, target.stat().st_size, flush=True)
                    await asyncio.sleep(.3)
                    return
                except Exception as exc:
                    tmp.unlink(missing_ok=True)
                    message = str(exc)
                    if any(s in message.lower() for s in ['401', '403', 'forbidden', 'unauthorized']):
                        stop.set()
                        manifest['failed'].append({'key': key, 'error': message[:300]})
                        return
                    if attempt == 2:
                        manifest['failed'].append({'key': key, 'error': message[:300]})
                    else:
                        await asyncio.sleep(2 ** attempt * 2)
    await asyncio.gather(*(generate(k, t) for k, t in texts.items()))
    manifest['expectedCount'] = len(texts)
    manifest['generatedCount'] = len(manifest['generated'])
    manifest['complete'] = len(manifest['generated']) == len(texts)
    manifest['generatedAt'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'expected': len(texts), 'generated': len(manifest['generated']), 'failed': len(manifest['failed'])}), flush=True)
    if not manifest['complete']:
        # Preserve successful audio and the truthful manifest as an artifact.
        print('INCOMPLETE: inspect audio-manifest.json; do not claim full audio coverage.', flush=True)

if __name__ == '__main__':
    asyncio.run(main())
