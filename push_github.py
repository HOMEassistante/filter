import subprocess
import sys
import os
import re

# ==== Fonctions utilitaires ====
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
        if e.stderr:
            print(e.stderr)
        sys.exit(1)

def print_colored(text, color_code):
    """Affiche du texte coloré dans la console."""
    print(f"\033[{color_code}m{text}\033[0m")

# ==== 1️⃣ Affiche le statut du dépôt ====
print_colored("\n=== Statut du dépôt ===", "1;34")
print(run_git_command(["status"]))

# ==== 2️⃣ Affiche les 10 derniers commits ====
print_colored("\n=== 10 derniers commits ===", "1;34")
print(run_git_command(["log", "--oneline", "-10"]))

# ==== 3️⃣ Affiche les fichiers modifiés ====
print_colored("\n=== Différences et fichiers modifiés ===", "1;34")
print(run_git_command(["diff", "--stat"]))

# ==== 4️⃣ Affiche les fichiers ajoutés ou supprimés ====
print_colored("\n=== Fichiers ajoutés ou supprimés ===", "1;34")
diff_name_status = run_git_command(["diff", "--name-status"])
for line in diff_name_status.splitlines():
    if line.startswith("A"):
        print_colored(line, "32")  # vert
    elif line.startswith("D"):
        print_colored(line, "31")  # rouge
    else:
        print(line)  # modifié ou autre

# ==== 5️⃣ Détection automatique des fichiers secrets ====
print_colored("\n=== Détection automatique des fichiers secrets ===", "1;34")

# Fichiers sensibles typiques
secret_patterns = [r".*\.env", r".*token.*\.txt", r".*\.pem", r".*\.key"]
all_files = run_git_command(["ls-files"]).splitlines()

secret_files = []
for f in all_files:
    for pattern in secret_patterns:
        if re.match(pattern, f, re.IGNORECASE):
            secret_files.append(f)

if secret_files:
    print_colored(f"Fichiers secrets détectés : {', '.join(secret_files)}", "31")
else:
    print_colored("Aucun fichier secret détecté automatiquement.", "33")  # jaune

# ==== 6️⃣ Supprimer les fichiers secrets de l'historique ====
if secret_files:
    try:
        args = [sys.executable, "-m", "git_filter_repo", "--force"]
        for f in secret_files:
            args += [f"--path", f, "--invert-paths"]
        subprocess.run(args, check=True)
        print_colored("Fichiers secrets supprimés de l'historique.", "32")
    except subprocess.CalledProcessError as e:
        print("Erreur lors de la suppression des fichiers secrets :", e)
        sys.exit(1)

# ==== 7️⃣ Créer/mettre à jour .gitignore pour ignorer les fichiers secrets ====
gitignore_path = ".gitignore"
with open(gitignore_path, "a") as f:
    for file in secret_files:
        f.write(f"{file}\n")

run_git_command(["add", ".gitignore"])
run_git_command(["commit", "-m", "Ajout de .gitignore pour ignorer les fichiers secrets"])

# ==== 8️⃣ Commit tous les changements restants ====
run_git_command(["add", "."])
try:
    run_git_command(["commit", "-m", "Nettoyage des fichiers secrets"])
except SystemExit:
    print_colored("Aucun changement à committer.", "33")

# ==== 9️⃣ Push sur GitHub avec force ====
print_colored("\n=== Push vers GitHub ===", "1;34")
try:
    run_git_command(["push", "origin", "main", "--force"])
    print_colored("Push terminé avec succès.", "32")
except SystemExit:
    print_colored("Erreur lors du push. Vérifie ton dépôt distant.", "31")

# ==== 🔟 Afficher le statut final ====
print_colored("\n=== Statut final du dépôt ===", "1;34")
print(run_git_command(["status"]))

# ==== 1️⃣1️⃣ Laisser la fenêtre ouverte ====
input("\nAppuie sur Entrée pour fermer la fenêtre...")
