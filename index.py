import pandas as pd
import os

# Archivos de datos
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
BANDAS_CSV = os.path.join(DATA_DIR, "bandas.csv")
ALBUMES_CSV = os.path.join(DATA_DIR, "albumes.csv")
CANCIONES_CSV = os.path.join(DATA_DIR, "canciones.csv")

# Inicializar DataFrames
def init_dataframes():
    if os.path.exists(BANDAS_CSV):
        bandas_df = pd.read_csv(BANDAS_CSV)
    else:
        bandas_df = pd.DataFrame(columns=["id", "nombre", "genero", "año_formacion", "pais"])
    
    if os.path.exists(ALBUMES_CSV):
        albumes_df = pd.read_csv(ALBUMES_CSV)
    else:
        albumes_df = pd.DataFrame(columns=["id", "banda_id", "titulo", "año", "duracion_total", "categoria"])
    
    if os.path.exists(CANCIONES_CSV):
        canciones_df = pd.read_csv(CANCIONES_CSV)
    else:
        canciones_df = pd.DataFrame(columns=["id", "album_id", "titulo", "duracion", "track_number"])
    
    return bandas_df, albumes_df, canciones_df

# Guardar DataFrames
def save_data(bandas_df, albumes_df, canciones_df):
    bandas_df.to_csv(BANDAS_CSV, index=False)
    albumes_df.to_csv(ALBUMES_CSV, index=False)
    canciones_df.to_csv(CANCIONES_CSV, index=False)

# Funciones de ayuda
def next_id(df):
    return df["id"].max() + 1 if not df.empty else 1

def get_albumes_by_banda(albumes_df, banda_id):
    return albumes_df[albumes_df["banda_id"] == banda_id]

def get_canciones_by_album(canciones_df, album_id):
    return canciones_df[canciones_df["album_id"] == album_id]
