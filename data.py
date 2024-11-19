
import pandas as pd
import numpy as np
import copy

filename="TAM_MMM_CoursesVelomagg_2022.csv"

archives =['MMM_EcoCompt_ED223110495_archive.json','MMM_EcoCompt_ED223110496_archive.json','MMM_EcoCompt_ED223110497_archive.json',
           'MMM_EcoCompt_ED223110500_archive.json','MMM_EcoCompt_ED223110501_archive.json','MMM_EcoCompt_X2H19070220_archive.json',
           'MMM_EcoCompt_X2H20042632_archive.json','MMM_EcoCompt_X2H20042633_archive.json','MMM_EcoCompt_X2H20042634_archive.json',
           'MMM_EcoCompt_X2H20042635_archive.json','MMM_EcoCompt_X2H20063161_archive.json','MMM_EcoCompt_X2H20063162_archive.json',
           'MMM_EcoCompt_X2H20063163_archive.json','MMM_EcoCompt_X2H20063164_archive.json','MMM_EcoCompt_X2H20104132_archive.json',
           'MMM_EcoCompt_X2H21070341_archive.json','MMM_EcoCompt_X2H21070342_archive.json','MMM_EcoCompt_X2H21070343_archive.json',
           'MMM_EcoCompt_X2H21070344_archive.json','MMM_EcoCompt_X2H21070345_archive.json','MMM_EcoCompt_X2H21070346_archive.json',
           'MMM_EcoCompt_X2H21070347_archive.json','MMM_EcoCompt_X2H21070348_archive.json','MMM_EcoCompt_X2H21070349_archive.json',
           'MMM_EcoCompt_X2H21070350_archive.json','MMM_EcoCompt_X2H21070351_archive.json','MMM_EcoCompt_X2H21111120_archive.json',
           'MMM_EcoCompt_X2H21111121_archive.json','MMM_EcoCompt_X2H22043029_archive.json','MMM_EcoCompt_X2H22043030_archive.json',
           'MMM_EcoCompt_X2H22043031_archive.json','MMM_EcoCompt_X2H22043032_archive.json','MMM_EcoCompt_X2H22043033_archive.json',
           'MMM_EcoCompt_X2H22043034_archive.json','MMM_EcoCompt_X2H22043035_archive.json','MMM_EcoCompt_X2H22104765_archive.json',
           'MMM_EcoCompt_X2H22104766_archive.json','MMM_EcoCompt_X2H22104767_archive.json','MMM_EcoCompt_X2H22104768_archive.json',
           'MMM_EcoCompt_X2H22104769_archive.json','MMM_EcoCompt_X2H22104770_archive.json','MMM_EcoCompt_X2H22104771_archive.json',
           'MMM_EcoCompt_X2H22104772_archive.json','MMM_EcoCompt_X2H22104773_archive.json','MMM_EcoCompt_X2H22104774_archive.json',
           'MMM_EcoCompt_X2H22104775_archive.json','MMM_EcoCompt_X2H22104776_archive.json','MMM_EcoCompt_X2H22104777_archive.json',
           'MMM_EcoCompt_XTH19101158_archive.json','MMM_EcoCompt_XTH21015106_archive.json','MMM_EcoCompt_XTH24072390_archive.json',
           'MMM_EcoCompt_XTH24072390_archive_01_06_2024.json','MMM_EcoCompt_X2H19070220_2020.json','MMM_EcoCompt_X2H20042632_2020.json',
           'MMM_EcoCompt_X2H20042633_2020.json','MMM_EcoCompt_X2H20042634_2020.json','MMM_EcoCompt_X2H20042635_2020.json',
           'MMM_EcoCompt_X2H20063161_2020.json','MMM_EcoCompt_X2H20063162_2020.json','MMM_EcoCompt_X2H20063163_2020.json',
           'MMM_EcoCompt_X2H20063164_2020.json','MMM_EcoCompt_XTH19101158_2020.json']


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


