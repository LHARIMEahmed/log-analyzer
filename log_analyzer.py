import os
import sys
import hashlib
from collections import defaultdict, Counter

def analyser_log(fichier_log):
    compteur = Counter()

    try:
        with open(fichier_log, "r") as fichier:
            for ligne in fichier:
                if "ERROR" in ligne:
                    compteur["ERROR"] += 1
                elif "WARNING" in ligne:
                    compteur["WARNING"] += 1
                elif "INFO" in ligne:
                    compteur["INFO"] += 1
    except FileNotFoundError:
        print(f"Fichier {fichier_log} introuvable.")
        sys.exit(1)

    return compteur

def calculer_hash(fichier_path, algo="sha256"):
    h = hashlib.new(algo)
    try:
        with open(fichier_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_path} est introuvable.")
        return None
    except PermissionError:
        print(f"Erreur : Permission refusée pour {fichier_path}.")
        return None
    except Exception as e:
        print(f"Erreur inattendue pour {fichier_path} : {e}")
        return None

def trouver_doublons_par_hash(dossier, algo="sha256"):
    hash_to_files = defaultdict(list)

    for root, _, files in os.walk(dossier):
        for nom_fichier in files:
            chemin_complet = os.path.join(root, nom_fichier)
            hash_fichier = calculer_hash(chemin_complet, algo)
            if hash_fichier:
                hash_to_files[hash_fichier].append(chemin_complet)

    doublons = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    return doublons

def ecrire_rapport(compteur, fichier_log, doublons, fichier_rapport="rapport.txt"):
    hash_log = calculer_hash(fichier_log)

    with open(fichier_rapport, "w") as f:
        f.write("=== Rapport d'analyse ===\n")
        for niveau in ["ERROR", "WARNING", "INFO"]:
            f.write(f"{niveau} : {compteur.get(niveau, 0)}\n")
        f.write(f"\nHash SHA256 de {fichier_log} : {hash_log}\n")

        f.write("\n=== Fichiers ayant le même hash (doublons) ===\n")
        if doublons:
            for h, fichiers in doublons.items():
                f.write(f"\nHash : {h}\n")
                for fichier in fichiers:
                    f.write(f" - {fichier}\n")
        else:
            f.write("Aucun doublon trouvé.\n")

    print(f"Rapport généré : {fichier_rapport}")

if __name__ == "__main__":
    fichier_log = "log.txt"
    dossier_a_verifier = sys.argv[1] if len(sys.argv) > 1 else "."  # Dossier via argument ou courant
    stats = analyser_log(fichier_log)
    doublons = trouver_doublons_par_hash(dossier_a_verifier)
    ecrire_rapport(stats, fichier_log, doublons)