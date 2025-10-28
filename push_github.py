import subprocess
import datetime

# Chemin vers le dépôt
repo_path = r"C:\Depot git"

# Message de commit avec date et heure
commit_message = f"Mise à jour automatique {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def run_git_command(command):
    """Exécute une commande git dans le dépôt et renvoie le code de retour et la sortie."""
    result = subprocess.run(
        command,
        cwd=repo_path,
        text=True,
        capture_output=True,
        shell=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

# Vérifie si le dépôt a des changements à committer
code, stdout, stderr = run_git_command(["git", "status", "--porcelain"])

if code != 0:
    print(f"Erreur Git : {stderr}")
    exit(1)

if stdout == "":
    print("✅ Aucun changement à committer.")
else:
    try:
        # Ajouter tous les fichiers suivis
        code, out, err = run_git_command(["git", "add", "."])
        if code != 0:
            raise Exception(err)

        # Créer le commit
        code, out, err = run_git_command(["git", "commit", "-m", commit_message])
        if code != 0:
            raise Exception(err)
        print(f"✅ Commit créé : {commit_message}")

        # Pousser sur GitHub
        code, out, err = run_git_command(["git", "push", "origin", "main"])
        if code != 0:
            raise Exception(err)
        print("✅ Dépôt mis à jour sur GitHub avec succès !")

    except Exception as e:
        print(f"❌ Erreur : {e}")

input("\nAppuie sur Entrée pour fermer...")
