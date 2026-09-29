"""
MedAI System — Interface Streamlit
Lancement: streamlit run interface/app_ui.py
"""

import streamlit as st
from views.vue_accueil import vue_accueil
from views.vue_entretien import vue_entretien
from views.vue_medecin import vue_medecin
from views.vue_compte_rendu import vue_compte_rendu
from views.vue_historique import vue_historique


st.set_page_config(
    page_title="MedAI System",
    page_icon=":stethoscope:",
    layout="wide",
)

# ── Barre latérale ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Navigation")
    if "record_id" in st.session_state:
        st.info(f"Dossier : {st.session_state.record_id[:8]}...")

    c_hist, c_reset = st.columns(2)
    with c_hist:
        if st.button("Historique", use_container_width=True):
            st.session_state.vue = "historique"
            st.rerun()
    with c_reset:
        if st.button("Réinitialiser", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("---")
    st.markdown("""
    ### À propos

    Système multi-agents de consultation médicale assistée par IA.

    Stack technique :
    - LangGraph (pipeline agents)
    - FastAPI (backend)
    - Streamlit (interface)
    """)

# ── Initialisation ────────────────────────────────────────────────────────────
if "vue" not in st.session_state:
    st.session_state.vue = "accueil"

# ── Routage ───────────────────────────────────────────────────────────────────
_vues = {
    "accueil": vue_accueil,
    "entretien": vue_entretien,
    "medecin": vue_medecin,
    "compte_rendu": vue_compte_rendu,
    "historique": vue_historique,
}

vue_fn = _vues.get(st.session_state.vue)
if vue_fn:
    vue_fn()
else:
    st.error("Vue inconnue")
    st.session_state.vue = "accueil"
    st.rerun()
