import streamlit as st
import pandas as pd
import altair as alt
import pickle
from functions import graph


# Page configuration
st.set_page_config(
    page_title="O&M RI",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.title("Archivo Maestro RI")

# Load data
data = pd.read_excel('data/data.xlsx', dtype=str)

alm = pd.read_csv('data/alarmas.csv', header = 4)

# Opciones
dic = {'Informacion': ['Codigo SISMAC', 'Nombre SISMAC', 'Cluster'],
           'Tecnología': ['Tecnología', 'RNC ID', 'ID 3G', 'Sitio 3G', 'ADJNODE ID', 'ID LTE', 'Sitio LTE', 'Celdas 3G - 1P', 'Celdas 3G - 2P', 'Celdas LTE AWS', 'Celdas LTE APT', 'Celdas LTE 1900'],
           'Ubicacion': ['Provincia', 'Cantón', 'Parroquia', 'Cuidad/Localidad', 'Latitud', 'Longitud', 'Dirección', 'Observaciones'],
            'Energia': ['Empresa Eléctrica', 'Contrato / CUE', 'Medidor', 'Generador', 'Estado Baterías'],
            'Infraestructura': ['Dueño Infraestructura', 'Codigo Torrero', 'Nombre Torrero', 'Equipamiento Coubicado', 'Tipo de Sitio', 'Altura Edificación', 'Tipo de Estructura ', 'Altura Estructura ', 'Altura total'],
            'Llaves': ['Fila', 'Columna', 'CENTRAL CNT REPOSO', 'ENTREGADA A SEGURIDAD', 'Ingreso 24/7'],
            'Direccionamiento IP': ['IP Gestion CoTX', 'IP Gestion 3G', 'IP Gestion LTE', 'IP Servicio 3G', 'IP Servicio LTE', 'IP RNC'],
            'Transmision': ['Medio de Transmision', 'Equipo Acceso 3G', 'Puerto Acceso 3G', 'Capa 3 3G', 'Equipo Acceso 4G', 'Puerto Acceso 4G', 'Capa 3 4G'],
            'Correctivos': ['Maleza', 'Correctivo', 'TX']
           }

opciones = list(dic.keys())

# Columnas
col1, col2 = st.columns(2)

with col1:
    site = st.selectbox(
        'Seleccionar Sitio',
        data['Nombre Sitio'].sort_values().tolist(),
        index=None,
        placeholder='Seleccionar Sitio...'
    )

with col2:
    filter_cols = st.multiselect("Seleccionar Categoria", opciones, default=['Informacion', 'Energia'])

if filter_cols:
    for item in filter_cols:
        filtered_df = data[['Nombre Sitio']+dic[item]][data['Nombre Sitio'] == site]
        st.dataframe(filtered_df, hide_index=True, height=90, width=3000)
else:
    st.dataframe(data[data['Nombre Sitio'] == site], hide_index=True, height=90, width=3000)

# Columnas
col3, col4 = st.columns(2)

if site:
    with col3:
        filt = alm[alm['Alarm Source'] == site]
        st.dataframe(filt, hide_index=True)
    with col4:
        df_map = data[data['Nombre Sitio'] == site][['Latitud', 'Longitud']]
        df_map.columns = ['latitude', 'longitude']
        df_map = df_map.astype(float)
        st.map(df_map, size=6, zoom=16)

with open('data/path10072024.pkl', 'rb') as file:
    data_new = pickle.load(file)

selected = data[data['Nombre Sitio'] == site].reset_index()

if not selected.empty and 'Transmision' in filter_cols:
    siteID = selected['RNC ID'][0] + '-' + selected['ADJNODE ID'][0]
    if siteID == 'nan-nan':
        st.write(siteID)
    else:
        graph(data_new[0], siteID)
