# Copyright (c) 2026 Ibrahim OLAOYE. Tous droits réservés.
import streamlit as st
from traductions import TEXTES as TRADUCTIONS

st.set_page_config(page_title="Traffic Intelligence System", layout="wide")

# Sélecteur de langue
langue = st.sidebar.selectbox("🌐 Langue / Language", ["Français", "English", "Русский", "العربية", "中文"])
st.session_state.langue = langue

# Définition des pages (le menu sera généré automatiquement)
page_accueil = st.Page("app_v1_ancien.py", title="Page d'accueil", icon="🏠", default=True)
page_v1 = st.Page("app_v1_ancien.py", title="Ancien Modèle (V1)", icon="1️⃣")
page_transition = st.Page("page_transition.py", title="Mise à jour (V2.0)", icon="🔄")
page_v2 = st.Page("app_v2.py", title="Intelligence Décisionnelle (V2.0)", icon="🧠")

# Création du menu (il s'affichera dans la sidebar par défaut)
pg = st.navigation([page_accueil, page_v1, page_transition, page_v2])
pg.run()
