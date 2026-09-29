"""Single build entrypoint, including documented content curation before audit."""
from pathlib import Path
import runpy,json,csv
S=Path(__file__).resolve().parent;A=S.parent/'katharine'
for name in ['enrich.py','questions.py','patterns.py']:runpy.run_path(str(S/name),run_name='__main__')
words=json.loads((A/'words.json').read_text())
for w in words:
 if w['ko'] in ['여기','거기','저기','어디']:w['ch']=2
 if w['ko'] in ['여러분','누구']:w['ch']=5
 if w['ko']=='묻다':w['note']='Asking uses the irregular polite form shown above. The homograph meaning bury is regular and is not tested here.'
(A/'words.json').write_text(json.dumps(words,ensure_ascii=False,indent=2))
with (A/'Vocabulary_Complete.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f);keys=['id','pos','group','ch','ko','yo','en','example','exampleEn','source','note'];wr.writerow(['ID','Part of speech','Group','Chapter','Dictionary / word','Polite form','English','Korean example','English example','Source','Notes'])
 for w in words:wr.writerow([w[k] for k in keys])
for name in ['build.py','assets.py']:runpy.run_path(str(S/name),run_name='__main__')
p=A/'README.md';p.write_text(p.read_text().replace('Run enrich.py, questions.py, patterns.py, build.py and assets.py in that order.','Run `python katharine-src/run.py` from the repository root. This applies curated notes and correct source-chapter labels before the vocabulary audit.'))
