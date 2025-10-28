import os
import subprocess
from dotenv import load_dotenv

# === Charger les variables du fichier .env ===
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

# === Configuration ===
repo_path = r"C:\Depot git"
commit_message = "Mise à jour automatique"
remote_url = "https://github.com/HOMEassistante/filter.git"
branch_name = "main"  # ou "master" selon ton dépôt

def push_to_github():
    if not github_token:
        print("❌ Erreur : le token GitHub n'est pas défini dans le fichier .env")
        return

    os.chdir(repo_path)

    print("🔄 Configuration du dépôt distant...")
    subprocess.run(["git", "init"], check=False)
    subprocess.run(["git", "remote", "remove", "origin"], check=False)
    subprocess.run([
        "git", "remote", "add", "origin",
        f"https://{github_token}@github.com/HOMEassistante/filter.git"
    ], check=True)

    print("📁 Ajout des fichiers...")
    subprocess.run(["git", "add", "."], check=True)

    print("💬 Création du commit...")
    subprocess.run(["git", "commit", "-m", commit_message], check=False)

    print("🚀 Envoi vers GitHub...")
    subprocess.run(["git", "branch", "-M", branch_name], check=False)
    subprocess.run(["git", "push", "-u", "origin", branch_name, "--force"], check=True)

    print("✅ Dépôt mis à jour avec succès !")

if __name__ == "__main__":
    push_to_github()
