"""Checks every starter alg (and alternative) in index.html solves the exact
case picture the app shows, with no extra AUF.

    python3 tools/check_algs.py

OLL only has to match which stickers are yellow; PLL has to match all colors
(up to a final AUF, since a PLL can finish with the top layer turned).
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from cube import case_of, mask, apply, solved, readout

src = open(os.path.join(os.path.dirname(__file__), '..', 'index.html')).read()
OLL_PAT = json.loads(re.search(r'const OLL_PAT = (\[.*?\]);', src).group(1))
PLL_PAT = json.loads(re.search(r'const PLL_PAT = (\[.*?\]);', src).group(1))
PLL_NAMES = re.findall(r"'(\w+)'", re.search(r'const PLL_NAMES = \[(.*?)\];', src).group(1))

def block(name):
    i = src.index(f'const {name} = {{')
    return src[i:src.index('};', i)]

oll = {int(k): v for k, v in re.findall(r'^\s+(\d+): "([^"]+)"', block('OLL_DEFAULT_ALG'), re.M)}
pll = dict(re.findall(r'^\s+(\w+): "([^"]+)"', block('PLL_DEFAULT_ALG'), re.M))
alt = dict(re.findall(r"^\s+'([\w-]+)': \"([^\"]+)\"", block('DEFAULT_ALT_ALG'), re.M))

def check_oll(n, alg):
    return mask(case_of(alg)[0]) == mask(OLL_PAT[n - 1])

def check_pll(name, alg):
    want = PLL_PAT[PLL_NAMES.index(name)]
    return any(case_of(alg + ' ' + auf)[0] == want for auf in ('', 'U', 'U2', "U'"))

bad = 0
rows = [(f'OLL {n}', a, check_oll(n, a)) for n, a in sorted(oll.items())]
rows += [(f'PLL {k}', a, check_pll(k, a)) for k, a in pll.items()]
for cid, a in alt.items():
    kind, key = cid.split('-', 1)
    ok = check_oll(int(key), a) if kind == 'oll' else check_pll(key, a)
    rows.append((f'{kind.upper()} {key} (alt)', a, ok))
for label, a, ok in rows:
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'}  {label:14} {a}")
print(f'\n{len(rows) - bad}/{len(rows)} match their picture')
sys.exit(1 if bad else 0)
