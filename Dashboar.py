import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title = "Cicloconteos",layout="wide")

uploaded_file = st.file_uploader("Cargar un archivo de Excel", type=["xlsx", "xls"])

if uploaded_file:
    # Cargar el archivo de Excel en un DataFrame
    dataset = pd.read_excel(uploaded_file)

    #Arreglar el filtrado
    # Filtrar el dataset
    #st.title("Filtrar el Reporte")
    #filtro = st.text_input("Ingrese un criterio de filtrado:")
    
    #if filtro:
         #Aplicar el filtro
        #resultado_filtrado = dataset[dataset['Itemid'] == filtro]
        #st.write("Resultado del Filtrado:")
        #st.write(resultado_filtrado)

#dataset=pd.read_excel("dataset/Cicloconteos.xlsx")
#dataset=pd.read_excel(uploaded_file)



st.sidebar.header("Filtros: ")

localidad = st.sidebar.multiselect("Por Localidad:",
                                 options = dataset["LOCALIDAD"].unique(),
                                 default = dataset["LOCALIDAD"].unique())

selection_query = dataset.query(
    "LOCALIDAD == @localidad"
    )

Minimo_Fecha = (dataset["Date"].min().date())
Maximo_Fecha = (dataset["Date"].max().date())

st.title('CICLOCONTEOS del '+f'{Minimo_Fecha}'+' al ' +f'{Maximo_Fecha}')

Desfavorables = (dataset[dataset["Trans amount"] < 0]["Trans amount"].sum()*(-1))
Favorables = (dataset[dataset["Trans amount"] > 0]["Trans amount"].sum())

# Formato a 2 decimales
Desfavorables_formateado = "{:.2f}".format(Desfavorables)
Favorables_formateado = "{:.2f}".format(Favorables)


first_column,second_column = st.columns(2)

with first_column:
    st.markdown('<p style="color: red; font-size: 24px;">DESFAVORABLES</p>',unsafe_allow_html=True)
    st.markdown('<p style="color: green; font-size: 24px;">FAVORABLES</p>',unsafe_allow_html=True)
    
with second_column:
    st.subheader(f'{Desfavorables_formateado} $')
    st.subheader(f'{Favorables_formateado} $')

col1, col2, col3 = st.columns(3)

# Mostrar la tabla de LOCALIDADES en la primera columna
with col1:
    st.title("LOCALIDADES")
    dataset_localidades = dataset.groupby('LOCALIDAD')['Trans amount'].sum().reset_index().sort_values(by='Trans amount', ascending=True)
    st.dataframe(dataset_localidades)

# Mostrar la tabla de USUARIO en la segunda columna
with col2:
    st.title("USUARIO")
    dataset_usuario = dataset.groupby('Created by')['Trans amount'].sum().reset_index().sort_values(by='Trans amount', ascending=True)
    st.dataframe(dataset_usuario)

# Mostrar la tabla de No. De Parte en la tercera columna
with col3:
    st.title("No. De Parte")
    dataset_parte = dataset.groupby('Itemid')['Trans amount'].sum().reset_index().sort_values(by='Trans amount', ascending=True)
    st.dataframe(dataset_parte)






