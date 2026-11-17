# Copyright (c) 2026 Ibrahim OLAOYE. Tous droits réservés.
import streamlit as st
from traductions import TEXTES as TRADUCTIONS

st.set_page_config(page_title="Traffic Intelligence System", layout="wide")

# Langue
langue = st.sidebar.selectbox("🌐 Langue / Language", ["Français", "English", "Русский", "العربية", "中文"])
st.session_state.langue = langue

# Menu
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Page d'accueil", "1️⃣ Ancien Modèle (V1)", "🔄 Mise à jour (V2.0)", "🧠 Intelligence Décisionnelle (V2.0)"]
)

# Affichage
if menu == "🏠 Page d'accueil":
    t = TRADUCTIONS[langue]
    st.title(t["titre_app"])
    st.markdown(t["bienvenue"])
    st.markdown(t["description"])
elif menu == "1️⃣ Ancien Modèle (V1)":
    exec(open("app_v1_ancien.py", encoding="utf-8").read())
elif menu == "🔄 Mise à jour (V2.0)":
    exec(open("page_transition.py", encoding="utf-8").read())
elif menu == "🧠 Intelligence Décisionnelle (V2.0)":
    exec(open("app_v2.py", encoding="utf-8").read())
