import subprocess
import os

def git_command(command):
    """
    Exécute une commande Git et affiche la sortie.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: {e}")

def add_all_files_to_git(directory):
    """
    Ajoute tous les fichiers d'un répertoire spécifique à l'index Git (staging).
    """
    if os.path.exists(directory):
        # Change le répertoire de travail actuel pour le répertoire spécifié
        os.chdir(directory)
        git_command(["git", "add", "."])  # Ajoute tous les fichiers dans le répertoire
        print(f"Tous les fichiers dans {directory} ont été ajoutés.")
        return True  # Indique que l'ajout a réussi
    else:
        print(f"Le répertoire {directory} n'existe pas.")
        return False  # Indique que l'ajout a échoué

def commit_changes(message):
    """
    Valide les changements dans le dépôt local avec un message de commit.
    """
    try:
        git_command(["git", "commit", "-m", message])
        print(f"Commit réalisé avec le message : {message}")
    except Exception as e:
        print(f"Erreur lors de la validation des changements : {e}")

def push_changes(branch="main"):
    """
    Pousse les changements vers la branche spécifiée sur GitHub.
    """
    try:
        git_command(["git", "push", "origin", branch])
        print(f"Les changements ont été poussés vers la branche {branch}.")
    except Exception as e:
        print(f"Erreur lors du push des changements : {e}")
        print("Assurez-vous que vous êtes connecté à GitHub et que la branche existe.")

if __name__ == "__main__":
    # Spécifiez le répertoire à mettre à jour
    dossier_a_mettre_a_jour = r"C:\Users\Win 11\Documents\filter"  # Mettez à jour ce chemin

    # Message de commit
    message_commit = "Mise à jour des fichiers dans le dossier filter"

    # Ajouter tous les fichiers à Git
    if add_all_files_to_git(dossier_a_mettre_a_jour):
        # Valider les changements
        commit_changes(message_commit)

        # Pousser vers GitHub (branch par défaut 'main')
        push_changes("main")
