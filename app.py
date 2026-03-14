import streamlit as st
import json

FICHIER = "questions.json"
MARQUEUR = "répondre ici"

def charger_questions():
    with open(FICHIER, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder(data):
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.title("Répondez aux questions")

data = charger_questions()

indices_restants = [
    i for i, q in enumerate(data)
    if q["output"] == MARQUEUR
]

if not indices_restants:
    st.success("Vous avez répondu à toutes les questions :)) !")
    st.json(data)
else:
    total = len(data)
    restant = len(indices_restants)
    st.progress((total - restant) / total)
    st.caption(f"Question {total - restant + 1} / {total}")

    idx = indices_restants[0]
    question = data[idx]["input"]

    st.subheader(f"{question}")

    with st.form(key=f"form_{idx}"):
        reponse = st.text_input("Ta réponse :")
        valider = st.form_submit_button("Valider")

    if valider:
        if reponse.strip():
            data[idx]["output"] = reponse.strip()
            sauvegarder(data)
            st.rerun()
        else:
            st.warning("Merci d'entrer une réponse avant de valider.")