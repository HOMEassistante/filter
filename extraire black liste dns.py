# script_extraction_gui.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Fonction principale
def extraire_et_afficher():
    # Choix du fichier source
    source_file = filedialog.askopenfilename(
        title="Choisir le fichier source",
        filetypes=[("Fichier texte ou raw", "*.txt *.raw")]
    )
    if not source_file:
        return

    # Lecture du fichier source
    with open(source_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Balises
    start_black = "## Blacklisted Entries! ##"
    end_black = "## Whitelisted Entries! ##"

    try:
        start_index = content.index(start_black) + len(start_black)
        end_index = content.index(end_black)
        blacklist_content = content[start_index:end_index].strip()
        whitelist_content = content[end_index + len(end_black):].strip()
    except ValueError:
        messagebox.showerror("Erreur", "Les balises ## Blacklisted Entries! ## ou ## Whitelisted Entries! ## sont introuvables.")
        return

    # Création de la fenêtre graphique
    root = tk.Tk()
    root.title("Contenu Blacklist / Whitelist")
    root.geometry("800x600")

    # Zone de texte pour Blacklist
    tk.Label(root, text="Blacklist", font=("Arial", 12, "bold")).pack()
    txt_black = scrolledtext.ScrolledText(root, width=100, height=15)
    txt_black.pack()
    txt_black.insert(tk.END, blacklist_content)

    # Zone de texte pour Whitelist
    tk.Label(root, text="Whitelist", font=("Arial", 12, "bold")).pack()
    txt_white = scrolledtext.ScrolledText(root, width=100, height=15)
    txt_white.pack()
    txt_white.insert(tk.END, whitelist_content)

    # Fonction pour sauvegarder
    def sauvegarder():
        default_dir = os.path.dirname(source_file)

        # Blacklist
        black_file = filedialog.asksaveasfilename(
            title="Enregistrer Blacklist",
            initialdir=default_dir,
            initialfile="blacklist",
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt"), ("Fichier brut", "*.raw")]
        )
        if black_file:
            with open(black_file, "w", encoding="utf-8") as f:
                f.write(blacklist_content)

        # Whitelist
        white_file = filedialog.asksaveasfilename(
            title="Enregistrer Whitelist",
            initialdir=default_dir,
            initialfile="whitelist",
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt"), ("Fichier brut", "*.raw")]
        )
        if white_file:
            with open(white_file, "w", encoding="utf-8") as f:
                f.write(whitelist_content)

        messagebox.showinfo("Succès", "Fichiers sauvegardés !")

    # Bouton pour sauvegarder
    tk.Button(root, text="Sauvegarder les fichiers", command=sauvegarder, bg="green", fg="white").pack(pady=10)

    root.mainloop()

# Lancer le script
if __name__ == "__main__":
    extraire_et_afficher()
