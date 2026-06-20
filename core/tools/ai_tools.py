from langchain.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
_llm = ChatOpenAI(model="gpt-4", temperature=0.3)


class AIMedicalEngine:
    """
    Moteur IA médical : fournit des capacités d'analyse
    clinique via LLM pour les agents du pipeline.
    """

    def __init__(self):
        self._registered = {}

    def register(self, name: str, fn):
        self._registered[name] = fn

    def capabilities(self):
        return {
            "symptom_analysis": self.analyser_symptomes,
            "interaction_check": self.verifier_interactions,
            "medical_reference": self.fetch_reference,
            "alert_detection": self.detecter_alertes,
        }

    @tool
    def analyser_symptomes(symptomes: list) -> dict:
        """Analyse une liste de symptômes et produit une évaluation médicale."""
        prompt = f"""Évalue les symptômes suivants et fournis une appréciation médicale prudente:

Symptômes: {', '.join(symptomes)}

Retourne un objet JSON avec:
- severity: low / medium / high
- urgency: monitoring / consultation / emergency
- possible_causes: 3 à 5 hypothèses diagnostiques
- red_flags: liste des signes d'alarme identifiés"""

        try:
            result = _llm.invoke(prompt)
            return {"status": "ok", "analysis": result.content, "data": symptomes}
        except Exception as err:
            return {"status": "error", "error": str(err), "data": symptomes}

    @tool
    def verifier_interactions(medicaments: list) -> dict:
        """Vérifie les interactions potentielles entre médicaments."""
        prompt = f"""Analyse les interactions possibles entre les médicaments suivants:

Médicaments: {', '.join(medicaments)}

Retourne un objet JSON avec:
- interaction_risk: low / medium / high
- contraindications: liste des contre-indications
- recommendations: mesures de prudence
- monitoring_needed: surveillance spécifique à mettre en place"""

        try:
            result = _llm.invoke(prompt)
            return {"status": "ok", "analysis": result.content, "data": medicaments}
        except Exception as err:
            return {"status": "error", "error": str(err), "data": medicaments}

    @tool
    def fetch_reference(condition: str) -> dict:
        """Récupère des informations médicales de référence sur une condition."""
        prompt = f"""Fournis des informations médicales générales sur la condition suivante:

Condition: {condition}

Retourne un objet JSON avec:
- description: définition médicale concise
- common_symptoms: symptômes typiquement associés
- general_approach: démarche diagnostique standard
- when_seek_care: quand consulter en urgence
- sources: références médicales recommandées"""

        try:
            result = _llm.invoke(prompt)
            return {"status": "ok", "reference": result.content, "condition": condition}
        except Exception as err:
            return {"status": "error", "error": str(err), "condition": condition}

    @tool
    def detecter_alertes(texte_symptomes: str) -> dict:
        """Détecte les signaux d'alerte (red flags) dans un texte de symptômes."""
        prompt = f"""Analyse ce texte et identifie les signaux d'alerte cliniques:

Texte: {texte_symptomes}

Retourne un objet JSON avec:
- red_flags_detected: true / false
- urgency_level: low / medium / high / critical
- specific_flags: liste des signaux identifiés
- immediate_action: action immédiate recommandée
- ed_indications: critères d'orientation vers les urgences"""

        try:
            result = _llm.invoke(prompt)
            return {"status": "ok", "red_flags": result.content, "input": texte_symptomes}
        except Exception as err:
            return {"status": "error", "error": str(err), "input": texte_symptomes}


# Instance globale du moteur IA médical
ai_medical = AIMedicalEngine()
