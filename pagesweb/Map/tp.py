#%%
from shiny import App, ui, render

jours = {
    "Lundi": "Map/carte_prediction_semaine/carte_prediction_lundi.html",
    "Mardi": "Map/carte_prediction_semaine/carte_prediction_mardi.html",
    "Mercredi": "Map/carte_prediction_semaine/carte_prediction_mercredi.html",
    "Jeudi": "Map/carte_prediction_semaine/carte_prediction_jeudi.html",
    "Vendredi": "Map/carte_prediction_semaine/carte_prediction_vendredi.html",
    "Samedi": "Map/carte_prediction_semaine/carte_prediction_samedi.html",
    "Dimanche": "Map/carte_prediction_semaine/carte_prediction_dimanche.html"
}

app_ui = ui.page_fluid(
    ui.h2("Prédiction du trafic VéloMagg"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("jour", "Jour :", choices=list(jours.keys()), selected="Lundi")
        ),
        ui.output_ui("afficher_carte")
    )
)

# Logique du serveur
def server(input, output, session):
    @output
    @render.ui
    def afficher_carte():
        # Récupérer le jour sélectionné
        jour_selectionne = input.jour()
        fichier_carte = jours.get(jour_selectionne, "")
        
        # Vérifier si le fichier est défini, sinon afficher un message
        if not fichier_carte:
            return ui.div("Aucune carte disponible pour le jour sélectionné.")
        
        # Retourner l'iframe avec la carte HTML
        return ui.div(
            ui.h4(f"Carte de prédiction pour {jour_selectionne}"),
            ui.HTML(f'<iframe src="{fichier_carte}" width="100%" height="600px" frameborder="0"></iframe>')
        )

# Créer l'application Shiny
app = App(app_ui, server)
# %%
