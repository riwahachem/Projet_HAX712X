
import pandas as pd
import numpy as np
import copy

filename="TAM_MMM_CoursesVelomagg_2022.csv"


def trajets_jour(j,m,a):
    if j<10:
        jj='0'+str(j)
    else :
        jj=str(j)
    if m<10:
        mm='0'+str(m)
    else :
        mm=str(m)
    aaaa=str(a)
    L=[]
    with open(filename) as f:
        for ligne in f :
            if ligne.split(",")[2]!='Deperture':
                x=ligne.split(",")
                if x[2].split('-')[0]==aaaa:
                    if x[2].split('-')[1]==mm:
                        if x[2].split('-')[2].split(' ')[0]==jj:
                            L.append([x[5],x[6]])
    M=[]
    for i in L:
        c=0
        n=0
        k=0
        for j in L:
            if j==i:
                c+=1
        if len(M)>0:
            while n==0 and k<len(M):
                if i==[M[k][0],M[k][1]]:
                    n=1 
                k+=1 
        if n==0:
            i.append(c)
            M.append(i)
    return M
  

def determination_jour(j,m,a):
    nombre_jour=0
    for i in range(1,m):
        if i%2==0 :
            if i==2:
                nombre_jour+=28
            elif i==8:
                nombre_jour+=31
            elif i==10 :
                nombre_jour+=31
            elif i==12 :
                nombre_jour+=31
            else :
                nombre_jour+=30
        if i%2==1:
            if i==9:
                nombre_jour+=30
            elif i==11:
                nombre_jour+=30
            else :
                nombre_jour+=31
    nombre_jour+=j
    jour=5+(nombre_jour%7)
    if jour>=7:
        return jour-7
    else :
        return jour
      

def données_jour_semaine(j,m,a):
    jour=determination_jour(j,m,a)
    M=[]
    L=[]
    W=[]
    with open(filename) as f :
        for ligne in f :
            if ligne.split(',')[2]!='Departure':
                x=ligne.split(',')
                if determination_jour(int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0]))==jour:
                    L.append(x)
                    if [int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0])] not in M:
                        M.append([int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0])])
                    if [x[5],x[6]] not in W:
                        W.append([x[5],x[6]])
    return L,M,W

def stats_jour(j,m,a):
    T=copy.deepcopy(données_jour_semaine(j,m,a)[0])
    M=copy.deepcopy(données_jour_semaine(j,m,a)[1])
    W=copy.deepcopy(données_jour_semaine(j,m,a)[2])
    L=[[i,0] for i in W]
    n=len(M)
    for x in T:
        if [int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0])] in M:
            j=W.index([x[5],x[6]])
            L[j][1]+=1/n
    return L

def stat_heure_jour(j,m,a):
    L=[0 for i in range(24)]
    t=0
    with open(filename) as f:
        for ligne in f :
            x=ligne.split(',')
            if x[2]!='Departure':
                if [int(x[2].split('-')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[2].split(' ')[0])]==[a,m,j]:
                    L[int(x[2].split('-')[2].split(' ')[1].split(':')[0])]+=1
                    t+=1
    L=[j/t for j in L]
    return L

def poids_heure(j,m,a):
    M=[]
    P=[0 for i in range(0,24)]
    L=[]
    with open(filename) as f:
        for ligne in f:
            x=ligne.split(',')
            if x[2]!='Departure':
                if determination_jour(int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0]))==determination_jour(j,m,a):
                    if [int(x[2].split('-')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[2].split(' ')[0])] not in L:
                        L.append([int(x[2].split('-')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[2].split(' ')[0])])
    for k in L:
        M.append(stat_heure_jour(k[2],k[1],k[0]))
    for i in range(0,24):
        for k in M:
            P[i]+=k[i]
    P=[j/len(M) for j in P]
    return P


#lundi=stats_jour_semaine(17,1,2022)
#mardi=stats_jour_semaine(18,1,2022)
#mercredi=stats_jour_semaine(19,1,2022)
#jeudi=stats_jour_semaine(13,1,2022)
#vendredi=stats_jour_semaine(14,1,2022)
#samedi=stats_jour_semaine(15,1,2022)
#dimanche=stats_jour_semaine(16,1,2022)
#semaine=[lundi,mardi,mercredi,jeudi,vendredi,samedi,dimanche]

#lundi_heure=poids_heure(17, 1, 2022)
#mardi_heure=poids_heure(18, 1, 2022)
#mercredi_heure=poids_heure(19, 1, 2022)
#jeudi_heure=poids_heure(13, 1, 2022)
#vendredi_heure=poids_heure(14, 1, 2022)
#samedi_heure=poids_heure(15, 1, 2022)
#dimanche_heure=poids_heure(16, 1, 2022)
#semaine_heure=[lundi_heure,mardi_heure,mercredi_heure,jeudi_heure,vendredi_heure,samedi_heure,dimanche_heure]
