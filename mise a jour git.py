import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

REMOTE_URL = "https://github.com/HOMEassistante/filter.git"

# --- Fonction pour exécuter une commande Git et afficher la sortie en direct ---
def executer(cmd, console):
    """Exécute une commande shell et affiche la sortie dans la console Tkinter."""
    console.insert(tk.END, f"\n> {cmd}\n", "cmd")
    console.see(tk.END)

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for ligne in iter(process.stdout.readline, ''):
        console.insert(tk.END, ligne)
        console.see(tk.END)
        console.update()

    process.wait()
    if process.returncode != 0:
        console.insert(tk.END, f"\n⚠️ Erreur lors de l'exécution : {cmd}\n", "error")
        console.see(tk.END)
        raise subprocess.CalledProcessError(process.returncode, cmd)

# --- Obtenir la liste des fichiers modifiés ---
def fichiers_modifies():
    try:
        sortie = subprocess.check_output("git status --porcelain", shell=True).decode().strip()
        if not sortie:
            return []
        lignes = sortie.splitlines()
        fichiers = []
        for ligne in lignes:
            statut, fichier = ligne[:2].strip(), ligne[3:]
            fichiers.append((statut or "?", fichier))
        return fichiers
    except subprocess.CalledProcessError:
        return []

# --- Processus complet de mise à jour Git ---
def maj_github(selection, message, console, bouton):
    if not selection:
        messagebox.showwarning("Attention", "Aucun fichier sélectionné.")
        return

    bouton.config(state="disabled")
    console.insert(tk.END, "\n🚀 Démarrage de la mise à jour GitHub...\n\n", "info")
    console.update()

    def tache():
        try:
            # Ajout des fichiers
            for fichier in selection:
                executer(f'git add "{fichier}"', console)

            # Commit
            executer(f'git commit -m "{message}"', console)

            # Pull + Push
            executer("git pull --rebase origin main || git pull --rebase origin master", console)
            executer("git push origin main || git push origin master", console)

            console.insert(tk.END, "\n✅ Mise à jour réussie !\n", "success")
            messagebox.showinfo("Succès", "Mise à jour GitHub terminée !")

        except Exception as e:
            console.insert(tk.END, f"\n❌ Erreur : {e}\n", "error")
            messagebox.showerror("Erreur", str(e))
        finally:
            bouton.config(state="normal")

    # Exécuter dans un thread pour ne pas bloquer l’interface
    threading.Thread(target=tache).start()

# --- Interface graphique principale ---
def interface_github():
    fenetre = tk.Tk()
    fenetre.title("GitHub Updater - HOMEassistante/filter")
    fenetre.geometry("800x600")

    tk.Label(fenetre, text="Sélectionne les fichiers à ajouter :", font=("Arial", 12, "bold")).pack(pady=10)

    fichiers = fichiers_modifies()
    if not fichiers:
        tk.Label(fenetre, text="Aucun fichier modifié ou non suivi.").pack(pady=10)
        fenetre.mainloop()
        return

    cadre = tk.Frame(fenetre)
    cadre.pack(fill=tk.BOTH, expand=False)

    liste_cases = []
    for statut, fichier in fichiers:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(cadre, text=f"[{statut}] {fichier}", variable=var, anchor="w")
        chk.pack(fill="x", padx=20)
        liste_cases.append((var, fichier))

    # Champ de message de commit
    tk.Label(fenetre, text="\nMessage du commit :").pack()
    champ_message = tk.Entry(fenetre, width=80)
    champ_message.insert(0, "Mise à jour automatique")
    champ_message.pack(pady=5)

    # Console de sortie Git
    tk.Label(fenetre, text="\nConsole Git :", font=("Arial", 11, "bold")).pack()
    console = scrolledtext.ScrolledText(fenetre, height=18, width=95, bg="#1E1E1E", fg="#FFFFFF", insertbackground="white")
    console.pack(padx=10, pady=5)
    console.tag_config("cmd", foreground="#00FF00")
    console.tag_config("info", foreground="#00BFFF")
    console.tag_config("error", foreground="#FF5555")
    console.tag_config("success", foreground="#00FF88")

    # Bouton principal
    def lancer_mise_a_jour():
        selection = [f for var, f in liste_cases if var.get()]
        message = champ_message.get().strip() or "Mise à jour automatique"
        maj_github(selection, message, console, bouton_envoyer)

    bouton_envoyer = tk.Button(fenetre, text="📤 Envoyer sur GitHub", command=lancer_mise_a_jour,
                               bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
    bouton_envoyer.pack(pady=15)

    fenetre.mainloop()

# --- Vérification du dépôt Git ---
def main():
    if not os.path.exists(".git"):
        messagebox.showerror("Erreur", "Ce dossier n'est pas un dépôt Git.\nExécute : git init && git remote add origin ...")
        sys.exit(1)

    try:
        remotes = subprocess.check_output("git remote -v", shell=True).decode()
        if "origin" not in remotes:
            executer(f"git remote add origin {REMOTE_URL}", None)
    except Exception:
        executer(f"git remote add origin {REMOTE_URL}", None)

    interface_github()

if __name__ == "__main__":
    main()
