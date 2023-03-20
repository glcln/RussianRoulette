import numpy as np
import matplotlib.pyplot as plt
from math import *
from random import *

N = 10000     # nombre participants
Nsurvi=N     # nombre de survivants
Nmort=0      # nombre de morts à chaque tour
NmortTOT=0   # nombre de morts total
moy_coup=0   # nombre moyen de coups tirés à chaque tour
ntour=0      # nombre de tours au total
pverif=0     # probabilité d'évaluation de la mort

p_survi=[1,5./6,4./6,3./6,2./6,1./6,0]      # probabilité de survie de chaque coup (0 -> 6)


while (Nsurvi>2):

    coup = np.zeros(Nsurvi,dtype=np.int64)               # nombre de coups choisi pour chaque joueur à chaque tour
    psurvi_parpep = np.zeros(Nsurvi,dtype=np.float64)    # probabilité de survie de chaque joueur
    mort = np.zeros(Nsurvi,dtype=np.int64)               # 1: mort, 0: vivant

    print("Début tour: ",Nsurvi,Nmort)
    for i in range(0,Nsurvi):
        coup[i] = randint(0,6)
        psurvi_parpep[i]=p_survi[coup[i]]

        pverif=random()              #sélection de la mort, générée aléatoirement
        if psurvi_parpep[i]<pverif:
            mort[i]=1
        else:
            mort[i]=0

    Nmort=sum(mort)
    moy_coup=sum(coup)/len(coup)     # nb moyen coup tiré
    print("Moyenne de coups tirés: ",moy_coup)

    print("Avant 50% trié: ",Nsurvi, Nmort)
    for i in range(0,Nsurvi):
        if (coup[i]<moy_coup)&(mort[i]==0):
            Nmort+=1

    Nsurvi-=Nmort
    print("Fin tour: ",Nsurvi,Nmort)
    ntour+=1
    NmortTOT+=Nmort
    Nmort=0


print("Nsurvi: ",Nsurvi," Tot: ",NmortTOT+Nsurvi," ntour: ",ntour) #OK





