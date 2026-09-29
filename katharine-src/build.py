"""Build print artifacts and perform an explicit, bounded lexical coverage audit."""
from pathlib import Path
import json,re,csv,collections
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor,black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,KeepTogether,PageBreak
from reportlab.lib.styles import ParagraphStyle
A=Path(__file__).resolve().parent.parent/'katharine';P=A/'pdfs';P.mkdir(exist_ok=True)
load=lambda n:json.loads((A/(n+'.json')).read_text())
words=load('words');questions=load('questions');patterns=load('patterns');grammar=load('grammar');tests=load('word_tests');practice=load('sentence_practice');stages=load('stages')
# Supplementary source examples/answers are retained for lexical auditing, not extra daily workload.
source_examples='''친구가 와요.
학생이 공부해요.
아이가 밥을 먹어요.
선생님이 책을 읽어요.
학교가 커요.
저는 한국어를 공부해요.
친구는 커피를 좋아해요.
한국어는 재미있어요.
물을 마셔요.
밥을 먹어요.
책을 읽어요.
사진을 봐요.
한국어를 공부해요.
숙제를 해요.
저는 커피를 마셔요.
친구는 영화를 봐요.
동생이 밥을 먹어요.
저는 집에 있어요.
학교에 가요.
공항에 도착해요.
병원에 가요.
카페에서 공부해요.
식당에서 밥을 먹어요.
사무실에서 일해요.
도서관에서 책을 읽어요.
집에 있어요.
집에 가요.
집에서 공부해요.
지하철로 회사에 가요.
택시로 병원에 가요.
왼쪽으로 가요.
천천히 오른쪽으로 가요.
가위로 종이를 잘라요.
컴퓨터로 이메일을 보내요.
젓가락으로 밥을 먹어요.
종이로 만들어요.
나무로 만들어요.
유리로 만들어요.
플라스틱으로 만들어요.
친구도 와요.
커피도 좋아해요.
빵도 먹어요.
영화도 봐요.
커피를 마셔요.
차도 마셔요.
커피만 마셔요.
빵만 먹어요.
한국어만 공부해요.
휴대폰만 있어요.
어머니의 휴대폰이에요.
친구의 책이에요.
선생님의 가방이에요.
강아지한테 밥을 줘요.
친구한테 문자를 보내요.
동료에게 이메일을 보내요.
친구한테 전화해요.
사장님에게 연락해요.
선생님에게 질문해요.
경찰에게 물어요.
선배한테 부탁해요.
후배에게 알려줘요.
저는 카페에서 커피를 마셔요.
저는 카페에서 친구를 만나요.
저는 친구한테 선물을 줘요.
저는 오늘 버스로 카페에 가요.
저는 커피만 마셔요.
저는 버스로 학교에 가요.
저는 도서관에서 책을 읽어요.
저는 친구한테 사진을 보내요.
네, 아버지는 커피를 좋아해요.
아니요. 어머니는 차만 마셔요.
네, 카페에 가요.
카페에 가요.
버스로 가요.
버스로 카페에 가요.
도서관에서 공부해요.
도서관에서 한국어를 공부해요.
친구한테 보내요.
사진을 보내요.
친구한테 사진을 보내요.
어머니한테 줘요.
꽃이에요.
어머니한테 꽃을 줘요.
오늘 학교에 가요.
버스로 학교에 가요.
학교에서 한국어를 공부해요.
공원에 가요.
자전거로 공원에 가요.
공원에서 친구를 만나요.
친구한테 사진을 보여줘요.
저는 학생이에요.
카페에서 커피를 마셔요.
빵도 먹어요.
이건 제 가방이에요.
친구한테 메시지를 보내요.
친구한테 사진도 보내요.
친구도 한국어를 공부해요.
공원에서 운동해요.
학교.
오른쪽으로 가세요.
한국어의 단어가 재미있어요.'''.splitlines()
contrast=['커피도 / 커피만','한국어도 / 한국어만','친구도 / 친구만','영화도 / 영화만','빵도 / 빵만']
forms={}
for w in words:
 for s in [w['ko'],w['yo'],*w['aliases']]:
  for v in s.split(' / '):
   if v:forms.setdefault(v,w['ko'])
 if w['yo']:forms.setdefault(w['ko'][:-1],w['ko'])
