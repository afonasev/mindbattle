import pathlib,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('apply',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
B=D/'qualified-class3-cycle1-sourceaa';p=m.read(B/'peer-snapshot.json')
m.apply(B,'01a141aa-bf07-7752-a28e-f9c6b25fe648',[88, 90, 91],D/'apply-class3-cycle1-sourceaa.json',D/'qa-class3-frbr96-final-snapshot.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':p['actualCurrentPeers']},concerns=['SoleaddressedSOURCEcycle1 exactly3notes, independentFINAL required. Allotherfields and89certified unchanged. Reusefulloriginalcontext, bindingnotnewprimarydownload.', 'Combinedfinalcatalog3notes+FRBR96 willgetoneaffected19snapshot, independentreceiptsseparateFINAL3/INITIAL1. SourceQA/rootREADY0qualitycredit.'])
