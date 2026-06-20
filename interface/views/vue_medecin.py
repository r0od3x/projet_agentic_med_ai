"""Vue médecin — Revue clinique et prescription"""

import streamlit as st
from ..utils.http_client import client


def vue_medecin():
    st.title("Espace Médecin")

    record_id = st.session_state.get("record_id")

    st.markdown(f"**Motif**: {st.session_state.get('motif')}")
    st.markdown("---")

    if "etat_dossier" not in st.session_state:
        try:
            etat = client.get_etat(record_id)
            if etat and "error" not in etat:
                st.session_state.etat_dossier = etat
            else:
                st.warning("Impossible de charger le dossier")
        except Exception as e:
            st.warning(f"Erreur de chargement: {e}")

    etat = st.session_state.get("etat_dossier", {})

    st.markdown("### Résumé Clinique")
    resume = etat.get("resume_clinique", "En cours de génération...")
    st.info(resume if resume else "Données non disponibles")

    st.markdown("### Entretien Patient")
    questions = etat.get("liste_questions", [])
    reponses = etat.get("liste_reponses", [])

    for q, r in zip(questions, reponses):
        st.markdown(f"**Q** : {q}")
        st.markdown(f"**R** : {r}")

    st.markdown("---")
    st.markdown("### Observations et Prescription")

    commentaires = st.text_area(
        "Vos observations cliniques",
        placeholder="Saisissez vos observations...",
        height=80,
        label_visibility="collapsed",
    )

    prescription = st.text_area(
        "Traitement / Conduite à tenir",
        placeholder="Ex: Paracétamol 1g x3/j, repos 48h...",
        height=80,
        label_visibility="collapsed",
    )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Retour"):
            st.session_state.vue = "entretien"
            st.rerun()

    with col2:
        if st.button("Générer le compte-rendu", type="primary", use_container_width=True):
            if not prescription.strip():
                st.error("Veuillez renseigner le traitement ou la conduite à tenir")
                return

            try:
                resp = client.valider_medecin(record_id, commentaires, prescription)
                if "error" not in resp:
                    st.session_state.commentaires_medecin = commentaires
                    st.session_state.prescription = prescription
                    st.session_state.vue = "compte_rendu"
                    st.rerun()
                else:
                    st.error(f"Erreur: {resp['error']}")
            except Exception as e:
                st.error(f"Erreur lors de l'envoi: {e}")
