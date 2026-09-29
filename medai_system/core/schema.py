from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class ConsultationContext(TypedDict, total=False):
    """Contexte partagé du pipeline de consultation médicale IA"""
    messages: Annotated[list, add_messages]
    current_node: Literal["triage_agent", "doctor_validation", "synthesis_agent", "FINISH"]
    nb_questions: int
    liste_questions: list
    liste_reponses: list
    soins_urgents: str
    resume_clinique: str
    prescription_medecin: str
    commentaires_medecin: str
    compte_rendu: str
    motif_consultation: str
    historique_medical: str
