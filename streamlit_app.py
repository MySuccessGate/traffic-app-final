# Copyright (c) 2026 Ibrahim OLAOYE. Tous droits réservés.
import streamlit as st
from traductions import TEXTES as TRADUCTIONS

# Configuration de la page
st.set_page_config(page_title="Traffic Intelligence System", page_icon="🚦", layout="wide")

# Ajout du sélecteur de langue
if 'langue' not in st.session_state:
    st.session_state.langue = "Français"

langue_choisie = st.sidebar.selectbox(
    "🌐 Langue / Language",
    ["Français", "English", "Русский", "العربية", "中文"],
    index=0
)
st.session_state.langue = langue_choisie

# Gestion de la transition via les paramètres de l'URL
if "page" not in st.query_params:
    st.query_params["page"] = "v1"

# Définition de la page d'accueil (sans le menu de navigation)
def page_accueil():
    langue_actuelle = st.session_state.get('langue', 'Français')
    t = TRADUCTIONS[langue_actuelle]
    st.title(t["titre_app"])
    st.markdown(t["bienvenue"])
    st.markdown(t["description"])

# Définition des pages
page_v1 = st.Page("app_v1_ancien.py", title="Ancien Modèle (V1)", icon="1️⃣")
page_transition = st.Page("page_transition.py", title="Mise à jour (V2.0)", icon="🔄")
page_v2 = st.Page("app_v2.py", title="Intelligence Décisionnelle (V2.0)", icon="🧠")

# Menu de navigation (version liste simple)
pg = st.navigation([
    st.Page(page_accueil, title="Page d'accueil", icon="🏠"),
    page_v1,
    page_transition,
    page_v2
])

# Lancement de la page sélectionnée
pg.run()

# Lancement de la page sélectionnée
pg.run()

