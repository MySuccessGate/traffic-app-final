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

# Récupération des traductions
langue_actuelle = st.session_state.get('langue', 'Français')
t = TRADUCTIONS[langue_actuelle]

# Définition du menu de navigation
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Page d'accueil", "1️⃣ Ancien Modèle (V1)", "🔄 Mise à jour (V2.0)", "🧠 Intelligence Décisionnelle (V2.0)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Ibrahim OLAOYE** - Ingénieur Statisticien-Économètre | Data Scientist")

# Affichage de la page sélectionnée
if menu == "🏠 Page d'accueil":
    st.title(t["titre_app"])
    st.markdown(t["bienvenue"])
    st.markdown(t["description"])

elif menu == "1️⃣ Ancien Modèle (V1)":
    # On exécute le fichier app_v1_ancien.py
    exec(open("app_v1_ancien.py", encoding="utf-8").read())

elif menu == "🔄 Mise à jour (V2.0)":
    exec(open("page_transition.py", encoding="utf-8").read())

elif menu == "🧠 Intelligence Décisionnelle (V2.0)":
    exec(open("app_v2.py", encoding="utf-8").read())
