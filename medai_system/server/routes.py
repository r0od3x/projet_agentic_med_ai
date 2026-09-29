from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid

from ..core.pipeline import pipeline
from ..core.schema import ConsultationContext
from ..data_store.record_store import RecordStore
from ..core.tools.questionnaire import construire_questionnaire

app = FastAPI(title="MedAI System — Consultation Multi-Agents")


# ── Schémas de requête ────────────────────────────────────────────────────────

class NouveauDossier(BaseModel):
    motif_consultation: str
    historique_medical: Optional[str] = None


class RepriseConsultation(BaseModel):
    record_id: str
    etape: str


class SoumissionReponses(BaseModel):
    reponses: list


class ValidationMedecin(BaseModel):
    commentaires_medecin: str = ""
    prescription_medecin: str = ""


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
async def index():
    return {
        "application": "MedAI System",
        "version": "2.0",
        "documentation": "/docs",
    }


@app.get("/ping")
async def ping():
    return {"status": "online"}


@app.post("/dossiers/nouveau")
async def creer_dossier():
    """Crée un nouveau dossier de consultation."""
    rid = str(uuid.uuid4())
    RecordStore.init_record(rid)
    return {"record_id": rid, "message": "Dossier créé"}


@app.get("/dossiers")
async def lister_dossiers():
    """Liste tous les dossiers de consultation."""
    dossiers = RecordStore.all_records()
    return {"dossiers": dossiers, "total": len(dossiers)}


@app.post("/consultation/init")
async def initialiser_consultation(payload: NouveauDossier, record_id: str):
    """Initialise une consultation avec le motif et l'historique médical."""
    dossier = RecordStore.load_record(record_id)
    if not dossier:
        return {"error": "Dossier introuvable"}

    dossier["motif_consultation"] = payload.motif_consultation
    dossier["historique_medical"] = payload.historique_medical or ""
    dossier["current_node"] = "triage_agent"
    dossier["nb_questions"] = 0
    dossier["liste_questions"] = []
    dossier["liste_reponses"] = []

    questions = construire_questionnaire(payload.motif_consultation)
    dossier["liste_questions"] = questions[:5]
    RecordStore.save_record(record_id, dossier)

    print(f"\n[SERVER] Consultation initialisée — Dossier: {record_id}")
    print(f"[SERVER] Motif: {payload.motif_consultation}")

    return {
        "record_id": record_id,
        "message": "Consultation initialisée",
        "motif": payload.motif_consultation,
        "questions": dossier["liste_questions"],
        "nb_questions": len(dossier["liste_questions"]),
        "prochaine_etape": "triage_agent",
    }


@app.post("/consultation/reprendre")
async def reprendre_consultation(payload: RepriseConsultation):
    """Reprend une consultation à une étape donnée."""
    dossier = RecordStore.load_record(payload.record_id)
    if not dossier:
        return {"error": "Dossier introuvable"}

    return {
        "record_id": payload.record_id,
        "message": "Consultation reprise",
        "etape": dossier.get("current_node"),
        "nb_questions": dossier.get("nb_questions", 0),
        "liste_questions": dossier.get("liste_questions", []),
        "liste_reponses": dossier.get("liste_reponses", []),
    }


@app.get("/consultation/{record_id}/questions")
async def get_questions(record_id: str):
    """Récupère le questionnaire associé à la consultation."""
    dossier = RecordStore.load_record(record_id)
    if not dossier:
        return {"error": "Dossier introuvable"}

    return {
        "record_id": record_id,
        "motif": dossier.get("motif_consultation"),
        "questions": dossier.get("liste_questions", []),
        "count": len(dossier.get("liste_questions", [])),
    }


@app.post("/consultation/{record_id}/reponses")
async def soumettre_reponses(record_id: str, body: SoumissionReponses):
    """Enregistre les réponses du patient aux questions cliniques."""
    dossier = RecordStore.load_record(record_id)
    if not dossier:
        return {"error": "Dossier introuvable"}

    dossier["liste_reponses"] = body.reponses
    dossier["nb_questions"] = len(body.reponses)
    dossier["current_node"] = "doctor_validation"
    RecordStore.save_record(record_id, dossier)

    print(f"[SERVER] Réponses enregistrées — Dossier: {record_id} ({len(body.reponses)} réponses)")

    return {
        "record_id": record_id,
        "message": "Réponses enregistrées",
        "count": len(body.reponses),
        "prochaine_etape": "doctor_validation",
    }


@app.get("/consultation/{record_id}")
async def get_dossier(record_id: str):
    """Retourne l'état complet d'une consultation."""
    dossier = RecordStore.load_record(record_id)
    if not dossier:
        return {"error": "Dossier introuvable"}

    return {
        "record_id": record_id,
        "current_node": dossier.get("current_node"),
        "motif": dossier.get("motif_consultation"),
        "historique_medical": dossier.get("historique_medical"),
        "liste_questions": dossier.get("liste_questions", []),
        "nb_questions": dossier.get("nb_questions", 0),
        "liste_reponses": dossier.get("liste_reponses", []),
        "resume_clinique": dossier.get("resume_clinique", ""),
        "soins_urgents": dossier.get("soins_urgents", ""),
        "commentaires_medecin": dossier.get("commentaires_medecin", ""),
        "prescription_medecin": dossier.get("prescription_medecin", ""),
        "compte_rendu": dossier.get("compte_rendu", ""),
    }


@app.post("/consultation/{record_id}/medecin")
async def valider_medecin(record_id: str, body: ValidationMedecin):
    """Enregistre les notes et la prescription du médecin."""
    dossier = RecordStore.load_record(record_id)
    if not dossier:
        return {"error": "Dossier introuvable"}

    dossier["commentaires_medecin"] = body.commentaires_medecin
    dossier["prescription_medecin"] = body.prescription_medecin
    dossier["current_node"] = "synthesis_agent"
    RecordStore.save_record(record_id, dossier)

    print(f"[SERVER] Validation médecin — Dossier: {record_id}")

    return {
        "record_id": record_id,
        "message": "Validation médicale enregistrée",
        "prochaine_etape": "synthesis_agent",
    }


@app.get("/consultation/{record_id}/compte-rendu")
async def get_compte_rendu(record_id: str):
    """Génère et retourne le compte-rendu final de la consultation."""
    dossier = RecordStore.load_record(record_id)
    if not dossier:
        return {"error": "Dossier introuvable"}

    if not dossier.get("compte_rendu"):
        from ..core.agents.synthesis_agent import synthesis_agent
        dossier = synthesis_agent(dossier)
        RecordStore.save_record(record_id, dossier)

    print(f"[SERVER] Compte-rendu généré — Dossier: {record_id}")

    return {
        "record_id": record_id,
        "compte_rendu": dossier.get("compte_rendu", "Compte-rendu non disponible"),
        "prochaine_etape": "FINISH",
    }
