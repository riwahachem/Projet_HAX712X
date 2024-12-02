import os

# Le chemin vers ton dossier contenant les fichiers Python
folder_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data'


# Liste des fichiers Python (.py) dans le dossier
files = [f for f in os.listdir(folder_path) if f.endswith('.py')]

# Ouvrir le fichier index.rst pour ajouter la documentation des modules
with open('index.rst', 'a') as f:
    f.write('\nModules\n========\n')  # Titre de la section Modules
    f.write('``modules`` lists all the Python files in the `data` folder.\n\n')
    
    # Pour chaque fichier Python dans le dossier, ajouter un bloc automodule
    for file in files:
        module_name = file[:-3]  # Retirer l'extension .py
        f.write(f'.. automodule:: {module_name}\n   :members:\n\n')
