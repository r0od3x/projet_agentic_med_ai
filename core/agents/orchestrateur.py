from ..schema import ConsultationContext


def orchestrateur(ctx: ConsultationContext) -> ConsultationContext:
    """
    Nœud orchestrateur : détermine la prochaine étape du pipeline
    en fonction de l'état courant de la consultation.
    """
    if not ctx.get("resume_clinique"):
        ctx["current_node"] = "triage_agent"
    elif not ctx.get("prescription_medecin"):
        ctx["current_node"] = "doctor_validation"
    elif not ctx.get("compte_rendu"):
        ctx["current_node"] = "synthesis_agent"
    else:
        ctx["current_node"] = "FINISH"
    return ctx
