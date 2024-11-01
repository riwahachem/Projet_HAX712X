
import pandas as pd

#importation des données csv des courses velomagg durant l'année 2021
url="https://data.montpellier3m.fr/sites/defaukt/files/ressources/TAM_MMM_CoursesVelomagg_2021.csv"
path_target="../data/CoursesVelomagg_2021.csv"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)
df_CoursesVelomagg_2021=pd.read_csv("../data/CoursesVelomagg_2021.csv")
df_CoursesVelomagg_traité=df_CoursesVelomagg_2021.dropna()

data_2021=pd.read_excel('TAM_MMM_CoursesVelomagg_2021.xlsx')

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
        v=0
        c=0
        n=0
        for j in L:
            if j==i:
                c+=1
        for k in M:
            if i==[k[0],k[1]]:
                n=1
        if n==0:
            i.append(c)
            M.append(i)
            v+=1
    return M
