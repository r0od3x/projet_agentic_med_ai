from langgraph.graph import StateGraph, END
from .schema import ConsultationContext
from .agents.orchestrateur import orchestrateur
from .agents.triage_agent import triage_agent
from .agents.doctor_validation import doctor_validation
from .agents.synthesis_agent import synthesis_agent


def _router(ctx: ConsultationContext) -> str:
    """Sélectionne le prochain nœud selon le champ current_node."""
    return ctx.get("current_node", "orchestrateur")


def build_pipeline():
    """Construit et compile le pipeline LangGraph de consultation médicale."""
    builder = StateGraph(ConsultationContext)

    # Enregistrement des nœuds
    builder.add_node("orchestrateur", orchestrateur)
    builder.add_node("triage_agent", triage_agent)
    builder.add_node("doctor_validation", doctor_validation)
    builder.add_node("synthesis_agent", synthesis_agent)

    # Point d'entrée
    builder.set_entry_point("orchestrateur")

    # Routage conditionnel depuis l'orchestrateur
    builder.add_conditional_edges(
        "orchestrateur",
        _router,
        {
            "triage_agent": "triage_agent",
            "doctor_validation": "doctor_validation",
            "synthesis_agent": "synthesis_agent",
            "FINISH": END,
        },
    )

    # Retour vers l'orchestrateur après chaque agent
    builder.add_edge("triage_agent", "orchestrateur")
    builder.add_edge("doctor_validation", "orchestrateur")
    builder.add_edge("synthesis_agent", "orchestrateur")

    return builder.compile()


# Pipeline compilé (singleton)
pipeline = build_pipeline()
