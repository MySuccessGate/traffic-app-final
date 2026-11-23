import streamlit as st
from traductions import TEXTES

st.set_page_config(page_title="Traffic Intelligence System", page_icon="🚦", layout="wide")

# --- Sélecteur de langue ---
if 'langue' not in st.session_state:
    st.session_state.langue = "Français"

langue_choisie = st.sidebar.selectbox(
    "🌐 Langue / Language",
    list(TEXTES.keys()),
    index=list(TEXTES.keys()).index(st.session_state.langue)
)
st.session_state.langue = langue_choisie

# --- Définition des pages (une seule page par défaut) ---
page_accueil = st.Page("app_v1_ancien.py", title="Page d'accueil", icon="🏠", default=True)
page_v1 = st.Page("app_v1_ancien.py", title="Ancien Modèle (V1)", icon="1️⃣")
page_transition = st.Page("page_transition.py", title="Mise à jour (V2.0)", icon="🔄")
page_v2 = st.Page("app_v2.py", title="Intelligence Décisionnelle (V2.0)", icon="🧠")

# --- Navigation ---
pg = st.navigation([page_accueil, page_v1, page_transition, page_v2])
pg.run()
