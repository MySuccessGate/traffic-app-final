# Copyright (c) 2026 Ibrahim OLAOYE. Tous droits réservés.
from traductions import TEXTES as TRADUCTIONS
import streamlit as st

langue_actuelle = st.session_state.get('langue', 'Français')
t = TRADUCTIONS[langue_actuelle]

import pandas as pd
import joblib
import xgboost as xgb
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trafic Smart City V1", page_icon="🚦", layout="wide")

model = xgb.XGBRegressor()
# CORRECTION ICI : plus de dossier "models/"
model.load_model("best_traffic_model.json")

@st.cache_data
def charger_donnees():
    # CORRECTION ICI : plus de dossier "data/"
    df = pd.read_csv("Metro_Interstate_Traffic_Volume.csv")
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['hour'] = df['date_time'].dt.hour
    df['dayofweek'] = df['date_time'].dt.dayofweek
    return df

df = charger_donnees()

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Aller à :", [
    "🏠 Accueil", "📊 Exploration", "📈 Visualisations", "🔍 Analyse", 
    "🧠 Modélisation", "🔮 Prédiction", "📉 Performance", 
    "📋 Tableau de bord", "ℹ️ À propos", "📚 Documentation"
])

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style='text-align: center; font-size: 12px; color: #666666; height: auto;'>
        <b>Ibrahim OLAOYE</b><br>
        Ingénieur Statisticien-Économètre<br>
        Data Scientist<br>
        ibolaoye93@gmail.com
    </div>
    """, 
    unsafe_allow_html=True
)

if menu == "🏠 Accueil":
    st.title(t["titre_app"])
    st.write(t["bienvenue"])
    st.write(t["description"])
    
    st.subheader(t["fonctionnalites"])
    st.markdown(f"""
    - {t['f1']}
    - {t['f2']}
    - {t['f3']}
    - {t['f4']}
    """)
    
    st.markdown("---")
    st.write(t["auteur"])

elif menu == "📊 Exploration":
    st.title(t["explo_titre"])
    st.write(f"{t['explo_nb']} : {len(df)}")
    
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce') 
    
    st.write(df.head(10))
    st.subheader(t["explo_stats"])
    st.write(df.describe())

elif menu == "📈 Visualisations":
    st.title(t["visu_titre"])
    st.subheader(t["visu_evol"])
    
    fig1 = px.line(df, x='date_time', y='traffic_volume', title=t["visu_graph1"])
    
    fig1.update_layout(
        xaxis_title=t["visu_axe_x"], 
        yaxis_title=t["visu_axe_y"]
    )
    
    st.plotly_chart(fig1, use_container_width=True)

elif menu == "🔍 Analyse":
    st.title(t["ana_titre"])
    st.subheader(t["ana_matrice"])
    
    df['temp'] = pd.to_numeric(df['temp'], errors='coerce')
    df['traffic_volume'] = pd.to_numeric(df['traffic_volume'], errors='coerce')
    
    cols_num = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'traffic_volume', 'hour', 'dayofweek']
    
    for col in cols_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    corr = df[cols_num].corr()
    
    fig3, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig3)
    
    st.subheader(t["ana_trafic_temp"])
    
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    ax5.scatter(df['temp'], df['traffic_volume'], alpha=0.5, s=10, color='tab:blue')
    ax5.set_title(t["ana_graph_temp"])
    ax5.set_xlabel("Température")
    ax5.set_ylabel("Volume de traffic")
    st.pyplot(fig5)

    
elif menu == "🧠 Modélisation":
    st.title(t["mod_titre"])
    st.write(t["mod_desc"])
    st.code("hour, dayofweek, temp, rain_1h, snow_1h, clouds_all")
    st.subheader(t["mod_pourquoi"])
    st.markdown("- Gère les non-linéarités\n- Robuste aux aberrants\n- Bonne généralisation")
    
    st.subheader(t["mod_importance"])
    features = ['hour', 'dayofweek', 'temp', 'rain_1h', 'snow_1h', 'clouds_all']
    importances = [0.70, 0.15, 0.05, 0.03, 0.02, 0.05]
    fig5, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=importances, y=features, ax=ax, color='purple')
    st.pyplot(fig5)

elif menu == "🔮 Prédiction":
    st.title(t["pred_titre"])
    col1, col2 = st.columns(2)
    with col1:
        hour = st.slider(t["pred_heure"], 0, 23, 12)
        day = st.selectbox(t["pred_jour"], t["jours"])
        temp = st.number_input(t["pred_temp"], -20.0, 50.0, 20.0)
    with col2:
        rain = st.number_input(t["pred_pluie"], 0.0, 20.0, 0.0)
        snow = st.number_input(t["pred_neige"], 0.0, 10.0, 0.0)
        clouds = st.number_input(t["pred_nuages"], 0, 100, 50)
        
    dayofweek = t["jours"].index(day)
    
    if st.button(t["pred_btn"]):
        input_data = pd.DataFrame([[hour, dayofweek, temp, rain, snow, clouds]], 
                                  columns=['hour', 'dayofweek', 'temp', 'rain_1h', 'snow_1h', 'clouds_all'])
        prediction = model.predict(input_data)[0]
        st.success(f"{t['pred_resultat']} : **{int(prediction)}** véhicules / heure")

elif menu == "📋 Tableau de bord":
    st.title(t["dash_titre"])
    st.write(t["dash_desc"])
    
    jour_filtre = st.selectbox(t["pred_jour"], t["jours"])
    
    day_index = t["jours"].index(jour_filtre)
    df_filtre = df[df['dayofweek'] == day_index]
    
    df_moyenne = df_filtre.groupby('hour')['traffic_volume'].mean().reset_index()
    
    fig_dash = px.line(df_moyenne, x='hour', y='traffic_volume', 
                       title=t["dash_graph_titre"],
                       labels={'hour': t["pred_heure"], 'traffic_volume': t["explo_graph"]},
                       markers=True)
    
    st.plotly_chart(fig_dash, use_container_width=True)

elif menu == "📉 Performance":
    st.title(t["perf_titre"])
    st.write(t["perf_desc"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric(t["perf_r2"], "0.946", delta="Excellent")
    col2.metric(t["perf_rmse"], "450 véhicules/h", delta="-", delta_color="off")
    col3.metric(t["perf_mae"], "320 véhicules/h", delta="-", delta_color="off")
    
    st.markdown("---")
    
    metrics = ['R²', 'RMSE (÷1000)', 'MAE (÷1000)']
    values = [0.946, 0.450, 0.320]
    colors = ['#2ecc71', '#e74c3c', '#f39c12']
    
    fig_perf = px.bar(x=metrics, y=values, 
                      title=t["perf_graph_titre"],
                      color=metrics,
                      color_discrete_sequence=colors,
                      text=values)
    
    fig_perf.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig_perf.update_layout(yaxis_range=[0, 1.1], showlegend=False)
    
    st.plotly_chart(fig_perf, use_container_width=True)
    
elif menu == "ℹ️ À propos":
    st.title(t["apropos_titre"])
    st.write(t["apropos_desc"])
    st.markdown(f"- {t['apropos_data']}")

elif menu == "📚 Documentation":
    st.title(t["doc_titre"])
    st.write(t["doc_desc"])
    st.subheader(t["doc_limit_titre"])
    st.write(f"{t['doc_limit_1']}\n{t['doc_limit_2']}")
