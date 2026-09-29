from pathlib import Path
import json,subprocess,concurrent.futures,time,sys
import fitz
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent.parent;A=R/'katharine';Q=R/'katharine-qa';Q.mkdir(exist_ok=True)
results=[]
def ok(name,condition):
 results.append(dict(test=name,passed=bool(condition)))
 (Q/'test_results.json').write_text(json.dumps(results,indent=2))
 if not condition:raise AssertionError(name)
 print('PASS',name,flush=True)
# Validate every generated audio file, not merely the count in its manifest.
m=json.loads((A/'audio-manifest.json').read_text());files=[A/v['url'] for v in m['generated'].values()]
ok('694 existing neural files',len(files)==694 and all(f.is_file() and f.stat().st_size>1000 for f in files))
def probe(f):
 r=subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
 return [str(f),r.returncode,r.stderr] if r.returncode or r.stderr else None
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:audio_errors=[x for x in ex.map(probe,files) if x]
ok('Every MP3 decodes without errors',not audio_errors)
(Q/'audio_validation.json').write_text(json.dumps(dict(expected=694,found=len(files),decode_errors=audio_errors,bytes=sum(f.stat().st_size for f in files)),indent=2))
# Check page count, missing-glyph replacements and page-boundary overflow.
pdf_errors=[];page_count=0;pdfs=list((A/'pdfs').rglob('*.pdf'))
for f in pdfs:
 d=fitz.open(f);page_count+=len(d)
 if '05_Reference' not in str(f) and len(d)!=1:pdf_errors.append([str(f),'activity is not one page'])
 for n,p in enumerate(d):
  if '\ufffd' in p.get_text():pdf_errors.append([str(f),n,'replacement glyph'])
  for b in p.get_text('dict')['blocks']:
   if b['type']==0:
    for line in b['lines']:
     for s in line['spans']:
      x0,y0,x1,y1=s['bbox']
      if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:pdf_errors.append([str(f),n,s['text'],'outside page'])
