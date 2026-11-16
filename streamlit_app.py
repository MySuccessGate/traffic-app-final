# Copyright (c) 2026 Ibrahim OLAOYE. Tous droits réservés.
import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Traffic Intelligence System", page_icon="🚦", layout="wide")
# Ajout du sélecteur de langue
if 'langue' not in st.session_state:
    st.session_state.langue = "Français"

langue_choisie = st.sidebar.selectbox(
    "🌐 Langue / Language",
    ["Français", "English"],
    index=0
)
st.session_state.langue = langue_choisie
# Gestion de la transition via les paramètres de l'URL
if "page" not in st.query_params:
    st.query_params["page"] = "v1"


# Page 1 : Ancien modèle (app_v1_ancien.py)
page_v1 = st.Page("app_v1_ancien.py", title="Ancien Modèle (V1)", icon="🚦")

# Page 2 : Transition
page_transition = st.Page("page_transition.py", title="Mise à jour (V2.0)", icon="🔄")
# Page 0 : Accueil
def page_accueil():
    st.title("🚦 Bienvenue sur Traffic Intelligence System")
    st.markdown("""
    Cette application vous permet de prédire le volume de trafic et d'analyser les données.
    Utilisez le menu de gauche pour naviguer entre les différentes versions et fonctionnalités.
    """)
    # Vous pouvez ajouter ici vos boutons ou liens vers les autres pages si vous le souhaitez
# Page 3 : Nouveau modèle (app_v2.py)
page_v2 = st.Page("app_v2.py", title="Intelligence Décisionnelle (V2.0)", icon="🧠")
pg = st.navigation({
    "Accueil": [st.Page(page_accueil, title="Page d'accueil", icon="🏠")],
    "Version 1.0": [page_v1],
    "Transition": [page_transition],
    "Version 2.0": [page_v2]

pg = st.navigation({
    "Version 1.0": [page_v1],
    "Transition": [page_transition],
    "Version 2.0": [page_v2]
})

# On lance la page sélectionnée
pg.run()
