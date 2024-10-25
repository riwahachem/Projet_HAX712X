
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
