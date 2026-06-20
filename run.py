"""
MedAI System — Point d'entrée principal
Démarrage du serveur: python run.py
"""

import sys
sys.path.insert(0, "medai_system")

from server.routes import app

if __name__ == "__main__":
    import uvicorn
    print("\n[MedAI] Démarrage du serveur sur http://localhost:8000")
    print("[MedAI] Documentation API : http://localhost:8000/docs\n")
    uvicorn.run("medai_system.server.routes:app", host="0.0.0.0", port=8000, reload=True)
