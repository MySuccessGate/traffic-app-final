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

# --- Menu de navigation classique (très stable) ---
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Page d'accueil", "1️⃣ Ancien Modèle (V1)", "🔄 Mise à jour (V2.0)", "🧠 Intelligence Décisionnelle (V2.0)"]
)

# --- Affichage des pages ---
if menu == "🏠 Page d'accueil":
    t = TEXTES[langue_choisie]
    st.title(t["titre_app"])
    st.markdown(t["bienvenue"])
    st.markdown(t["description"])

elif menu == "1️⃣ Ancien Modèle (V1)":
    exec(open("app_v1_ancien.py", encoding="utf-8").read())

elif menu == "🔄 Mise à jour (V2.0)":
    exec(open("page_transition.py", encoding="utf-8").read())

elif menu == "🧠 Intelligence Décisionnelle (V2.0)":
    exec(open("app_v2.py", encoding="utf-8").read())
