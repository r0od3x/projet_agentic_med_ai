import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

_STORE_PATH = Path(__file__).parent / "records"
_STORE_PATH.mkdir(exist_ok=True)


class RecordStore:
    """Gère la persistance des dossiers de consultation en JSON."""

    @staticmethod
    def _record_path(rid: str) -> Path:
        return _STORE_PATH / f"{rid}.json"

    @classmethod
    def init_record(cls, rid: str) -> Dict[str, Any]:
        """Initialise un nouveau dossier de consultation."""
        record = {
            "record_id": rid,
            "messages": [],
            "etape_courante": "orchestrateur",
            "nb_questions": 0,
            "liste_questions": [],
            "liste_reponses": [],
            "motif_consultation": "",
            "historique_medical": "",
            "resume_clinique": "",
            "soins_urgents": "",
            "prescription_medecin": "",
            "commentaires_medecin": "",
            "compte_rendu": "",
        }
        cls.save_record(rid, record)
        return record

    @classmethod
    def save_record(cls, rid: str, data: Dict[str, Any]) -> None:
        """Sauvegarde un dossier."""
        with open(cls._record_path(rid), "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    @classmethod
    def load_record(cls, rid: str) -> Optional[Dict[str, Any]]:
        """Charge un dossier existant, retourne None si introuvable."""
        path = cls._record_path(rid)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    @classmethod
    def all_records(cls) -> list:
        """Retourne la liste de tous les dossiers disponibles."""
        result = []
        for fp in _STORE_PATH.glob("*.json"):
            try:
                with open(fp, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    result.append({
                        "record_id": data.get("record_id"),
                        "motif": data.get("motif_consultation"),
                        "etape": data.get("etape_courante"),
                    })
            except Exception:
                pass
        return result

    @classmethod
    def remove_record(cls, rid: str) -> bool:
        """Supprime un dossier. Retourne True si trouvé et supprimé."""
        path = cls._record_path(rid)
        if path.exists():
            path.unlink()
            return True
        return False
