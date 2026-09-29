from langchain.tools import tool


def construire_questionnaire(motif: str) -> list:
    """
    Génère une liste de questions cliniques adaptées
    au motif de consultation du patient.
    """
    questions = []
    motif_lower = motif.lower()

    # Question d'ouverture générique
    questions.append(f"Pouvez-vous décrire précisément ce que vous ressentez concernant '{motif}'?")

    if any(terme in motif_lower for terme in ["tete", "céphalée", "migraine", "mal de tête"]):
        questions.extend([
            "La douleur est-elle pulsatile ou en pression constante?",
            "Est-elle localisée d'un côté ou diffuse?",
            "Avez-vous des nausées, une photophobie ou une phonophobie associées?",
        ])
    elif any(terme in motif_lower for terme in ["fièvre", "fievre", "température", "frissons"]):
        questions.extend([
            "Avez-vous mesuré votre température? Quel est le chiffre?",
            "Avez-vous des frissons ou des sueurs nocturnes?",
            "D'autres symptômes accompagnent-ils la fièvre (toux, maux de gorge, éruption)?",
        ])
    elif any(terme in motif_lower for terme in ["douleur", "mal", "douleurs"]):
        questions.extend([
            "Pouvez-vous localiser précisément la douleur?",
            "La douleur irradie-t-elle vers d'autres zones?",
            "Qu'est-ce qui la déclenche ou la soulage?",
        ])
    else:
        questions.extend([
            "Depuis quand ressentez-vous ces symptômes?",
            "Est-ce un épisode nouveau ou avez-vous déjà vécu cela?",
            "Avez-vous d'autres manifestations associées?",
        ])

    # Question de clôture systématique
    questions.append("Prenez-vous des médicaments ou avez-vous des antécédents médicaux importants?")

    return questions[:5]


@tool
def recueillir_reponse(question: str) -> str:
    """Pose une question médicale au patient et retourne sa réponse."""
    print(f"\n[MÉDECIN] {question}")
    return input("[PATIENT] ")
