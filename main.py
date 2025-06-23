import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from index import init_dataframes, next_id, save_data, get_albumes_by_banda

# Configuración de la aplicación
st.set_page_config(page_title="Analizador de Discografías", layout="wide")

# Interfaz de usuario
st.title("🎵 Analizador de Discografías")

# Cargar datos
bandas_df, albumes_df, canciones_df = init_dataframes()

# Menú de navegación
menu = st.sidebar.selectbox("Menú", ["Inicio", "Agregar Datos", "Analizar Datos", "Exportar/Importar"])

if menu == "Inicio":
    st.header("Bienvenido al Analizador de Discografías")
    st.write("""
    Esta aplicación permite:
    - Almacenar información en archivos CSV
    - Analizar datos musicales
    - Exportar/importar a Excel
    """)

elif menu == "Agregar Datos":
    st.header("Agregar Nueva Información")
    
    opcion = st.radio("¿Qué desea agregar?", ("Banda", "Álbum", "Canción"))
    
    if opcion == "Banda":
        with st.form("form_banda"):
            nombre = st.text_input("Nombre de la banda")
            genero = st.text_input("Género musical")
            año = st.number_input("Año de formación", min_value=1900, max_value=datetime.now().year)
            pais = st.text_input("País de origen")
            
            if st.form_submit_button("Guardar Banda"):
                if nombre in bandas_df["nombre"].values:
                    st.error("Esta banda ya existe")
                else:
                    nueva_banda = pd.DataFrame([{
                        "id": next_id(bandas_df),
                        "nombre": nombre,
                        "genero": genero,
                        "año_formacion": año,
                        "pais": pais
                    }])
                    bandas_df = pd.concat([bandas_df, nueva_banda], ignore_index=True)
                    save_data(bandas_df, albumes_df, canciones_df)
                    st.success("Banda agregada!")

    elif opcion == "Álbum":
        if bandas_df.empty:
            st.warning("Primero debes agregar una banda")
        else:
            with st.form("form_album"):
                banda_seleccionada = st.selectbox("Banda", bandas_df["nombre"])
                titulo = st.text_input("Título del álbum")
                año = st.number_input("Año de lanzamiento", min_value=1900, max_value=datetime.now().year)
                duracion = st.number_input("Duración total (minutos)", min_value=0.1, step=0.1)
                categoria = st.selectbox("Categoría", ["Sencillo/EP", "Album", "Mini Album", "Compilation Album"])
                
                if st.form_submit_button("Guardar Álbum"):
                    banda_id = bandas_df[bandas_df["nombre"] == banda_seleccionada]["id"].values[0]
                    if categoria == "Sencillo/EP":
                        categoria_id=1
                    elif categoria == "Album":
                        categoria_id=2
                    elif categoria == "Mini Album":
                        categoria_id=3
                    elif categoria == "Compilation Album":
                        categoria_id=4
                    nuevo_album = pd.DataFrame([{
                        "id": next_id(albumes_df),
                        "banda_id": banda_id,
                        "titulo": titulo,
                        "año": año,
                        "duracion_total": duracion,
                        "categoria": categoria_id
                    }])
                    albumes_df = pd.concat([albumes_df, nuevo_album], ignore_index=True)
                    save_data(bandas_df, albumes_df, canciones_df)
                    st.success("Álbum agregado!")

    elif opcion == "Canción":
        if bandas_df.empty:
            st.warning("Primero debes agregar una banda")
        else:
            banda_seleccionada = st.selectbox("Banda", bandas_df["nombre"])
            banda_id = bandas_df[bandas_df["nombre"] == banda_seleccionada]["id"].values[0]
            albumes_banda = get_albumes_by_banda(albumes_df, banda_id)
            
            if albumes_banda.empty:
                st.warning("Esta banda no tiene álbumes registrados")
            else:
                with st.form("form_cancion"):
                    album_seleccionado = st.selectbox("Álbum", albumes_banda["titulo"])
                    titulo = st.text_input("Título de la canción")
                    duracion = st.number_input("Duración (segundos)", min_value=1, step=1)
                    track_number = st.number_input("Número de pista", min_value=1, step=1)
                    
                    if st.form_submit_button("Guardar Canción"):
                        album_id = albumes_banda[albumes_banda["titulo"] == album_seleccionado]["id"].values[0]
                        nueva_cancion = pd.DataFrame([{
                            "id": next_id(canciones_df),
                            "album_id": album_id,
                            "titulo": titulo,
                            "duracion": duracion,
                            "track_number": track_number
                        }])
                        canciones_df = pd.concat([canciones_df, nueva_cancion], ignore_index=True)
                        save_data(bandas_df, albumes_df, canciones_df)
                        st.success("Canción agregada!")

