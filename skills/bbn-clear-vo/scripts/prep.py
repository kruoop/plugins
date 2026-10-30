# User's script (one phrase per line, blank line between thoughts, "-" = syllable hints) -> TTS paragraph files.
#   python3 prep.py script.txt            (run from the episode folder; writes vo/text/pNN-1.txt, vo/script_asm.txt, vo/captions.txt)
# Captions keep the user's words (hyphens dropped); only the TTS text gets lexicon.tsv spellings.
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
lex = [l.rstrip('\n').split('\t')[:2] for l in open(os.path.join(HERE, '..', 'references', 'lexicon.tsv'), encoding='utf-8')
       if l.strip() and not l.startswith('#')]


def tts(s):
    for a, b in lex:
        s = re.sub(a, b, s)
    return s


paras = [[l.strip().replace('-', '') for l in p.split('\n') if l.strip()]
         for p in re.split(r'\n\s*\n', open(sys.argv[1], encoding='utf-8').read()) if p.strip()]
groups, i = [], 0
while i < len(paras):  # a name-only paragraph ("ตัวที่สอง ออมนิรูท") is too short to read well alone: join it to the next one
    if len(paras[i]) == 1 and i + 1 < len(paras):
        groups.append(paras[i] + paras[i + 1]); i += 2
    else:
        groups.append(paras[i]); i += 1
os.makedirs('vo/text', exist_ok=True)
with open('vo/script_asm.txt', 'w', encoding='utf-8') as asm, open('vo/captions.txt', 'w', encoding='utf-8') as cap:
    for n, g in enumerate(groups, 1):
        lines = [tts(l) for l in g]
        open(f'vo/text/p{n:02d}-1.txt', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
        asm.write(f'[p{n:02d}]\n' + ' '.join(lines) + '\n')
        cap.write('\n'.join(g) + '\n\n')
        print(f'p{n:02d}: ' + ' / '.join(lines))
