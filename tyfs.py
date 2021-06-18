#!/usr/bin/python3.6
# TODO :
# - en caso de que la especie no este presente, no escribirla.
#  - optimizar?
# 

import re
import sys

#def trues_falses(POSYDIN,ENES):
    # POSYDIN es la lista de posiciones con sus dinamicas
    # ENES es la cantidad de cada especie. 
filer=open(sys.argv[1],"r")
POSCAR=filer.read()
POSCAR=POSCAR.split('\n')
SPECSL=re.compile(r"^(\s+[A-Z]*[a-z])+")
DIRORCAR=re.compile(r"^Direct|Cart")
LN=enumerate(POSCAR)

# leer los átomos y la lista de especies. 
for linum, line in LN:
    if re.match(SPECSL,line ):
        HEAD=POSCAR[:linum]
        SPEC_LIST=line.split()
        linum,line=next(LN)
        SPEC_N=[int ( n ) for n in line.split()]
        TOTAL_N=sum(SPEC_N)
    if re.match(DIRORCAR,line):
        linum,line=next(LN)
        try:
            POSLIST=POSCAR[linum:linum+TOTAL_N]
        except Exception as e:
            print ( e )
        break

TRUES={}
FALSE={}
SPECS_T={}
SPECS_F={}
atom=enumerate(POSLIST)
spec=enumerate(SPEC_LIST)
for ospec,sym in spec:
        firs=sum(SPEC_N[:ospec])
        last=sum(SPEC_N[:ospec+1])-1
        FALSE[sym]=[line for line in POSLIST[firs:last+1] if "F" in line ]
        TRUES[sym]=[line for line in POSLIST[firs:last+1] if "T" in line ]
        SPECS_T[ sym ]=len(TRUES[sym])
        SPECS_F[ sym ]=len(FALSE[sym])

# y ahora escribo
TF=open('TRUES.vasp','w')
TF.write ("\n".join(HEAD)+"\n")
TF.write (" ".join(SPEC_LIST)+"\n")
TF.write (" ".join([str(SPECS_T[sym]) for sym in SPEC_LIST ] )+"\n")
TF.write("Selective Dynamics\nDirect")
for sym in SPEC_LIST:
    TF.write("\n"+"\n".join(TRUES[sym]))
# print (FALSE)
TF.close()

# y ahora escribo
FF=open('FALSE.vasp','w')
FF.write ("\n".join(HEAD)+"\n")
FF.write (" ".join(SPEC_LIST)+"\n")
FF.write (" ".join([str(SPECS_F[sym]) for sym in SPEC_LIST])+"\n")
FF.write("Selective Dynamics\nDirect")
for sym in SPEC_LIST:
    FF.write("\n"+"\n".join(FALSE[sym]))
# print (FALSE)
FF.close()
