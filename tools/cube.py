"""Minimal sticker-level 3x3 simulator used to check starter algs against the
OLL/PLL pictures in index.html."""
import re, json
FACES = {'U':(0,1,0),'D':(0,-1,0),'R':(1,0,0),'L':(-1,0,0),'F':(0,0,1),'B':(0,0,-1)}
def solved():
    st = {}
    for x in (-1,0,1):
        for y in (-1,0,1):
            for z in (-1,0,1):
                p=(x,y,z)
                for f,n in FACES.items():
                    if any(p[i]==n[i]!=0 for i in range(3)): st[(p,n)] = f
    return st
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def rot(v,a):  # clockwise 90 viewed from +a
    c=cross(a,v); d=sum(i*j for i,j in zip(a,v))
    return tuple(-c[i]+a[i]*d for i in range(3))
# move -> (axis, layer predicate on coordinate along axis)
def spec(m):
    base={'R':('R',lambda k:k==1),'L':('L',lambda k:k==1),'U':('U',lambda k:k==1),'D':('D',lambda k:k==1),
          'F':('F',lambda k:k==1),'B':('B',lambda k:k==1),
          'r':('R',lambda k:k>=0),'l':('L',lambda k:k>=0),'u':('U',lambda k:k>=0),'d':('D',lambda k:k>=0),
          'f':('F',lambda k:k>=0),'b':('B',lambda k:k>=0),
          'M':('L',lambda k:k==0),'E':('D',lambda k:k==0),'S':('F',lambda k:k==0),
          'x':('R',lambda k:True),'y':('U',lambda k:True),'z':('F',lambda k:True)}
    return base[m]
def apply(st, alg):
    for tok in re.findall(r"[RLUDFBrludfbMESxyz]w?[2']*'?", alg.replace('(', ' ').replace(')', ' ')):
        m=tok[0]; wide = 'w' in tok
        if wide: m=m.lower()
        n = 2 if '2' in tok else 1
        if tok.endswith("'"): n = 4-n if n==1 else 2
        face, pred = spec(m); a = FACES[face]
        for _ in range(n % 4):
            new={}
            for (p,nv),c in st.items():
                k=sum(i*j for i,j in zip(p,a))
                if pred(k): new[(rot(p,a),rot(nv,a))]=c
                else: new[(p,nv)]=c
            st=new
    return st
def invert(alg):
    toks=re.findall(r"[RLUDFBrludfbMESxyz]w?[2']*'?", alg.replace('(', ' ').replace(')', ' '))
    out=[]
    for t in reversed(toks):
        if '2' in t: out.append(t.replace("'",""))
        elif t.endswith("'"): out.append(t[:-1])
        else: out.append(t+"'")
    return ' '.join(out)
def readout(st):
    g=lambda p,n: st[(p,FACES[n])]
    u=''.join(g((c-1,1,r-1),'U') for r in range(3) for c in range(3))
    s = u + g((-1,1,-1),'L')+g((-1,1,-1),'B') + g((1,1,-1),'B')+g((1,1,-1),'R') \
          + g((-1,1,1),'F')+g((-1,1,1),'L') + g((1,1,1),'R')+g((1,1,1),'F') \
          + g((1,1,0),'R')+g((0,1,-1),'B')+g((-1,1,0),'L')+g((0,1,1),'F')
    return s
def centers_home(st):
    return all(st[(n,n)]==f for f,n in FACES.items())
def case_of(alg):  # state this alg solves, read in the fixed view
    st=apply(solved(), invert(alg)); return readout(st), centers_home(st)
def mask(s): return ''.join('U' if ch=='U' else '.' for ch in s)
