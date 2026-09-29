"""
Client HTTP pour la communication avec le serveur MedAI System.
"""

import os

import requests
from typing import Optional, Dict, Any

_BASE = os.getenv("MEDAI_SERVER_URL", "http://localhost:8000").rstrip("/")


class MedAIClient:
    def __init__(self, server_url: str = _BASE):
        self.url = server_url
        self.timeout = float(os.getenv("MEDAI_HTTP_TIMEOUT", "120"))

    def _get(self, path: str, **kwargs) -> Optional[Dict[str, Any]]:
        try:
            r = requests.get(f"{self.url}{path}", timeout=self.timeout, **kwargs)
            return r.json() if r.status_code == 200 else None
        except Exception as e:
            print(f"[CLIENT] GET {path} → erreur: {e}")
            return None

    def _post(self, path: str, **kwargs) -> Dict[str, Any]:
        try:
            r = requests.post(f"{self.url}{path}", timeout=self.timeout, **kwargs)
            return r.json() if r.status_code == 200 else {"error": f"HTTP {r.status_code}", "details": r.text}
        except Exception as e:
            print(f"[CLIENT] POST {path} → erreur: {e}")
            return {"error": str(e)}

    def is_online(self) -> bool:
        """Vérifie que le serveur répond."""
        try:
            r = requests.get(f"{self.url}/ping", timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def nouveau_dossier(self) -> Optional[str]:
        """Crée un nouveau dossier et retourne son identifiant."""
        data = self._post("/dossiers/nouveau")
        return data.get("record_id") if data else None

    def initialiser_consultation(
        self, record_id: str, motif: str, historique: str = ""
    ) -> Dict[str, Any]:
        """Initialise une consultation avec le motif et l'historique."""
        return self._post(
            "/consultation/init",
            params={"record_id": record_id},
            json={"motif_consultation": motif, "historique_medical": historique or ""},
        )

    def get_etat(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Retourne l'état courant d'une consultation."""
        return self._get(f"/consultation/{record_id}")

    def get_questions(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Récupère les questions cliniques."""
        return self._get(f"/consultation/{record_id}/questions")

    def soumettre_reponses(self, record_id: str, reponses: list) -> Dict[str, Any]:
        """Soumet les réponses patient."""
        return self._post(
            f"/consultation/{record_id}/reponses",
            json={"reponses": reponses},
        )

    def valider_medecin(
        self, record_id: str, commentaires: str = "", prescription: str = ""
    ) -> Dict[str, Any]:
        """Enregistre les observations du médecin."""
        return self._post(
            f"/consultation/{record_id}/medecin",
            json={"commentaires_medecin": commentaires, "prescription_medecin": prescription},
        )

    def reprendre(self, record_id: str, etape: str) -> bool:
        """Reprend une consultation interrompue."""
        data = self._post(
            "/consultation/reprendre",
            json={"record_id": record_id, "etape": etape},
        )
        return "error" not in data

    def get_compte_rendu(self, record_id: str) -> Optional[str]:
        """Génère et retourne le compte-rendu final."""
        data = self._get(f"/consultation/{record_id}/compte-rendu")
        return data.get("compte_rendu") if data else None

    def lister_dossiers(self) -> Dict[str, Any]:
        """Liste tous les dossiers de consultation."""
        data = self._get("/dossiers")
        return data if data else {"dossiers": [], "total": 0, "error": "Serveur inaccessible"}


# Instance partagée
client = MedAIClient()
