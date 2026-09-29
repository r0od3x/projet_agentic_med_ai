# MedAI System — Consultation médicale multi-agents

Plateforme de pré-consultation médicale assistée par IA, construite sur une architecture
**multi-agents LangGraph**. Un agent de triage interroge le patient, un médecin valide et prescrit,
puis un agent de synthèse rédige le compte-rendu final.

> ⚠️ **Projet pédagogique.** MedAI ne remplace en aucun cas un avis médical professionnel.

| Couche | Technologies |
|---|---|
| Orchestration | LangGraph, LangChain |
| LLM | OpenAI (modèle configurable, `gpt-4o` par défaut) |
| API | FastAPI + Uvicorn |
| Interface | Streamlit |
| Persistance | Fichiers JSON (un dossier par consultation) |

---

## Fonctionnalités

- **Triage intelligent** — questionnaire adapté au motif de consultation, analyse des réponses par le LLM
- **Synthèse clinique** — symptômes principaux, hypothèses, signaux d'alerte, soins initiaux
- **Validation médecin** — observations et prescription saisies par le praticien
- **Compte-rendu final** — généré automatiquement et exportable
- **Historique** — liste et reprise des consultations interrompues
- **API documentée** — Swagger disponible sur `/docs`

---

## Pipeline multi-agents

```
[Orchestrateur]
      ↓
[Triage Agent]       → collecte patient + analyse IA
      ↓
[Orchestrateur]
      ↓
[Doctor Validation]  → observations + prescription médecin
      ↓
[Orchestrateur]
      ↓
[Synthesis Agent]    → compte-rendu médical final
      ↓
[FINISH]
```

---

## Structure du projet

```
projet_agentic_med_ai/
├── run.py                        # Démarrage du serveur API
├── langgraph.json                # Configuration LangGraph Studio
├── requirements_server.txt
├── requirements_ui.txt
├── .env.example
└── medai_system/
    ├── core/
    │   ├── config.py             # Configuration (modèle LLM, variables d'env)
    │   ├── schema.py             # État partagé (ConsultationContext)
    │   ├── pipeline.py           # Graphe LangGraph
    │   ├── agents/               # orchestrateur, triage, validation médecin, synthèse
    │   └── tools/                # questionnaire, analyse clinique, moteur IA
    ├── server/routes.py          # API FastAPI
    ├── interface/                # Application Streamlit (vues + client HTTP)
    ├── data_store/record_store.py  # Persistance JSON des dossiers
    └── mcp_module/medical_hub.py   # Hub de ressources médicales (MCP)
```

---

## Démarrage

Prérequis : **Python 3.10+** et une clé API OpenAI.

### 1. Configuration

```bash
cp .env.example .env
# puis renseigner OPENAI_API_KEY dans .env
```

| Variable | Description | Défaut |
|---|---|---|
| `OPENAI_API_KEY` | Clé API OpenAI (**obligatoire**) | — |
| `OPENAI_MODEL` | Modèle utilisé par les agents | `gpt-4o` |
| `MEDAI_HOST` / `MEDAI_PORT` | Adresse d'écoute de l'API | `127.0.0.1` / `8000` |
| `MEDAI_RELOAD` | Rechargement automatique (dev) | `false` |
| `MEDAI_SERVER_URL` | URL de l'API utilisée par l'interface | `http://localhost:8000` |
| `MEDAI_HTTP_TIMEOUT` | Timeout des appels interface → API (s) | `120` |

### 2. Serveur backend

```bash
pip install -r requirements_server.txt
python run.py
```

API : http://localhost:8000 — documentation : http://localhost:8000/docs

### 3. Interface Streamlit

```bash
pip install -r requirements_ui.txt
streamlit run medai_system/interface/app_ui.py
```

### (Optionnel) LangGraph Studio

```bash
langgraph dev    # utilise langgraph.json → graphe « consultation_pipeline »
```

---

## Principaux endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/ping` | État du serveur |
| POST | `/dossiers/nouveau` | Crée un dossier de consultation |
| GET | `/dossiers` | Liste des dossiers |
| POST | `/consultation/init` | Démarre une consultation (motif, antécédents) |
| GET | `/consultation/{id}/questions` | Questions cliniques générées |
| POST | `/consultation/{id}/reponses` | Réponses du patient |
| POST | `/consultation/{id}/medecin` | Observations et prescription du médecin |
| GET | `/consultation/{id}/compte-rendu` | Compte-rendu final |
| POST | `/consultation/reprendre` | Reprise d'une consultation interrompue |
