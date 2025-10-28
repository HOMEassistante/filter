import subprocess
import sys
import os
import re

# ==== Fonctions utilitaires ====
def run_git_command(cmd, capture_output=True, exit_on_error=False):
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
        print(f"\n❌ Erreur lors de la commande: git {' '.join(cmd)}")
        if e.stderr:
            print(e.stderr.strip())
        if exit_on_error:
            sys.exit(1)
        return ""  # continue au lieu de quitter

def print_colored(text, color_code):
    """Affiche du texte coloré dans la console."""
    print(f"\033[{color_code}m{text}\033[0m")

def safe_input(msg):
    """Empêche la fermeture immédiate de la fenêtre."""
    try:
        input(msg)
    except EOFError:
        pass

# ==== Début du script ====
print_colored("\n=== Analyse du dépôt Git ===", "1;34")

# Vérifie que c’est bien un dépôt Git
if not os.path.exists(".git"):
    print_colored("⚠️  Ce dossier n'est pas un dépôt Git !", "31")
    safe_input("\nAppuie sur Entrée pour fermer la fenêtre...")
    sys.exit(0)

# ==== 1️⃣ Statut du dépôt ====
print_colored("\n=== Statut du dépôt ===", "1;34")
print(run_git_command(["status"]))

# ==== 2️⃣ Derniers commits ====
print_colored("\n=== 10 derniers commits ===", "1;34")
print(run_git_command(["log", "--oneline", "-10"]))

# ==== 3️⃣ Fichiers modifiés ====
print_colored("\n=== Fichiers modifiés ===", "1;34")
print(run_git_command(["diff", "--stat"]))

# ==== 4️⃣ Fichiers ajoutés ou supprimés ====
print_colored("\n=== Fichiers ajoutés ou supprimés ===", "1;34")
diff_name_status = run_git_command(["diff", "--name-status"])
for line in diff_name_status.splitlines():
    if line.startswith("A"):
        print_colored(line, "32")
    elif line.startswith("D"):
        print_colored(line, "31")
    else:
        print(line)

# ==== 5️⃣ Détection automatique des fichiers secrets ====
print_colored("\n=== Détection automatique des fichiers secrets ===", "1;34")
secret_patterns = [r".*\.env", r".*token.*\.txt", r".*\.pem", r".*\.key"]
all_files = run_git_command(["ls-files"]).splitlines()

secret_files = []
for f in all_files:
    for pattern in secret_patterns:
        if re.match(pattern, f, re.IGNORECASE):
            secret_files.append(f)

if secret_files:
    print_colored(f"🚨 Fichiers secrets détectés : {', '.join(secret_files)}", "31")
else:
    print_colored("✅ Aucun fichier secret détecté.", "32")

# ==== 6️⃣ Suppression des fichiers secrets ====
if secret_files:
    print_colored("\nSuppression de l’historique des fichiers secrets...", "33")
    args = [sys.executable, "-m", "git_filter_repo", "--force"]
    for f in secret_files:
        args += ["--path", f, "--invert-paths"]

    try:
        subprocess.run(args, check=True)
        print_colored("✅ Fichiers secrets supprimés de l’historique.", "32")
    except subprocess.CalledProcessError as e:
        print_colored("❌ Erreur lors de la suppression des fichiers secrets.", "31")
        print(str(e))

# ==== 7️⃣ Ajout dans .gitignore (local seulement) ====
if secret_files:
    gitignore_path = ".gitignore"

    # Écriture ou mise à jour du .gitignore
    with open(gitignore_path, "a", encoding="utf-8") as f:
        for file in secret_files:
            f.write(f"{file}\n")

    # Empêche .gitignore d’être suivi par Git
    run_git_command(["rm", "--cached", ".gitignore"], exit_on_error=False)
    print_colored("📄 .gitignore mis à jour localement (non suivi sur GitHub).", "33")

# ==== 8️⃣ Commit du reste ====
run_git_command(["add", "."], exit_on_error=False)
output = run_git_command(["commit", "-m", "Nettoyage des fichiers secrets"], exit_on_error=False)
if not output.strip():
    print_colored("⚠️ Aucun changement à committer.", "33")

# ==== 9️⃣ Push GitHub ====
print_colored("\n=== Push vers GitHub ===", "1;34")
output = run_git_command(["push", "origin", "main", "--force"], exit_on_error=False)
if "rejected" in output or "error" in output.lower():
    print_colored("⚠️ Push refusé. Vérifie les règles du dépôt distant.", "31")
else:
    print_colored("✅ Push terminé avec succès.", "32")

# ==== 🔟 Statut final ====
print_colored("\n=== Statut final du dépôt ===", "1;34")
print(run_git_command(["status"]))



# ==== 1️⃣2️⃣ Suppression de .gitignore du dépôt en ligne ====
if os.path.exists(".gitignore"):
    print_colored("\n=== Suppression de .gitignore du dépôt distant ===", "1;34")
    run_git_command(["rm", "--cached", ".gitignore"], exit_on_error=False)
    run_git_command(["commit", "-m", "Retrait de .gitignore du dépôt"], exit_on_error=False)
    output = run_git_command(["push", "origin", "main", "--force"], exit_on_error=False)

    if "rejected" in output or "error" in output.lower():
        print_colored("⚠️ Erreur lors du retrait de .gitignore en ligne.", "31")
    else:
        print_colored("✅ .gitignore retiré du dépôt GitHub avec succès.", "32")
else:
    print_colored("ℹ️ Aucun fichier .gitignore à retirer.", "33")



safe_input("\nAppuie sur Entrée pour fermer la fenêtre...")
