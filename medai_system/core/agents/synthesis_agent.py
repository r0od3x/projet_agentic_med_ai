from ..schema import ConsultationContext
from ..tools.ai_tools import ai_medical
from ..config import get_llm

_llm = get_llm(temperature=0.7)


def synthesis_agent(ctx: ConsultationContext) -> ConsultationContext:
    """
    Agent de synthèse : génère le compte-rendu médical final
    à partir de l'ensemble des données de la consultation.
    """
    # Construire le résumé des échanges patient
    paires_qa = "\n".join([
        f"Q{i}: {q} - R{i}: {r}"
        for i, (q, r) in enumerate(
            zip(ctx.get("liste_questions", []), ctx.get("liste_reponses", [])), start=1
        )
    ])

    # Vérification des interactions médicamenteuses si nécessaire
    medicaments_cites = [
        r for r in ctx.get("liste_reponses", [])
        if any(terme in r.lower() for terme in ["médicament", "traitement", "pharmacie", "comprimé", "pilule"])
    ]
    analyse_interactions = "Non applicable"
    if medicaments_cites:
        analyse_interactions = ai_medical.verifier_interactions(medicaments_cites)

    # Rédaction du prompt de génération du compte-rendu
    prompt_cr = f"""Rédige un compte-rendu médical complet, structuré et professionnel.

DONNÉES DE LA CONSULTATION:
- Motif de consultation: {ctx.get('motif_consultation', 'N/D')}
- Historique médical: {ctx.get('historique_medical', 'N/D')}
- Échanges patient-médecin: {paires_qa}
- Résumé clinique: {ctx.get('resume_clinique', 'N/D')}
- Soins initiaux conseillés: {ctx.get('soins_urgents', 'N/D')}
- Observations du médecin: {ctx.get('commentaires_medecin', 'N/D')}
- Traitement prescrit: {ctx.get('prescription_medecin', 'N/D')}
- Analyse interactions médicamenteuses: {analyse_interactions}

STRUCTURE DU COMPTE-RENDU:
1. SYNTHÈSE DU DOSSIER
   - Identification du patient
   - Motif de consultation
   - Contexte général

2. PLAINTE PRINCIPALE ET SYMPTOMATOLOGIE
   - Description détaillée
   - Chronologie et évolution
   - Facteurs aggravants / soulageants

3. ANAMNÈSE
   - Questions posées lors de l'entretien
   - Réponses du patient
   - Antécédents pertinents

4. ÉVALUATION CLINIQUE
   - Résumé diagnostique
   - Analyse symptomatique
   - Signaux d'alerte détectés

5. PLAN DE PRISE EN CHARGE
   - Traitement prescrit
   - Recommandations hygiéno-diététiques
   - Modalités de suivi

6. CONCLUSION ET PRONOSTIC
   - Bilan général
   - Points de vigilance
   - Prochaine étape

Rédige un compte-rendu exhaustif, clair et exploitable cliniquement."""

    ctx["compte_rendu"] = _llm.invoke(prompt_cr).content
    return ctx
