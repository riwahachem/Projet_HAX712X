import numpy as np

filename = 'TAM_MMM_CoursesVelomagg_2022.csv'

def prediction_jour(j,m,a):
    M,l=semaine_trajet[(determination_jour(j,m,a)%7)-1][0],semaine_trajet[(determination_jour(j,m,a)%7)-1][1]
    for i in range(len(M)):
        M[i][2]=[M[i][2]-(1.96*(np.sqrt((M[i][2]*(1-M[i][2]))/l))),M[i][2]+(1.96*(np.sqrt((M[i][2]*(1-M[i][2]))/l)))]
    return M 