manual={'누가':'누구','뭘':'뭐','뭐예요':'뭐','이건':'이것','이거':'이것','제가':'저','저의':'저','내가':'나','내':'나','교수님':'교수','같은':'같다','모르는':'모르다','가는':'가다','갈':'가다','산':'사다','여행한':'여행하다','가세요':'가다','사세요':'살다','알고':'알다','가지고':'가지다','잃어버렸어요':'잃어버리다','만나면':'만나다','찾으면':'찾다','없으면':'없다','있으면':'있다','뭐라고':'뭐'}
forms.update(manual)
suffixes='한테도 에게도 에서도 으로도 로도 에만 에서만 의 이 가 은 는 을 를 에 에서 에게 한테 으로 로 도 만 과 와 하고 랑 이랑 까지 예요 이에요 고 면 으면 은 ㄴ 세요 요'.split()
allowed=re.compile('^(?:'+'|'.join(sorted(map(re.escape,set(suffixes)),key=len,reverse=True))+')+$')
fragments=set('이 가 은 는 을 를 에 에서 으로 로 도 만 의 에게 한테 아요 어요 해요 요 다 으 이에요 예요 세요 시 고 면 으면 았 었 와 과 하고 이랑 랑 까지 이라고 라고 님 님에게 게 도록 보다'.split())
corpus=[]
def add(id,text):
 if text:corpus.append((id,text))
for w in words:add(w['id']+' example',w['example']);add(w['id']+' note',w['note'])
for q in questions:add(q['id']+' original',q['original']);add(q['id']+' revised',q['ko'])
for p in patterns:
 add(p['id']+' form',p['form']);add(p['id']+' tip',p['tip'])
 for e in p['examples']:add(p['id']+' example',e['ko'])
for i,s in enumerate(source_examples+contrast):add('source-'+str(i),s)
for q in tests:add(q['id'],q['ko'])
for q in practice:add(q['id']+' model',q['model'])
rows=[];unresolved=collections.defaultdict(list);usage=collections.defaultdict(set);ordered=sorted(forms,key=len,reverse=True)
for id,text in corpus:
 for token in re.findall('[가-힣]+',text):
  match=forms.get(token)
  if not match and token in fragments:match='[grammar]'
  if not match:
   for f in ordered:
    if token.startswith(f) and allowed.fullmatch(token[len(f):] or '\0'):match=forms[f];break
  if not match:unresolved[token].append(id)
  else:usage[match].add(id)
  rows.append([id,token,match or '', 'covered' if match else 'REVIEW'])
