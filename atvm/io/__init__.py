import os 
url_courses_24 ="https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_CoursesVelomagg.csv"
url_zip = "https://data.montpellier3m.fr/dataset/courses-des-velos-velomagg-de-montpellier-mediterranee-metropole/resource/edf37027-143f-4c39"

data_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),  
    "..",                                        
    "data_atvm"                                  
)

#path_target= os.path.join(
#    os.path.dirname(os.path.realpath(__file__)),"..","data"
#)

path_csv_target = os.path.join(data_dir, "TAM_MMM_CoursesVelomagg.csv")
path_zip_target = os.path.join(data_dir, "TAM_MMM_CoursesVelomagg_Archives.zip")