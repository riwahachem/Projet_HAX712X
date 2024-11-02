
import pandas as pd
import numpy as np

#importation des données csv des courses velomagg durant l'année 2021
url="https://data.montpellier3m.fr/sites/defaukt/files/ressources/TAM_MMM_CoursesVelomagg_2021.csv"
path_target="../data/CoursesVelomagg_2021.csv"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)
df_CoursesVelomagg_2021=pd.read_csv("../data/CoursesVelomagg_2021.csv")
df_CoursesVelomagg_traité=df_CoursesVelomagg_2021.dropna()

data_2021=pd.read_excel('TAM_MMM_CoursesVelomagg_2021.xlsx')
filename = 'TAM_MMM_CoursesVelomagg_2022.csv'

def data(date, heure, depart, arrivee) :
  L=[]
  with open(filename) as f:
    for ligne in f :
      if ligne.split(",")[2]!= 'Departure' :
        x=ligne.split(",")
        if heure.split("h")[0] == x[2].split("-")[2].split(" ")[1].split(":")[0]:
          if x[5].split(" ")[1,:] ==depart.split(" "):
            if x[6].split(" ")[1,:] == arrivee.split(" "):
              L.append([x[5],x[6]])
  return L

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
      

def stats_jour(j,m,a):
    L=[]
    jour=determination_jour(j, m, a)
    with open (filename) as f:
        for ligne in f: 
            if ligne.split(',')[2]!='Departure':
                x=ligne.split(',')
                if determination_jour(int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0]))==jour:
                    L.append([x[5],x[6]])
    nombre_trajet=len(L)
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
            i.append(c/nombre_trajet)
            M.append(i)
    return M

lundi=stats_jour(17,1,2022)
mardi=stats_jour(18,1,2022)
mercredi=stats_jour(19,1,2022)
jeudi=stats_jour(13,1,2022)
vendredi=stats_jour(14,1,2022)
samedi=stats_jour(15,1,2022)
dimanche=stats_jour(16,1,2022)
semaine=[lundi,mardi,mercredi,jeudi,vendredi,samedi,dimanche]