elif menu == "Analizar Datos":
    st.header("Análisis de Discografías")
    
    if bandas_df.empty:
        st.warning("No hay bandas registradas para analizar")
    else:
        bandas_seleccionadas = st.multiselect("Selecciona bandas para analizar", bandas_df["nombre"])
        
        if bandas_seleccionadas:
            bandas_filtradas = bandas_df[bandas_df["nombre"].isin(bandas_seleccionadas)]
            albumes_filtrados = albumes_df[albumes_df["banda_id"].isin(bandas_filtradas["id"])]
            total_canciones = canciones_df[canciones_df["album_id"].isin(albumes_filtrados["id"])]
            albumes_filtrados_anno = albumes_filtrados.groupby(["banda_id", "año"], as_index=False)["titulo"].count()
            
            # Estadísticas básicas
            st.subheader("Estadísticas Básicas")
            col1, col2, col3 = st.columns(3)
            col1.metric("Número de Bandas", len(bandas_seleccionadas))
            col2.metric("Total de Álbumes", len(albumes_filtrados))
            col3.metric("Total de Canciones", len(total_canciones))
            
            # Gráficos
            st.subheader("Álbumes por Año")
            if not albumes_filtrados.empty:
                fig = px.bar(albumes_filtrados_anno, x="año", y="titulo",
                            color="banda_id", hover_data=["titulo"],
                            labels={'año': 'Año de lanzamiento', 'titulo': 'Álbumes', 'banda_id': 'Banda'},
                            title="Lanzamiento de álbumes por año")
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Duración de Álbumes")
                fig2 = px.box(albumes_filtrados, x="banda_id", y="duracion_total",
                              labels={'banda_id': 'Banda', 'duracion_total': 'Duración (minutos)'},
                              title="Distribución de duración de álbumes")
                st.plotly_chart(fig2, use_container_width=True)
                
                st.subheader("Distribución de Géneros")
                fig3 = px.pie(bandas_filtradas, names="genero", title="Géneros musicales")
                st.plotly_chart(fig3, use_container_width=True)

elif menu == "Exportar/Importar":
    st.header("Exportar/Importar Datos")
    
    tab1, tab2 = st.tabs(["Exportar", "Importar"])
    
    with tab1:
        st.subheader("Exportar a Excel")
        if st.button("Generar Archivo Excel"):
            with pd.ExcelWriter("discografia.xlsx") as writer:
                bandas_df.to_excel(writer, sheet_name="Bandas", index=False)
                albumes_df.to_excel(writer, sheet_name="Álbumes", index=False)
                canciones_df.to_excel(writer, sheet_name="Canciones", index=False)
            
            with open("discografia.xlsx", "rb") as f:
                st.download_button(
                    label="Descargar Excel",
                    data=f,
                    file_name="discografia.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with tab2:
        st.subheader("Importar desde Excel")
        uploaded_file = st.file_uploader("Sube un archivo Excel", type=["xlsx"])
        
        if uploaded_file:
            try:
                new_bandas = pd.read_excel(uploaded_file, sheet_name="Bandas")
                new_albumes = pd.read_excel(uploaded_file, sheet_name="Álbumes")
                new_canciones = pd.read_excel(uploaded_file, sheet_name="Canciones")
                
                st.write("Vista previa de los datos:")
                st.dataframe(new_bandas)
                
                if st.button("Confirmar Importación"):
                    bandas_df = new_bandas
                    albumes_df = new_albumes
                    canciones_df = new_canciones
                    save_data(bandas_df, albumes_df, canciones_df)
                    st.success("Datos importados correctamente!")
            except Exception as e:
                st.error(f"Error al importar: {str(e)}")

# Resumen de datos
st.sidebar.subheader("Resumen de Datos")
st.sidebar.write(f"Bandas: {len(bandas_df)}")
st.sidebar.write(f"Álbumes: {len(albumes_df)}")
st.sidebar.write(f"Canciones: {len(canciones_df)}")
