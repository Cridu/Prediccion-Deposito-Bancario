import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ── Configuración de la página ────────────────────────────────────────────────
st.set_page_config(
    page_title="Predicción de Depósito Bancario",
    layout="centered"
)

st.title("Predicción de Subscripción a Depósito Bancario")
st.markdown(
    "Introduce los datos del cliente para predecir si suscribirá un depósito a plazo."
)
st.divider()

# ── Cargar modelo ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("modelo_final.joblib")

model = load_model()

# ── Formulario de entrada ─────────────────────────────────────────────────────
st.subheader("Datos del cliente")

col1, col2 = st.columns(2)

with col1:
    age      = st.number_input("Edad",                    min_value=18, max_value=95, value=40)
    job      = st.selectbox("Tipo de trabajo", [
        'admin.', 'blue-collar', 'entrepreneur', 'housemaid',
        'management', 'retired', 'self-employed', 'services',
        'student', 'technician', 'unemployed', 'unknown'
    ])
    marital  = st.selectbox("Estado civil",        ['married', 'single', 'divorced'])
    education= st.selectbox("Nivel de educación",  ['secondary', 'tertiary', 'primary', 'unknown'])
    default  = st.selectbox("¿Crédito impagado?",  ['no', 'yes'])
    balance  = st.number_input("Balance anual medio (€)", value=1000)
    housing  = st.selectbox("¿Tiene hipoteca?",    ['yes', 'no'])
    loan     = st.selectbox("¿Tiene préstamo?",    ['no', 'yes'])

with col2:
    contact  = st.selectbox("Tipo de contacto",    ['cellular', 'telephone', 'unknown'])
    day      = st.number_input("Día del último contacto", min_value=1, max_value=31, value=15)
    month    = st.selectbox("Mes del último contacto", [
        'jan', 'feb', 'mar', 'apr', 'may', 'jun',
        'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
    ])
    duration = st.number_input("Duración último contacto (segundos)", min_value=0, value=200)
    campaign = st.number_input("Nº contactos esta campaña", min_value=1, value=2)
    pdays    = st.number_input(
        "Días desde último contacto campaña anterior (-1 = sin contacto)",
        min_value=-1, value=-1
    )
    previous = st.number_input("Nº contactos campañas anteriores", min_value=0, value=0)
    poutcome = st.selectbox("Resultado campaña anterior", ['unknown', 'failure', 'other', 'success'])

st.divider()

# ── Predicción ────────────────────────────────────────────────────────────────
if st.button("Predecir", use_container_width=True, type="primary"):

    # Construir el dataframe con el mismo preprocesamiento que en el notebook
    input_data = pd.DataFrame([{
        'age'      : age,
        'job'      : job,
        'marital'  : marital,
        'education': education,
        'default'  : default,
        'balance'  : balance,
        'housing'  : housing,
        'loan'     : loan,
        'contact'  : contact,
        'day'      : day,
        'month'    : month,
        'duration' : duration,
        'campaign' : campaign,
        'pdays'    : pdays,
        'previous' : previous,
        'poutcome' : poutcome,
    }])

    # Preprocesamiento de pdays (igual que en el notebook)
    input_data['contacted_before'] = (input_data['pdays'] != -1).astype(int)
    input_data['pdays_clean']      = input_data['pdays'].clip(lower=0)
    input_data = input_data.drop(columns=['pdays'])

    # Predicción
    pred     = model.predict(input_data)[0]
    # 0 = 'no', 1 = 'yes'
    etiqueta = "✅ SÍ suscribirá el depósito" if pred == 1 else "❌ NO suscribirá el depósito"
    color    = "green" if pred == 1 else "red"

    st.markdown(f"### Resultado:")
    st.markdown(
        f"<h2 style='color:{color}; text-align:center'>{etiqueta}</h2>",
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown("**Datos introducidos:**")
    st.dataframe(input_data, use_container_width=True)
