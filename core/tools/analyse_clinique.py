from langchain.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
_llm = ChatOpenAI(model="gpt-4", temperature=0.7)


@tool
def synthese_clinique(corpus: str) -> str:
    """Génère une synthèse clinique préliminaire à partir du corpus patient."""
    prompt = f"""À partir du recueil patient suivant, produis une synthèse clinique préliminaire:

{corpus}

La synthèse doit couvrir:
1. Symptômes principaux identifiés
2. Orientation clinique provisoire (prudente et non définitive)
3. Signaux d'alerte détectés
4. Points nécessitant un approfondissement
5. Premières recommandations générales"""

    return _llm.invoke(prompt).content


@tool
def soins_initiaux(symptomes: str) -> str:
    """Produit des recommandations de soins initiaux en attendant la consultation."""
    prompt = f"""Sur la base des symptômes suivants, formule des conseils de soins initiaux:

Symptômes: {symptomes}

Les recommandations doivent inclure:
- Repos et activité physique adaptée
- Hydratation et alimentation
- Surveillance des signes d'aggravation
- Critères d'appel aux urgences"""

    return _llm.invoke(prompt).content
