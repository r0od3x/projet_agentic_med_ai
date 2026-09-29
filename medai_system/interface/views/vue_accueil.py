"""Vue d'accueil — Saisie du motif de consultation"""

import streamlit as st
from utils.http_client import client


def vue_accueil():
    st.title("MedAI System")
    st.markdown("*Plateforme de consultation médicale assistée par IA*")

    st.markdown("### Nouveau dossier de consultation")

    if not client.is_online():
        st.error(
            f"Serveur indisponible. Vérifiez que le backend tourne sur {client.url}"
        )
        return

    col_gauche, col_droite = st.columns(2)

    with col_gauche:
        motif = st.text_area(
            "Motif de consultation",
            placeholder="Ex: Douleur thoracique depuis 2 jours",
            height=100,
        )

    with col_droite:
        historique = st.text_area(
            "Historique médical (facultatif)",
            placeholder="Ex: Diabète type 2, hypertension...",
            height=100,
        )

    if st.button("Ouvrir la consultation", type="primary", use_container_width=True):
        if not motif.strip():
            st.error("Veuillez renseigner le motif de consultation")
            return

        record_id = client.nouveau_dossier()
        if not record_id:
            st.error("Impossible de créer le dossier")
            return

        resp = client.initialiser_consultation(record_id, motif, historique)

        if resp and "error" not in resp:
            st.session_state.record_id = record_id
            st.session_state.motif = motif
            st.session_state.historique = historique
            st.session_state.vue = "entretien"
            st.rerun()
        else:
            st.error(f"Erreur lors de l'initialisation: {resp.get('error', 'Inconnue')}")
