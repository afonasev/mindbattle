"""Apply one qualified exactSOURCE card, no quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;tp=C/'src/content/topics/national-parks-nature.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))]);a.apply(D/'qualified-parks4-source62','01a14262-8bca-7a42-9ef8-31c73fb38274',[4],D/'apply-parks4.json',D/'qa-parks4.json',pathlib.Path(__file__))
