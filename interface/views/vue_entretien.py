"""Vue d'entretien clinique — Questionnaire patient"""

import streamlit as st
from ..utils.http_client import client


def vue_entretien():
    st.title("Entretien Clinique")

    record_id = st.session_state.get("record_id")
    motif = st.session_state.get("motif")

    st.markdown(f"**Motif de consultation**: {motif}")
    st.markdown("---")

    if "liste_questions" not in st.session_state:
        try:
            resp = client.get_questions(record_id)
            if resp and "error" not in resp:
                st.session_state.liste_questions = resp.get("questions", [])
            else:
                st.error(f"Erreur: {resp.get('error', 'Inconnue')}")
                return
        except Exception as e:
            st.error(f"Impossible de charger le questionnaire: {e}")
            return

    questions = st.session_state.get("liste_questions", [])

    if not questions:
        st.warning("Aucune question disponible pour ce motif")
        return

    if "saisies" not in st.session_state:
        st.session_state.saisies = {}

    st.info(f"Veuillez répondre aux {len(questions)} questions de l'entretien clinique")

    for idx, question in enumerate(questions, start=1):
        st.markdown(f"**Question {idx}** — {question}")
        st.session_state.saisies[f"r{idx}"] = st.text_area(
            label=f"Réponse {idx}",
            key=f"saisie_{idx}",
            height=65,
            label_visibility="collapsed",
        )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Retour"):
            st.session_state.vue = "accueil"
            st.rerun()

    with col2:
        if st.button("Valider les réponses", type="primary", use_container_width=True):
            saisies_valides = [v.strip() for v in st.session_state.saisies.values() if v.strip()]
            if len(saisies_valides) < len(questions):
                st.error(f"Merci de répondre aux {len(questions)} questions avant de continuer")
                return

            try:
                reponses_ordonnees = [st.session_state.saisies[f"r{i}"] for i in range(1, len(questions) + 1)]
                resp = client.soumettre_reponses(record_id, reponses_ordonnees)

                if "error" not in resp:
                    st.session_state.vue = "medecin"
                    st.rerun()
                else:
                    st.error(f"Erreur: {resp['error']}")
            except Exception as e:
                st.error(f"Erreur lors de la soumission: {e}")