with (A/'Vocabulary_Audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f);wr.writerow(['source','surface token','headword / grammar','status']);wr.writerows(rows)
audit=dict(method='Deterministic headword/surface-form and suffix audit with manually mapped irregular forms; not a general-purpose morphological analyzer.',scope='Saved original/revised learner questions, vocabulary examples, pattern forms/examples/tips, original word tests, model answers and Korean snippets in learner notes. Korean teacher-only explanatory prose is replaced by English instructions, not assigned as student vocabulary.',entries=len(corpus),tokens=len(rows),unique_tokens=len(set(r[1] for r in rows)),unresolved=dict(unresolved),words=len(words),polite_forms=sum(bool(w['yo']) for w in words),added_words=[w['ko'] for w in words if w['ch']==0])
(A/'audit_report.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));(A/'word_usage.json').write_text(json.dumps({k:sorted(v) for k,v in usage.items()},ensure_ascii=False,indent=2));(A/'source_examples.json').write_text(json.dumps(source_examples,ensure_ascii=False,indent=2))
if unresolved:raise ValueError('Unmapped source vocabulary: '+json.dumps(dict(unresolved),ensure_ascii=False))
# The platform font is embedded in PDFs only; never copied into the downloadable bundle.
pdfmetrics.registerFont(TTFont('KR','/usr/share/fonts/truetype/nanum/NanumGothic.ttf'));pdfmetrics.registerFont(TTFont('KR-Bold','/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'))
W,H=A4;sheets=[]
def wrap(text,font,size,width):
 out=[];line=''
 for char in str(text):
  if pdfmetrics.stringWidth(line+char,font,size)>width and line:
   if char!=' ' and line.rfind(' ')>len(line)*.5:prev,rest=line.rsplit(' ',1);out.append(prev);line=rest+char
   else:out.append(line.rstrip());line=char.lstrip()
  else:line+=char
 if line:out.append(line.rstrip())
 return out

def sheet(file,title,items,ch,extension=False,kind='conversation',instruction=''):
 path=P/file;path.parent.mkdir(parents=True,exist_ok=True);c=canvas.Canvas(str(path),pagesize=A4,pageCompression=1);c.setTitle('Katharine Korean / '+title);c.setAuthor('Fly Korean / Jay')
 c.setFillColor(HexColor('#39443e'));c.setFont('Helvetica-Bold',8.5);c.drawString(36,H-33,'FLY KOREAN  /  KATHARINE');c.setFont('Helvetica',8);c.drawRightString(W-36,H-33,'OPTIONAL EXTENSION' if extension else 'ONE PAGE / DAILY SPEAKING')
 y=H-64;c.setFillColor(black);c.setFont('Helvetica-Bold',18)
 for line in wrap(title,'Helvetica-Bold',18,W-72):c.drawString(36,y,line);y-=22
 c.setFont('Helvetica',8.5);c.setFillColor(HexColor('#424a50'));c.drawString(36,y-1,f'Chapters 001-{ch:03}. One sheet only. Real or imaginary answers are both welcome.')
 y-=20;instruction=instruction or 'Read each question and answer aloud. Highlight unknown words; write their meanings in the far-right column.'
 for line in wrap(instruction,'Helvetica',8.6,W-72):c.drawString(36,y,line);y-=12
 top=min(y-24,H-154);fold=424;right=441;c.setFont('Helvetica-Bold',8);c.drawString(36,top+5,'SPEAK ALOUD');c.drawString(right,top+5,'WORD / MEANING');c.setFont('Helvetica',7);c.drawString(right,top-7,'Fold or cover this column.')
 c.setStrokeColor(HexColor('#b9bdc0'));c.setDash(2,3);c.line(fold,top+15,fold,75);c.setDash();row_h=min(73,(top-95)/8)
 for i,item in enumerate(items):
  text=item['ko'];yy=top-34-i*row_h;size=13.5 if kind=='word-test' and ('____' in text or len(text)>32) else 15
  if not re.search('[가-힣]',text):size=12
  lines=wrap(text,'KR',size,340)
  if len(lines)>3:size=11.5;lines=wrap(text,'KR',size,340)
  c.setFillColor(HexColor('#707974'));c.setFont('Helvetica',8);c.drawString(36,yy+2,f'{i+1:02}');c.setFillColor(black);c.setFont('KR',size)
  for li,line in enumerate(lines):c.drawString(57,yy-li*(size+5),line)
  ly=yy-(len(lines)-1)*(size+5)-4;start=min(57+pdfmetrics.stringWidth(lines[-1],'KR',size)+9,407);c.setStrokeColor(HexColor('#b8bdc1'));c.setLineWidth(.45);c.setDash(1,3);c.line(start,ly,right-8,ly);c.setDash();c.setStrokeColor(HexColor('#899094'));c.line(right,yy-5,W-36,yy-5);c.line(right,yy-27,W-36,yy-27)
  if item.get('note'):
   c.setFont('Helvetica',7);c.setFillColor(HexColor('#6a736d'));note=wrap(item['note'],'Helvetica',7,340)[0];c.drawString(57,yy-len(lines)*(size+5)-9,note)
 c.setStrokeColor(HexColor('#ccd0d2'));c.line(36,66,W-36,66);c.setFillColor(HexColor('#4b5155'));c.setFont('Helvetica',8);c.drawString(36,51,'FIRST PASS  [ ]    SECOND PASS WITHOUT NOTES  [ ]    DATE: ______________');c.setFont('Helvetica',7.6);c.drawString(36,37,'No written answers needed. Cover your notes, answer again, and stop after this page.');c.save()
 sheets.append(dict(id=Path(file).stem,title=title,url='pdfs/'+file,ch=ch,extension=extension,kind=kind,questions=[x['ko'] for x in items],questionIds=[x.get('id','') for x in items]))
for st in stages:
 for ext in [False,True]:
  qs=[q for q in questions if q['stage']==st['id'] and q['extension']==ext]
  for start in range(0,len(qs),8):
   n=start//8+1;folder='02_Optional_Extension' if ext else '01_Daily_Conversation';sheet(f'{folder}/S{st["id"]:02}_{"EXT" if ext else "CORE"}_{n:02}.pdf',f'{st["title"]} / {n}',qs[start:start+8],st['ch'],ext)
for ch in range(1,6):
 qs=[q for q in practice if q['ch']==ch]
 for start in range(0,len(qs),8):
  n=start//8+1;sheet(f'03_Sentence_Practice/CH{ch:03}_Sentences_{n:02}.pdf',f'Chapter {ch:03} / Build a sentence {n}',qs[start:start+8],ch,kind='sentence-practice',instruction=qs[0]['instruction'])
 for part in 'ABCD':
  qs=[q for q in tests if q['ch']==ch and q['part']==part];sheet(f'04_Word_Review/CH{ch:03}_Words_{part}.pdf',f'Chapter {ch:03} / Word review {part}',qs,ch,kind='word-test',instruction=qs[0]['instruction'])
mission=['Who are you? Say one sentence.','Where do you go today? How do you go there?','What do you do there? Say two sentences.','What do you also do? What do you only do?','Describe one item and its owner.','Who do you contact? What do you send or give?','Tell your whole story again in five short sentences.','Ask your teacher one question about their day.']
sheet('03_Sentence_Practice/Final_Speaking_Mission.pdf','Your day / One connected story',[dict(id=f'M-{i+1}',ko=s) for i,s in enumerate(mission)],5,kind='mission',instruction='Speak in short Korean sentences. You may tell an imaginary story. Use only words you know.')
sheet('03_Sentence_Practice/Also_Only_Contrast.pdf','Also or only / Change the meaning',[dict(id=f'C-{i+1}',ko=s) for i,s in enumerate(contrast)],4,kind='contrast',instruction='For each pair, make two Korean sentences. Say how the meaning changes. No written answer is needed.')
# Reference documents are not part of the random daily pool.
body=ParagraphStyle('Body',fontName='KR',fontSize=9.3,leading=14,spaceAfter=6,wordWrap='CJK');small=ParagraphStyle('Small',parent=body,fontSize=8.2,leading=12,spaceAfter=0);h1=ParagraphStyle('H1',parent=body,fontName='KR-Bold',fontSize=19,leading=26,spaceAfter=12);h2=ParagraphStyle('H2',parent=body,fontName='KR-Bold',fontSize=12,leading=17,spaceBefore=12,spaceAfter=8)
def para(t,style=body):return Paragraph(escape(str(t)).replace('\n','<br/>'),style)
def footer(c,d):
 c.setFont('Helvetica',8);c.setFillColor(HexColor('#666666'));c.drawString(36,27,'KATHARINE / FLY KOREAN / REFERENCE - NOT A DAILY ASSIGNMENT');c.drawRightString(W-36,27,str(d.page))
def doc(name,story):
 path=P/'05_Reference'/name;path.parent.mkdir(exist_ok=True);SimpleDocTemplate(str(path),pagesize=A4,leftMargin=36,rightMargin=36,topMargin=36,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
def table(rows,widths):
 t=Table([[para(x,small) for x in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#edf0f2')),('LINEBELOW',(0,0),(-1,0),.7,HexColor('#889095')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,1),(-1,-1),.25,HexColor('#d6dadd'))]));return t
story=[para('Vocabulary / All 308 entries',h1),para('Original 250 words plus 58 additions from the sentences. Verbs and adjectives show dictionary and polite forms. Every app card and the CSV contain a Korean example and its English translation.')]
for pos in ['Pronoun','Noun','Dependent noun','Verb','Adjective','Auxiliary','Copula','Adverb','Determiner','Interjection']:
 arr=[w for w in words if w['pos']==pos]
 if not arr:continue
 story+=[para(pos,h2),table([['Word / dictionary','Polite (-yo)','English meaning','Source']]+[[w['ko'],w['yo'] or '-',w['en'],f'CH{w["ch"]:03}' if w['ch'] else 'Added'] for w in arr],[98,101,269,55])]
doc('Vocabulary_by_POS.pdf',story)
doc('Verb_Adjective_Forms.pdf',[para('Dictionary + polite forms',h1),para('78 conjugating entries. Forms are supplied explicitly, not guessed from a suffix rule.'),table([['Part of speech','Dictionary','Polite','Meaning']]+[[w['pos'],w['ko'],w['yo'],w['en']] for w in words if w['yo']],[66,102,130,225])])
story=[para('Sentence patterns / Chapters 001-005',h1),para('Use the pattern needed for today, not the whole reference book.')]
for p in patterns:
 block=[para(p['id']+' / '+p['title'],h2),para(p['form']),para(p['en'])]
 for e in p['examples']:block+=[para(e['ko']),para(e['en'],small)]
 if p['tip']:block.append(para(p['tip'],small))
 block.append(Spacer(1,8));story.append(KeepTogether(block))
story += [PageBreak(),para('Grammar and surface forms',h1),table([['Form','Meaning','Scope']]+[[g['ko'],g['en'],g['level']] for g in grammar],[111,328,84])];doc('Sentence_Patterns_and_Grammar.pdf',story)
story=[para('Teacher guide and coverage audit',h1),para('Give the learner ONE daily sheet. Use five new words and due reviews as a gentle default. A short answer is natural conversation, not automatically wrong: use the second pass to build complete sentences.'),para('Respect, role-play and privacy',h2),para('Use imaginary answers for family, jobs, travel and health questions. Do not demand private addresses or phone numbers. For parents/grandparents, introduce the respectful 사세요 when ready; source-level 살아요 forms are retained for grammar continuity. The male-speaker sibling questions are explicitly role-play.'),para('Core vs extension',h2),para('Past, wanting, ability, experience, conditionals and noun modifiers are separated into optional sheets. They do not enter the default daily pool. The original wording remains in questions.json. All 150 original word-test items remain; Part C allows any suitable choice because several original choices can be valid.'),para('Revised standalone questions',h2),table([['Original','Revised']]+[[q['original'],q['ko']] for q in questions if q['ko']!=q['original']],[262,261]),para('Audit scope and method',h2),para(audit['scope']),para(audit['method']),para(f'{audit["entries"]} corpus entries, {audit["tokens"]} Korean token occurrences, {audit["unique_tokens"]} distinct surface tokens; zero unresolved tokens in this saved corpus.'),para('Added vocabulary',h2),para(' / '.join(audit['added_words'])),para('Local storage and grading',h2),para('Progress is local to the browser and website address; it is not synced to the teacher. Export backups regularly. Device/browser changes and clearing site data can erase progress. English glosses allow alternatives: exact typing mismatch must not be treated as proof of a wrong answer. Local microphone playback has no automated pronunciation score.')]
doc('Teacher_Guide_and_Audit.pdf',story)
D=dict(version=1,student='Katharine',words=words,questions=questions,patterns=patterns,grammar=grammar,sheets=sheets)
(A/'data.json').write_text(json.dumps(D,ensure_ascii=False,separators=(',',':')));(A/'data.js').write_text('window.KATHARINE_DATA='+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';')
(A/'sheets.json').write_text(json.dumps(sheets,ensure_ascii=False,indent=2));(A/'PDF_Index.md').write_text('# One sheet per day\n\n'+'\n'.join(f'- {s["url"]}: {s["title"]}' for s in sheets))
summary=dict(words=len(words),polite_forms=78,audio_files=694,conversation_questions=len(questions),activity_sheets=len(sheets),core_sheets=sum(not s['extension'] for s in sheets),extension_sheets=sum(s['extension'] for s in sheets),pdf_files=len(list(P.rglob('*.pdf'))),practice_items=sum(len(s['questions']) for s in sheets))
(A/'build_summary.json').write_text(json.dumps(summary,indent=2));print(summary)
