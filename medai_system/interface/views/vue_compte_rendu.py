"""Vue compte-rendu — Rapport médical final"""

import streamlit as st
from utils.http_client import client
from datetime import datetime


def vue_compte_rendu():
    st.title("Compte-Rendu Médical")

    record_id = st.session_state.get("record_id")

    if "compte_rendu" not in st.session_state:
        cr = client.get_compte_rendu(record_id)
        st.session_state.compte_rendu = cr if cr else _generer_cr_local()

    cr = st.session_state.compte_rendu

    st.markdown(f"""
    **Date** : {datetime.now().strftime("%d/%m/%Y à %H:%M")}
    **Dossier** : `{record_id[:8]}...`
    """)

    st.markdown("---")
    st.markdown("### Compte-Rendu")
    st.write(cr)

    st.markdown("---")

    with st.expander("Récapitulatif de la consultation"):
        st.markdown(f"**Motif** : {st.session_state.get('motif')}")
        st.markdown(f"**Prescription** : {st.session_state.get('prescription')}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Nouvelle consultation", use_container_width=True):
            st.session_state.clear()
            st.session_state.vue = "accueil"
            st.rerun()

    with col2:
        st.download_button(
            label="Télécharger (TXT)",
            data=_formater_export(cr),
            file_name=f"cr_{record_id[:8]}.txt",
            use_container_width=True,
        )


def _generer_cr_local() -> str:
    """Génère un compte-rendu local en cas d'indisponibilité du serveur."""
    motif = st.session_state.get("motif", "Non renseigné")
    historique = st.session_state.get("historique", "Aucun")
    prescription = st.session_state.get("prescription", "À définir")
    commentaires = st.session_state.get("commentaires_medecin", "")
    saisies = st.session_state.get("saisies", {})

    cr = f"""## Compte-Rendu de Consultation

### Motif de Consultation
{motif}

### Historique Médical
{historique}

### Entretien Patient
"""
    for idx, (_, reponse) in enumerate(saisies.items(), start=1):
        cr += f"\n{idx}. {reponse}"

    cr += f"""

### Observations Médicales
{commentaires if commentaires else "Aucune observation complémentaire"}

### Prescription / Conduite à Tenir
{prescription}

### Date et Heure
{datetime.now().strftime("%d/%m/%Y à %H:%M")}
"""
    return cr


def _formater_export(cr: str) -> str:
    return f"""COMPTE-RENDU DE CONSULTATION MÉDICALE
=======================================

{cr}
"""
