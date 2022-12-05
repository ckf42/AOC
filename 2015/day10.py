import AOCInit
import util
import re

if __name__ != '__main__':
    exit()

inp = '1'

# atomic ele
eleTableRec = [
    'H 22 H',
    'He 13112221133211322112211213322112 Hf.Pa.H.Ca.Li',
    'Li 312211322212221121123222112 He',
    'Be 111312211312113221133211322112211213322112 Ge.Ca.Li',
    'B 1321132122211322212221121123222112 Be',
    'C 3113112211322112211213322112 B',
    'N 111312212221121123222112 C',
    'O 132112211213322112 N',
    'F 31121123222112 O',
    'Ne 111213322112 F',
    'Na 123222112 Ne',
    'Mg 3113322112 Pm.Na',
    'Al 1113222112 Mg',
    'Si 1322112 Al',
    'P 311311222112 Ho.Si',
    'S 1113122112 P',
    'Cl 132112 S',
    'Ar 3112 Cl',
    'K 1112 Ar',
    'Ca 12 K',
    'Sc 3113112221133112 Ho.Pa.H.Ca.Co',
    'Ti 11131221131112 Sc',
    'V 13211312 Ti',
    'Cr 31132 V',
    'Mn 111311222112 Cr.Si',
    'Fe 13122112 Mn',
    'Co 32112 Fe',
    'Ni 11133112 Zn.Co',
    'Cu 131112 Ni',
    'Zn 312 Cu',
    'Ga 13221133122211332 Eu.Ca.Ac.H.Ca.Zn',
    'Ge 31131122211311122113222 Ho.Ga',
    'As 11131221131211322113322112 Ge.Na',
    'Se 13211321222113222112 As',
    'Br 3113112211322112 Se',
    'Kr 11131221222112 Br',
    'Rb 1321122112 Kr',
    'Sr 3112112 Rb',
    'Y 1112133 Sr.U',
    'Zr 12322211331222113112211 Y.H.Ca.Tc',
    'Nb 1113122113322113111221131221 Er.Zr',
    'Mo 13211322211312113211 Nb',
    'Tc 311322113212221 Mo',
    'Ru 132211331222113112211 Eu.Ca.Tc',
    'Rh 311311222113111221131221 Ho.Ru',
    'Pd 111312211312113211 Rh',
    'Ag 132113212221 Pd',
    'Cd 3113112211 Ag',
    'In 11131221 Cd',
    'Sn 13211 In',
    'Sb 3112221 Pm.Sn',
    'Te 1322113312211 Eu.Ca.Sb',
    'I 311311222113111221 Ho.Te',
    'Xe 11131221131211 I',
    'Cs 13211321 Xe',
    'Ba 311311 Cs',
    'La 11131 Ba',
    'Ce 1321133112 La.H.Ca.Co',
    'Pr 31131112 Ce',
    'Nd 111312 Pr',
    'Pm 132 Nd',
    'Sm 311332 Pm.Ca.Zn',
    'Eu 1113222 Sm',
    'Gd 13221133112 Eu.Ca.Co',
    'Tb 3113112221131112 Ho.Gd',
    'Dy 111312211312 Tb',
    'Ho 1321132 Dy',
    'Er 311311222 Ho.Pm',
    'Tm 11131221133112 Er.Ca.Co',
    'Yb 1321131112 Tm',
    'Lu 311312 Yb',
    'Hf 11132 Lu',
    'Ta 13112221133211322112211213322113 Hf.Pa.H.Ca.W',
    'W 312211322212221121123222113 Ta',
    'Re 111312211312113221133211322112211213322113 Ge.Ca.W',
    'Os 1321132122211322212221121123222113 Re',
    'Ir 3113112211322112211213322113 Os',
    'Pt 111312212221121123222113 Ir',
    'Au 132112211213322113 Pt',
    'Hg 31121123222113 Au',
    'Tl 111213322113 Hg',
    'Pb 123222113 Tl',
    'Bi 3113322113 Pm.Pb',
    'Po 1113222113 Bi',
    'At 1322113 Po',
    'Rn 311311222113 Ho.At',
    'Fr 1113122113 Rn',
    'Ra 132113 Fr',
    'Ac 3113 Ra',
    'Th 1113 Ac',
    'Pa 13 Th',
    'U 3 Pa',
]
# transuranic ele
# for i in range(4, 10):
    # eleTableRec.append(f'Np{i} 1311222113321132211221121332211{i} Hf.Pa.H.Ca.Pu{i}')
    # eleTableRec.append(f'Pu{i} 31221132221222112112322211{i} Np{i}')
eleTableRec = list((l[0], l[1], l[2].split('.'))
                   for s in eleTableRec
                   if (l := s.split()))
runReg = re.compile(r'(\d)\1*')
tokenDict = {k: v for (v, k, _) in eleTableRec}
decayDict = {k: v for (k, _, v) in eleTableRec}
eleTableRec = {k: len(v) for (k, v, _) in eleTableRec}

def tokenize(s):
    """
    122 -> 1, 'H'
    """
    runSegList = list(m.group() for m in runReg.finditer(s))
    res = list()
    while len(runSegList) != 0:
        m = util.lastAccumSuchThat(runSegList, lambda x, y: x + y, lambda z: z in tokenDict)
        if m[0] is None:
            res.append(runSegList.pop(0))
        else:
            res.append(tokenDict[m[2]])
            runSegList = runSegList[m[0] + 1:]
    return tuple(res)

def simpleLasStep(s):
    """
    312 -> 131112
    """
    return ''.join(str(len(p)) + p[0] for m in runReg.finditer(s) if (p := m.group()))

def lasStep(tokens):
    """
    'Y' -> 'Sr', 'U'
    1 -> 11
    2 -> 'Ca'
    """
    return tuple(s
                 for t in tokens
                 for s in (tokenize(simpleLasStep(t)) if t[0].isdigit() else decayDict[t]))

def toLen(tokens):
    return sum((len(s) if s[0].isdigit() else eleTableRec[s]) for s in tokens)

inp = tokenize(inp)
# part 1
for i in range(40):
    inp = lasStep(inp)
print(toLen(inp))

# part 2
for i in range(10):
    inp = lasStep(inp)
print(toLen(inp))

