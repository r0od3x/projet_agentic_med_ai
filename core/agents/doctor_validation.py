from ..schema import ConsultationContext


def doctor_validation(ctx: ConsultationContext) -> ConsultationContext:
    """
    Nœud de validation médicale : affiche le résumé clinique
    et recueille les observations et prescriptions du médecin.
    """
    print("\n=== RÉSUMÉ CLINIQUE GÉNÉRÉ ===")
    print(ctx.get("resume_clinique", "Non disponible"))

    print("\n=== SOINS INITIAUX CONSEILLÉS ===")
    print(ctx.get("soins_urgents", "Non disponible"))

    print("\n=== ENTRETIEN PATIENT ===")
    for idx, (q, r) in enumerate(
        zip(ctx.get("liste_questions", []), ctx.get("liste_reponses", [])), start=1
    ):
        print(f"Q{idx}: {q}")
        print(f"R{idx}: {r}\n")

    ctx["commentaires_medecin"] = input("Observations cliniques du médecin: ")
    ctx["prescription_medecin"] = input("Traitement / Conduite à tenir: ")

    return ctx
