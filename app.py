import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

MARQUEUR = "à compléter par l'utilisateur"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
NOM_FEUILLE = "mon_app_questions"  # le nom exact de ta Google Sheet

# --- Connexion à Google Sheets ---
def connecter():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open(NOM_FEUILLE).sheet1

# --- Chargement des questions ---
def charger_questions(sheet):
    lignes = sheet.get_all_records()
    return lignes

# --- Sauvegarde d'une réponse ---
def sauvegarder(sheet, idx, reponse):
    # +2 car : 1 pour l'en-tête, 1 car les indices Google Sheets commencent à 1
    sheet.update_cell(idx + 2, 2, reponse)

# --- App ---
st.title("📝 Compléter le fichier")

sheet = connecter()
data = charger_questions(sheet)

indices_restants = [
    i for i, q in enumerate(data)
    if q["output"] == MARQUEUR
]

if not indices_restants:
    st.success("✅ Toutes les questions ont été répondues !")
    st.table(data)
else:
    total = len(data)
    restant = len(indices_restants)
    st.progress((total - restant) / total)
    st.caption(f"Question {total - restant + 1} / {total}")

    idx = indices_restants[0]
    question = data[idx]["input"]

    st.subheader(f"❓ {question}")

    with st.form(key=f"form_{idx}"):
        reponse = st.text_input("Ta réponse :")
        valider = st.form_submit_button("Valider ➡️")

    if valider:
        if reponse.strip():
            sauvegarder(sheet, idx, reponse.strip())
            st.rerun()
        else:
            st.warning("Merci d'entrer une réponse avant de valider.")