for rel,name in [('01_Daily_Conversation/S01_CORE_01.pdf','pdf_basic'),('02_Optional_Extension/S17_EXT_01.pdf','pdf_extension'),('04_Word_Review/CH003_Words_C.pdf','pdf_choices'),('05_Reference/Vocabulary_by_POS.pdf','pdf_vocab')]:
 d=fitz.open(A/'pdfs'/rel);d[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(Q/(name+'.png'))
(Q/'pdf_validation.json').write_text(json.dumps(dict(files=len(pdfs),pages=page_count,issues=pdf_errors),ensure_ascii=False,indent=2));ok('All PDF activities are one page with no text outside the page',not pdf_errors)
# Scheduler checks run on the actual delivered module.
js='''const assert=require('node:assert/strict'),K=require('./katharine/scheduler.js');let n=new Date(2026,8,29,13).getTime(),tests=0;
function t(name,fn){fn();tests++;console.log(name);}
t('New is unscheduled',()=>assert.equal(K.blank().phase,'new'));
t('Again one minute',()=>assert.equal(K.schedule(K.blank(),1,n).due,n+K.MIN));
t('First Good ten minutes',()=>assert.equal(K.schedule(K.blank(),3,n).due,n+10*K.MIN));
t('Second Good graduates',()=>assert.equal(K.schedule(K.schedule(K.blank(),3,n),3,n+10*K.MIN).interval,1));
t('Easy is not instant mastery',()=>assert.equal(K.secure(K.schedule(K.blank(),4,n),n),false));
t('Stable success increases interval',()=>{let c=K.schedule(K.schedule(K.blank(),4,n),3,n+3*K.DAY);assert.equal(c.interval,8);assert.equal(K.secure(c,n+3*K.DAY),true);});
t('Overdue is not secure',()=>{let c=K.schedule(K.schedule(K.blank(),4,n),3,n+3*K.DAY);assert.equal(K.secure(c,c.due+1),false);});
t('Lapse resets successful dates',()=>{let c=K.schedule(K.schedule(K.blank(),4,n),1,n+3*K.DAY);assert.equal(c.lapses,1);assert.equal(c.goodDays.length,0);});
t('Same day not two successful dates',()=>assert.equal(K.schedule(K.schedule(K.blank(),3,n),3,n+10*K.MIN).goodDays.length,1));
t('No mutation of old card',()=>{let c=K.blank(),s=JSON.stringify(c);K.schedule(c,3,n);assert.equal(JSON.stringify(c),s);});
t('Minimum ease',()=>{let c=K.blank();for(let i=0;i<100;i++)c=K.schedule(c,1,n);assert.equal(c.ease,1.3);});
t('Maximum interval',()=>{let c=K.blank();for(let i=0;i<100;i++)c=K.schedule(c,4,n+i*K.DAY);assert.equal(c.interval,365);});
t('Invalid grade',()=>assert.throws(()=>K.schedule(K.blank(),5,n)));
t('Korean normalization',()=>assert.equal(K.normalize('들어요!'),K.normalize(' 들 어 요. ')));
t('Next local midnight',()=>{let d=new Date(K.nextDay(n));assert.equal(d.getDate(),30);assert.equal(d.getHours(),0);});console.log(JSON.stringify({schedulerTests:tests,passed:tests}));'''
r=subprocess.run(['node','-e',js],cwd=R,capture_output=True,text=True);(Q/'scheduler_results.txt').write_text(r.stdout+r.stderr);ok('15 scheduler unit tests',r.returncode==0)
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox']);ctx=browser.new_context(viewport=dict(width=1440,height=1050),accept_downloads=True);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8765');page.wait_for_selector('[data-action=start]');page.screenshot(path=str(Q/'app_desktop.png'),full_page=True)
 ok('308 complete vocabulary records',page.evaluate('KATHARINE_DATA.words.length')==308)
 ok('104 one-page activities',page.evaluate('KATHARINE_DATA.sheets.length')==104)
 assignment=page.evaluate('KATHARINE_DEBUG.dailySheet().id');page.reload();ok('Daily PDF stable after reload',page.evaluate('KATHARINE_DEBUG.dailySheet().id')==assignment)
 page.locator('[data-action=start]').first.click();page.locator('[data-action=reveal]').click();page.locator('[data-grade="3"]').click();st=page.evaluate('KATHARINE_DEBUG.getState()');ok('Grade persisted',len(st['history'])==1);first=st['history'][0]['id'];ok('Independent direction records',st['cards'][first]['r']['total']==1 and st['cards'][first]['p']['total']==0);ok('Production starts tomorrow',st['cards'][first]['unlockAt']>time.time()*1000)
 page.locator('[data-action=undo]').click();ok('Undo restores previous grade state',len(page.evaluate('KATHARINE_DEBUG.getState().history'))==0);page.locator('[data-grade="4"]').click();page.reload();ok('Learning survives refresh',len(page.evaluate('KATHARINE_DEBUG.getState().history'))==1)
 page.locator('[data-view=library]').click();page.fill('#search','들어요');ok('Search accepts conjugated form',page.locator('.wordrow .ko').first.inner_text()=='듣다');page.locator('.wordrow').first.click();page.fill('#wordNote','Test cue <safe>');page.locator('[data-save-word]').click();page.locator('#closeDialog').click();page.reload();page.locator('[data-view=library]').click();page.fill('#search','듣다');page.locator('.wordrow').first.click();ok('Private note saved and escaped',page.locator('#wordNote').input_value()=='Test cue <safe>');page.locator('[data-toggle-star]').click();page.locator('#closeDialog').click();page.locator('#starsOnly').check();ok('Star filter works',page.locator('.wordrow').count()==1)
 page.locator('[data-view=settings]').click();ok('Real neural manifest loaded','694' in page.locator('#main').inner_text())
 with page.expect_download() as di:page.locator('[data-action=export]').click()
 backup=Q/'test-backup.json';di.value.save_as(str(backup));before=page.evaluate('KATHARINE_DEBUG.getState()');ok('Backup contains actual progress',len(json.loads(backup.read_text())['history'])==1)
 page.evaluate("localStorage.removeItem('fly-korean-katharine-v1')");page.reload();page.locator('[data-view=settings]').click();page.once('dialog',lambda d:d.accept());page.locator('#importFile').set_input_files(str(backup));page.wait_for_timeout(250);ok('Backup import restores saved progress',page.evaluate('KATHARINE_DEBUG.getState().history.length')==1)
 page.locator('[data-view=patterns]').click();ok('All 26 patterns available',page.locator('.pattern-card').count()==26);page.locator('[data-view=progress]').click();page.screenshot(path=str(Q/'app_progress.png'),full_page=True)
 page.locator('[data-view=study]').click();page.locator('[data-action=reveal]').click();page.screenshot(path=str(Q/'app_card.png'),full_page=True);page.locator('[data-audio]').first.click();page.wait_for_timeout(200)
 ok('Generated audio is served as audio',page.evaluate("async()=>{let m=await(await fetch('audio-manifest.json')).json();let r=await fetch(Object.values(m.generated)[0].url);return r.ok&&r.headers.get('content-type').includes('audio');}"))
 ok('Invalid backup rejected',page.evaluate("()=>{try{KATHARINE_DEBUG.validate({version:999});return false;}catch(e){return true;}}"))
 # Simulate tomorrow to verify no Korean answer/audio leaks on a production front.
 page.evaluate("()=>{let s=KATHARINE_DEBUG.getState(),k=Object.keys(s.cards).find(k=>s.cards[k].firstDay);s.settings.direction='p';s.cards[k].unlockAt=Date.now()-1000;s.cards[k].r.lastDay='2000-01-01';localStorage.setItem('fly-korean-katharine-v1',JSON.stringify(s));}")
 page.reload();page.locator('[data-action=start]').first.click();ok('English-to-Korean front hides Korean audio',page.locator('.prompt.english').count()==1 and page.locator('[data-audio]').count()==0)
 mobile=browser.new_context(viewport=dict(width=390,height=844),is_mobile=True,device_scale_factor=1);mp=mobile.new_page();mp.on('pageerror',lambda e:errors.append(str(e)));mp.goto('http://127.0.0.1:8765');mp.wait_for_selector('[data-action=start]');mp.screenshot(path=str(Q/'app_mobile.png'),full_page=True);ok('Mobile dashboard fits width',mp.evaluate('document.documentElement.scrollWidth<=window.innerWidth'));mp.locator('[data-action=start]').first.click();mp.locator('[data-action=reveal]').click();mp.screenshot(path=str(Q/'app_mobile_card.png'),full_page=True);ok('Mobile card fits width',mp.evaluate('document.documentElement.scrollWidth<=window.innerWidth'))
 fp=browser.new_page();fp.on('pageerror',lambda e:errors.append(str(e)));fp.goto((A/'index.html').as_uri());fp.wait_for_selector('[data-action=start]');ok('Extracted local-file app opens',fp.evaluate('KATHARINE_DATA.words.length')==308)
 page.goto('http://127.0.0.1:8765');page.evaluate('navigator.serviceWorker.ready');page.wait_for_timeout(500);ctx.set_offline(True);page.reload();ok('Cached app opens offline',page.locator('[data-action=start]').count()>0);ctx.set_offline(False);ok('No JavaScript exceptions',not errors);browser.close()
(Q/'browser_errors.json').write_text(json.dumps(errors,indent=2));print('All validations completed')
