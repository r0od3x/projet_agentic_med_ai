from ..schema import ConsultationContext
from ..tools.questionnaire import recueillir_reponse, construire_questionnaire
from ..tools.analyse_clinique import synthese_clinique, soins_initiaux
from ..tools.ai_tools import ai_medical


def triage_agent(ctx: ConsultationContext) -> ConsultationContext:
    """
    Agent de triage : collecte les informations patient,
    interroge les outils IA médicaux et produit un résumé clinique.
    """
    motif = ctx.get("motif_consultation", "Consultation générale")

    ctx.setdefault("liste_questions", [])
    ctx.setdefault("liste_reponses", [])
    ctx.setdefault("nb_questions", 0)

    # Étape 1 : récupérer le contexte médical de référence
    ref_medicale = ai_medical.fetch_reference(motif)

    # Étape 2 : construire un questionnaire adapté au motif
    questionnaire = construire_questionnaire(motif)

    # Étape 3 : poser les questions et collecter les réponses
    for idx, question in enumerate(questionnaire[:5], start=1):
        ctx["liste_questions"].append(question)
        reponse = recueillir_reponse(question)
        ctx["liste_reponses"].append(reponse)
        ctx["nb_questions"] = idx

    # Étape 4 : analyser les symptômes via IA
    contenu_reponses = " ".join(ctx["liste_reponses"])
    analyse_symptomes = ai_medical.analyser_symptomes([contenu_reponses])
    detection_alertes = ai_medical.detecter_alertes(contenu_reponses)

    # Construire le corpus d'analyse enrichi
    paires_qa = "\n".join([
        f"Q{i+1}: {q}\nR{i+1}: {r}"
        for i, (q, r) in enumerate(zip(ctx["liste_questions"], ctx["liste_reponses"]))
    ])

    corpus_enrichi = f"""
RECUEIL PATIENT:
{paires_qa}

RÉSULTATS IA:
- Référence médicale: {ref_medicale.get('reference', 'N/D')}
- Analyse symptomatique: {analyse_symptomes.get('analysis', 'N/D')}
- Signes d'alerte: {detection_alertes.get('red_flags', 'N/D')}
"""

    # Étape 5 : générer le résumé clinique et les soins initiaux
    ctx["resume_clinique"] = synthese_clinique(corpus_enrichi)
    ctx["soins_urgents"] = soins_initiaux(motif)
    ctx["current_node"] = "doctor_validation"

    return ctx
