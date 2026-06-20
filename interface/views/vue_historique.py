"""Vue historique — Liste des dossiers de consultation"""

import streamlit as st
from ..utils.http_client import client


def vue_historique():
    st.title("Historique des Dossiers")

    try:
        data = client.lister_dossiers()
        dossiers = data.get("dossiers", [])
        total = data.get("total", 0)

        st.markdown(f"**{total} dossier(s) enregistré(s)**")

        if not dossiers:
            st.info("Aucun dossier disponible pour le moment")
        else:
            st.markdown("---")
            for dossier in dossiers:
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.markdown(f"**ID** : `{dossier['record_id'][:12]}...`")
                with c2:
                    st.markdown(f"**Motif** : {dossier.get('motif', 'N/D')}")
                with c3:
                    etape = dossier.get("etape", "?")
                    icone = "✓" if etape == "compte_rendu" else ("⊙" if etape == "medecin" else "•")
                    st.markdown(f"{icone} {etape}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Erreur de chargement: {e}")

    if st.button("← Retour à l'accueil"):
        st.session_state.vue = "accueil"
        st.rerun()
