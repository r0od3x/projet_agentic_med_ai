# MedAI System — Système de Consultation Médicale Multi-Agents

Plateforme de consultation médicale assistée par intelligence artificielle, construite sur une architecture multi-agents LangGraph.

## Architecture

```
medai_system/
├── core/
│   ├── schema.py              # Schéma d'état (ConsultationContext)
│   ├── pipeline.py            # Pipeline LangGraph
│   └── agents/
│       ├── orchestrateur.py   # Nœud d'orchestration
│       ├── triage_agent.py    # Agent de triage et diagnostic
│       ├── doctor_validation.py  # Validation médicale
│       └── synthesis_agent.py    # Génération du compte-rendu
│   └── tools/
│       ├── questionnaire.py   # Génération de questions adaptées
│       ├── analyse_clinique.py   # Synthèse et soins initiaux
│       └── ai_tools.py        # Moteur IA médical
├── server/
│   └── routes.py              # API FastAPI
├── interface/
│   ├── app_ui.py              # Application Streamlit
│   ├── views/                 # Vues Streamlit
│   └── utils/http_client.py  # Client HTTP
├── data_store/
│   └── record_store.py        # Persistance JSON des dossiers
└── mcp_module/
    └── medical_hub.py         # Hub de ressources MCP
```

## Pipeline Multi-Agents

```
[Orchestrateur]
      ↓
[Triage Agent] → collecte patient + analyse IA
      ↓
[Orchestrateur]
      ↓
[Doctor Validation] → observations + prescription médecin
      ↓
[Orchestrateur]
      ↓
[Synthesis Agent] → compte-rendu médical final
      ↓
[FINISH]
```

## Démarrage

### 1. Variables d'environnement
```bash
cp .env.example .env
# Renseigner OPENAI_API_KEY dans .env
```

### 2. Serveur backend
```bash
pip install -r requirements_server.txt
python run.py
```

### 3. Interface Streamlit
```bash
pip install -r requirements_ui.txt
cd interface
streamlit run app_ui.py
```

## Technologies

- **LangGraph** — Orchestration du pipeline multi-agents
- **LangChain / OpenAI GPT-4** — Traitement du langage naturel
- **FastAPI** — API REST backend
- **Streamlit** — Interface utilisateur
- **MCP** — Protocole de ressources médicales
