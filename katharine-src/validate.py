"""Run regression suite and always retain precise browser error diagnostics."""
from pathlib import Path
source=Path(__file__).with_name('test.py')
text=source.read_text()
marker="ok('No JavaScript exceptions',not errors)"
assert text.count(marker)==1
text=text.replace(marker,"(Q/'browser_errors.json').write_text(json.dumps(errors,indent=2));print('BROWSER_ERRORS:',json.dumps(errors),flush=True);"+marker)
text=text.replace("lambda e:errors.append(str(e))","lambda e:errors.append(str(e)+' | '+str(getattr(e,'stack','')))" )
exec(compile(text,str(source),'exec'),{'__name__':'__main__','__file__':str(source)})
