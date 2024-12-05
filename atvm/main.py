from atvm.io import *
from atvm.io.Load import LoadData

def main():
    # Télécharger et charger le fichier CSV direct
    print("Téléchargement et chargement du fichier CSV direct...")
    loader_csv = LoadData(url=url_courses_24, target_name=path_csv_target)
    df_csv = loader_csv.save_as_df()

    if df_csv is not None:
        print("Fichier CSV chargé avec succès :")
        print(df_csv.head())

    # Télécharger, extraire et charger un fichier depuis une archive ZIP
    print("\nTéléchargement et extraction de l'archive ZIP...")
    loader_zip = LoadData(url=url_zip, target_name=path_zip_target)
    extracted_dir = path_zip_target.replace(".zip", "_extracted")
    extracted_files = loader_zip.extract_zip(extract_to=extracted_dir)

    if extracted_files:
        print(f"Fichiers extraits : {extracted_files}")

        # Charger un fichier CSV extrait (si disponible)
        csv_files = [f for f in extracted_files if f.endswith(".csv")]
        if csv_files:
            df_zip = loader_zip.save_as_df(file_path=csv_files[0])
            if df_zip is not None:
                print("Données extraites de l'archive :")
                print(df_zip.head())
        else:
            print("Aucun fichier CSV trouvé dans l'archive.")
    else:
        print("Aucun fichier extrait de l'archive.")


if __name__ == "__main__":
    main()