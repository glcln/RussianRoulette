import numpy as np
import matplotlib.pyplot as plt
from math import *
from random import *

def moyenne(Liste):
    return sum(Liste)/len(Liste)

def RandomMort(Nsurvi):
    mort = []
    for i in range(0,Nsurvi//2):
        mort.append(1)
    for i in range(Nsurvi//2,Nsurvi):
        mort.append(0)
    shuffle(mort)
    return mort

def supmoy(moy_coup,coup):
    if coup>moy_coup:
        marker=1
    else:
        marker=0
    return marker

## Main
plt.close()

N = 1000        # nombre participants
Nsurvi = N      # nombre de survivants
Nmort = 0       # nombre de morts à chaque tour
NmortTOT = 0    # nombre de morts total
moy_coup = 0    # nombre moyen de coups tirés à chaque tour
ntour = 0       # nombre de tours au total
pverif = 0      # probabilité d'évaluation de la mort
cpt_mort = 0   # nombre de survivants avec un nombre de coups choisi < à moy_coup

p_survi = [1,5./6,4./6,3./6,2./6,1./6,0]      # probabilité de survie de chaque coup (0 -> 6)
marker = []             # identifie ceux qui ont eu coup>moy_coup ("1") du reste des survivants ("0")
sum_marker = []         # nombre de joueurs qui ont eu coup>moy_coup au tour en cours
sum_marker.append(0)

# Données graphiques
List_survi = []
List_mort = []
List_ntour = []
List_moycoups = []
List_marker = []

List_survi.append(N)
List_mort.append(0)
List_ntour.append(0)
List_moycoups.append(0)
List_marker.append(0)


while (Nsurvi>=2):

    coup = np.zeros(Nsurvi, dtype=np.int64)               # nombre de coups choisi pour chaque joueur à chaque tour
    psurvi_parpep = np.zeros(Nsurvi, dtype=np.float64)    # probabilité de survie de chaque joueur
    mort = np.zeros(Nsurvi, dtype=np.int64)               # 1: mort, 0: vivant

    selec_mort = RandomMort(Nsurvi)


    print("Début tour:      Nsurvi=", Nsurvi,"  Nmort=", Nmort)
    for i in range(0, Nsurvi):
        coup[i] = fcoup()            #dépend de la loi de proba choisie
        psurvi_parpep[i] = p_survi[coup[i]]

        pverif=random()              #sélection de la mort, générée aléatoirement
        if psurvi_parpep[i] < pverif:
            mort[i] = 1
        else:
            mort[i] = 0

    Nmort = sum(mort)
    moy_coup = moyenne(coup)     # nombre moyen coups tirés sur l'ensemble des joueurs du tours (vivants et morts après le tir)
    List_moycoups.append(moy_coup)
    print("Moyenne de coups tirés: ",moy_coup)

    print("Avant 50% trié:  Nsurvi=", Nsurvi-Nmort,"  Nmort=", Nmort)
    for i in range(0, Nsurvi):
        if (coup[i] <= moy_coup) & (mort[i] == 0):
            if selec_mort[i]==1:
                mort[i]=1
                cpt_mort += 1
    Nmort += cpt_mort
    Nsurvi -= Nmort
    print("Fin tour:        Nsurvi=",Nsurvi,"  Nmort=",Nmort)
    List_mort.append(Nmort)
    List_survi.append(Nsurvi)
    NmortTOT = Nmort

    #Discriminer les survivants
    for i in range(0, Nsurvi+Nmort):
        if (mort[i] == 0):
            marker.append(supmoy(moy_coup,coup[i]))

    sum_marker.append(sum(marker))
    if ntour == 0:
        print("Avec coup>moyenne: ",sum_marker[1])
        List_marker.append(sum_marker[1])
    else:
        print("Avec coup>moyenne: ",sum_marker[ntour+1]-sum_marker[ntour])
        List_marker.append(sum_marker[ntour+1]-sum_marker[ntour])
    print("")
    Nmort = 0
    cpt_mort = 0
    ntour+=1
    List_ntour.append(ntour)


print("Nsurvi: ",Nsurvi," Tot: ",NmortTOT+Nsurvi," ntour: ",ntour) #OK

print(List_marker)



#Display:
fig, axs = plt.subplots(4)
axs[0].plot(List_ntour,List_survi,'.g-',label='Nombre de survivants')
axs[0].legend()
axs[1].plot(List_ntour,List_mort,'.r-',label='Nombre de morts')
axs[1].legend()
axs[2].plot(List_ntour,List_moycoups,'.b-',label='Moyenne des coups')
axs[2].legend()
axs[3].plot(List_ntour,List_marker,'.k-',label='Joueurs avec coup > Moyenne des coups')
axs[3].legend()
axs[3].set_xlabel("Nombre de tours")
fig.set_size_inches(10, 8)
plt.show()


## Loi uniforme de coups
plt.close()

N=10000

def fcoup():
    return randint(0,6)

coup = np.zeros(N,dtype=np.int64)
psurvi_parpep = np.zeros(N, dtype=np.float64)
p_survi = [1,5./6,4./6,3./6,2./6,1./6,0]


for i in range(0,N):
    coup[i]=fcoup()

plt.hist(coup, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5],color='blue',rwidth=0.85)
plt.axvline(x=moyenne(coup),color='red',label='moyenne: %3.2f' %moyenne(coup))
plt.grid(axis='y')
plt.title("Loi uniforme")
plt.ylabel("Fréquence")
plt.xlabel("Nombres de coups")
plt.legend()
plt.show()


## Loi exponentielle de coups
plt.close()

# lambda=esperance de la loi, à choisir pour "bien couper" la sélection
# lambda = ln(sqrt(2)): pour que P([0,2])=1/2, et coupure à 6 coups max

N=100000
lbd=np.log(np.sqrt(2))

def fcoup():
    coup=10;
    while coup>=7:
        coup=expovariate(lbd)
    return floor(coup)

coup = np.zeros(N,dtype=np.int64)
p_survi = [1,5./6,4./6,3./6,2./6,1./6,0]

exp_loi = []
x=[6*i/N for i in range (0,N)]

cpt_zeros=0

for i in range(0,N):
    coup[i]=fcoup()
    if coup[i]==0:
        cpt_zeros+=1

for i in range(0,N):
    exp_loi.append(cpt_zeros*np.exp(-lbd*x[i]))


print(moyenne(coup),1/lbd)


plt.hist(coup, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5],color='blue',rwidth=0.85)
plt.axvline(moyenne(coup),color='red',label='moyenne: %3.2f' %moyenne(coup))
plt.plot(x,exp_loi,'k--',label='modèle continu')
plt.grid(axis='y')
plt.title("Loi exponentielle de paramètre $\lambda=\ln{(\sqrt{2})}$")
plt.ylabel("Fréquence")
plt.xlabel("Nombres de coups")
plt.legend()
plt.show()


## Biais humain

#Ajout d'un biais

#si tour précédent coup>moy_coup ne pas choisir un coup < à moy_coup d'avant
#si l'inverse alors choisir coup > moy_coup d'avant

#En fait dans tous les cas, choisir coup > moy_coup du tour d'avant



