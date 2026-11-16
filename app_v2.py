# Copyright (c) 2026 Ibrahim OLAOYE. Tous droits réservés.
import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import shap
from sklearn.model_selection import train_test_split
from traductions import TEXTES

langue_actuelle = st.session_state.get('langue', 'Français')
t = TEXTES[langue_actuelle]

st.title(t["titre_v2"])
st.markdown(f"### {t['plateforme_decision']}")

@st.cache_resource
def charger_et_entrainer():
    df = pd.read_csv("data/Metro_Interstate_Traffic_Volume.csv")
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['hour'] = df['date_time'].dt.hour
    df['dayofweek'] = df['date_time'].dt.dayofweek
    df['is_holiday'] = df['holiday'].notna().astype(int)
    
    features = ['hour', 'dayofweek', 'temp', 'rain_1h', 'snow_1h', 'clouds_all', 'is_holiday']
    X = df[features]
    y = df['traffic_volume']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = xgb.XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
    model.fit(X_train, y_train)
    
    model_low = xgb.XGBRegressor(n_estimators=100, objective='reg:quantileerror', quantile_alpha=0.025, random_state=42, verbosity=0)
    model_low.fit(X_train, y_train)
    
    model_high = xgb.XGBRegressor(n_estimators=100, objective='reg:quantileerror', quantile_alpha=0.975, random_state=42, verbosity=0)
    model_high.fit(X_train, y_train)
    
    return model, model_low, model_high, features

with st.spinner("Chargement du modèle et des données..."):
    model, model_low, model_high, features = charger_et_entrainer()

st.sidebar.header(t["parametres_sim"])
hour = st.sidebar.slider(t["pred_heure"], 0, 23, 12)
day = st.sidebar.selectbox(t["pred_jour"], t["jours"])
temp = st.sidebar.number_input(t["pred_temp"], -20.0, 50.0, 20.0)
rain = st.sidebar.number_input(t["pred_pluie"], 0.0, 20.0, 0.0)
snow = st.sidebar.number_input(t["pred_neige"], 0.0, 10.0, 0.0)
clouds = st.sidebar.number_input(t["pred_nuages"], 0, 100, 50)
is_holiday = st.sidebar.checkbox(t["pred_ferie"], value=False)

dayofweek = t["jours"].index(day)
input_data = pd.DataFrame([[hour, dayofweek, temp, rain, snow, clouds, int(is_holiday)]], columns=features)

col1, col2 = st.columns(2)

with col1:
    st.markdown(t["option_a"])
    if st.button(t["btn_lancer"]):
        pred = model.predict(input_data)[0]
        low = model_low.predict(input_data)[0]
        high = model_high.predict(input_data)[0]
        st.metric(label=t["pred_mediane"], value=f"{int(pred)} véhicules/h")
        st.info(f"**{t['intervalle']}**\n\n[{int(low)} ; {int(high)}]\n\n*{t['marge']} : ±{int(high - low)} véhicules*")

with col2:
    st.subheader(t["option_b"])
    if st.button(t["btn_expliquer"]):
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_data)
        fig, ax = plt.subplots(figsize=(10, 4))
        shap.bar_plot(shap_values[0], feature_names=features, max_display=10, show=False)
        st.pyplot(fig)

st.markdown("---")
st.subheader(t["option_c"])
col_sim1, col_sim2 = st.columns(2)
with col_sim1:
    st.markdown(t["scenario_actuel"])
    st.write(f"- {t['pred_heure']} : {hour}h")
    st.write(f"- {t['pred_jour']} : {day}")
    st.write(f"- {t['pred_temp']} : {temp}°C")
    st.write(f"- {t['pred_pluie']} : {rain} mm/h")
with col_sim2:
    st.markdown(t["scenario_alt"])
    hour_alt = st.slider(t["heure_alt"], 0, 23, 17, key="hour_alt")
    temp_alt = st.number_input(t["temp_alt"], -20.0, 50.0, 10.0, key="temp_alt")
    rain_alt = st.number_input(t["pluie_alt"], 0.0, 20.0, 5.0, key="rain_alt")

if st.button(t["comparer"]):
    input_actuel = pd.DataFrame([[hour, dayofweek, temp, rain, snow, clouds, int(is_holiday)]], columns=features)
    pred_actuel = model.predict(input_actuel)[0]
    input_alt = pd.DataFrame([[hour_alt, dayofweek, temp_alt, rain_alt, snow, clouds, int(is_holiday)]], columns=features)
    pred_alt = model.predict(input_alt)[0]
    
    diff = pred_alt - pred_actuel
    pct = (diff / pred_actuel) * 100
    
    st.markdown(f"### {t['resultats_comp']}")
    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric(t["scenario_actuel"], f"{int(pred_actuel)} véhicules/h")
    col_res2.metric(t["scenario_alt"], f"{int(pred_alt)} véhicules/h", delta=f"{int(diff)}")
    col_res3.metric(t["variation"], f"{pct:.1f}%")

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; font-family: Arial, sans-serif; font-size: 14px;'>
        <span style='color: #0066CC; font-weight: bold; font-size: 16px;'>Ibrahim OLAOYE</span><br>
        <span style='color: #333333;'>Ingénieur Statisticien-Économètre | Data Scientist</span><br>
        <span style='color: #666666; font-size: 13px;'>ibolaoye93@gmail.com | +229 01 96 95 83 44</span>
    </div>
    """, 
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
