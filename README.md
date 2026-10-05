# P1 - Predicción de Subscripción a un Producto Bancario
 
Aprendizaje Automático — UC3M 2025-26
 
## Descripción
Modelo predictivo para determinar si un cliente bancario suscribirá un depósito a plazo.  
Variable objetivo: `deposit` (clasificación binaria).
 
## Estructura del repositorio
 
```
P1_AA_2026/
├── notebook_principal.ipynb   # EDA, HPO, selección de modelo
├── notebook_predicciones.ipynb  # Carga modelo final y predicciones competición
├── mystreamlit.py             # App Streamlit para despliegue
├── .gitignore
└── README.md
```
 
## Ficheros de datos
datos de entrenamiento/evaluación
datos de competición (sin target)
 
## Ejecución
```bash
# Notebook principal
jupyter notebook notebook_principal.ipynb
 
# App Streamlit
streamlit run mystreamlit.py
```
