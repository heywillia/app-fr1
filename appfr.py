
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import uuid

# --- AUTENTICACIÓN GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# --- ACCEDER A LA HOJA ---
spreadsheet = client.open("APFR1_BDD")
jugadores_sheet = spreadsheet.worksheet("Jugadores")
valoraciones_sheet = spreadsheet.worksheet("valoraciones")

# --- CARGAR DATOS DE JUGADORES ---
df_jugadores = pd.DataFrame(jugadores_sheet.get_all_records())
jugadores_dict = dict(zip(df_jugadores["Nombre"], df_jugadores["ID"]))

# --- UI STREAMLIT ---
st.title("⚽ Valorá a tus compañeros")

evaluador_nombre = st.selectbox("¿Quién sos vos?", options=list(jugadores_dict.keys()))
evaluador_id = jugadores_dict[evaluador_nombre]

st.write("### Valorá a tus compañeros (1 a 10):")

valoraciones = []
for nombre, evaluado_id in jugadores_dict.items():
    if nombre == evaluador_nombre:
        continue  # no se autoevalúa
    st.subheader(f"{nombre}")
    nota = st.slider(f"Puntaje para {nombre}", 1, 10, 5, key=nombre)
    comentario = st.text_input(f"Comentario para {nombre}", "", key=f"c_{nombre}")
    valoraciones.append({
        "ID": str(uuid.uuid4()),
        "Evaluador_ID": evaluador_id,
        "Evaluado_ID": evaluado_id,
        "Valoración": nota,
        "Comentarios": comentario,
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if st.button("Enviar valoraciones"):
    for v in valoraciones:
        valoraciones_sheet.append_row([
            v["ID"],
            v["Evaluador_ID"],
            v["Evaluado_ID"],
            v["Valoración"],
            v["Comentarios"],
            v["Fecha"]
        ])
    st.success("✅ ¡Valoraciones guardadas con éxito!")
