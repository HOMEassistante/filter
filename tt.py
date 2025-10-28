import os
import subprocess
import sys
import shutil

# -----------------------------
# Fonctions utilitaires
# -----------------------------
def run_git_command(cmd, capture_output=True):
    """Exécute une commande Git et retourne sa sortie."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            capture_output=capture_output,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: git {' '.join(cmd)}")
        print(e.stderr)
        sys.exit(1)

def print_colored(text, color_code):
    """Affiche du texte coloré dans la console."""
    print(f"\033[{color_code}m{text}\033[0m")

# -----------------------------
# Étape 1 : Vérifier dépôt
# -----------------------------
print_colored("\n=== Statut du dépôt avant opérations ===", "1;34")
status = run_git_command(["status"])
print(status)

# -----------------------------
# Étape 2 : Créer .gitignore
# -----------------------------
gitignore_content = ".env\ntoken win 11.txt\n"
with open(".gitignore", "w") as f:
    f.write(gitignore_content)
print_colored("\n.gitignore créé pour ignorer les fichiers secrets.", "32")

# -----------------------------
# Étape 3 : Récréer les fichiers secrets locaux
# -----------------------------
secrets = {
    ".env": "VOTRE_CONTENU_SECRET_ENV\n",
    "token win 11.txt": "VOTRE_TOKEN_SECRET\n"
}

for path, content in secrets.items():
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)
        print_colored(f"Fichier secret recréé localement : {path}", "32")
    else:
        print_colored(f"Fichier déjà présent localement : {path}", "33")

# -----------------------------
# Étape 4 : Afficher les changements
# -----------------------------
print_colored("\n=== Différences locales après ajout de secrets ===", "1;34")
diff_stat = run_git_command(["diff", "--stat"])
print(diff_stat)

print_colored("\n=== Fichiers locaux ajoutés ou supprimés ===", "1;34")
diff_name_status = run_git_command(["diff", "--name-status"])
for line in diff_name_status.splitlines():
    if line.startswith("A"):
        print_colored(line, "32")  # vert = ajouté
    elif line.startswith("D"):
        print_colored(line, "31")  # rouge = supprimé
    else:
        print(line)  # modifié ou autre

# -----------------------------
# Étape 5 : Afficher derniers commits
# -----------------------------
print_colored("\n=== 10 derniers commits ===", "1;34")
log = run_git_command(["log", "--oneline", "-10"])
print(log)

# -----------------------------
# Étape 6 : Laisser la fenêtre ouverte
# -----------------------------
input("\nAppuie sur Entrée pour fermer la fenêtre...")