def intensity_jour(j,m,a):
    L=[]
    for filename in archives :
        with open(filename,'r') as f:
            json_data = f.read()
            data = json.loads(json_data)
            for i in range(len(data)):
                if int(data[i].get("dateObserved").split('-')[0])==a:
                    if int(data[i].get("dateObserved").split('-')[1])==m:
                        if int(data[i].get("dateObserved").split('-')[2][0]+data[i].get("dateObserved").split('-')[2][1])==j:
                            if data[i].get("intensity")!=None:
                                L.append([data[i].get("intensity"),data[i].get("location").get('coordinates')])
    M=[]
    for i in L:
        c=i[0]
        n=0
        k=0
        for j in L:
            if j[1]==i[1]:
                c+=j[0]
        if len(M)>0:
            while n==0 and k<len(M):
                if i[1]==M[k][1]:
                    n=1 
                k+=1 
        if n==0:
            i[0]=c
            M.append(i)
    return M

def intensity_jour_total(j,m,a):
    N=0
    for filename in archives :
        with open(filename,'r') as f:
            json_data = f.read()
            data = json.loads(json_data)
            for i in range(len(data)):
                if int(data[i].get("dateObserved").split('-')[0])==a:
                    if int(data[i].get("dateObserved").split('-')[1])==m:
                        if int(data[i].get("dateObserved").split('-')[2][0]+data[i].get("dateObserved").split('-')[2][1])==j:
                            if data[i].get("intensity")!=None:
                                N+=data[i].get("intensity")
    return N

def intensity_jour_stats(j,m,a):
    N=[]
    L=[]
    jour=determination_jour(j, m, a)
    for filename in archives :
        with open(filename,'r') as f:
            json_data=f.read()
            data=json.loads(json_data)
            for i in range(len(data)):
                if data[i].get("intensity")!=None:
                    jour_data=int(data[i].get("dateObserved").split('-')[2][0]+data[i].get("dateObserved").split('-')[2][1]),int(data[i].get("dateObserved").split('-')[1]),int(data[i].get("dateObserved").split('-')[0])
                    if determination_jour(jour_data[0],jour_data[1],jour_data[2])==jour:
                        L.append([data[i].get("intensity"),data[i].get("location").get('coordinates')])
    M=[]
    for i in L:
        n=0
        c=i[0]
        p=0
        k=0
        for j in L:
            if j[1]==i[1]:
                c+=j[0]
                n+=1
        if len(M)>0:
            while p==0 and k<len(M):
                if i[1]==M[k][1]:
                    p=1 
                k+=1 
        if p==0:
            i[0]=c/n 
            N.append(n)
            M.append(i)
    return [M,N]



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

#lundi_intensity = intensity_jour_stats(22,4,2024)
#mardi_intensity = intensity_jour_stats(23,4,2024)
#mercredi_intensity = intensity_jour_stats(24,4,2024)
#jeudi_intensity = intensity_jour_stats(25,4,2024)
#vendredi_intensity = intensity_jour_stats(26,4,2024)
#samedi_intensity = intensity_jour_stats(27,4,2024)
#dimanche_intensity = intensity_jour_stats(28,4,2024)
#semaine_pieton = [lundi_intensity,mardi_intensity,mercredi_intensity,jeudi_intensity,vendredi_intensity,samedi_intensity,dimanche_intensity]

#lundi_heure=poids_heure(17, 1, 2022)
#mardi_heure=poids_heure(18, 1, 2022)
#mercredi_heure=poids_heure(19, 1, 2022)
#jeudi_heure=poids_heure(13, 1, 2022)
#vendredi_heure=poids_heure(14, 1, 2022)
#samedi_heure=poids_heure(15, 1, 2022)
#dimanche_heure=poids_heure(16, 1, 2022)
#semaine_heure=[lundi_heure,mardi_heure,mercredi_heure,jeudi_heure,vendredi_heure,samedi_heure,dimanche_heure]
