"""
MedAI System — Point d'entrée principal
Démarrage du serveur: python run.py
"""

import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("MEDAI_HOST", "127.0.0.1")
PORT = int(os.getenv("MEDAI_PORT", "8000"))
RELOAD = os.getenv("MEDAI_RELOAD", "false").lower() == "true"

if __name__ == "__main__":
    import uvicorn

    print(f"\n[MedAI] Démarrage du serveur sur http://{HOST}:{PORT}")
    print(f"[MedAI] Documentation API : http://{HOST}:{PORT}/docs\n")
    uvicorn.run("medai_system.server.routes:app", host=HOST, port=PORT, reload=RELOAD)
