# script_diff_2fenetres_v2.py
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

def afficher_diff_fichiers():
    # Choisir le fichier source
    source_file = filedialog.askopenfilename(
        title="Choisir le fichier source",
        filetypes=[("Fichier texte ou raw", "*.txt *.raw")]
    )
    if not source_file:
        return

    # Choisir le fichier à ajouter
    ajout_file = filedialog.askopenfilename(
        title="Choisir le fichier à ajouter",
        filetypes=[("Fichier texte ou raw", "*.txt *.raw")]
    )
    if not ajout_file:
        return

    # Lire les fichiers
    with open(source_file, "r", encoding="utf-8") as f:
        lignes_source = f.read().splitlines()
    with open(ajout_file, "r", encoding="utf-8") as f:
        lignes_ajout = f.read().splitlines()

    # Trouver uniquement les lignes nouvelles (pas déjà dans le fichier source)
    lignes_nouvelles = [ligne for ligne in lignes_ajout if ligne not in lignes_source]

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Visualisation fichiers source et ajout sans doublons")

    # Taille initiale plus compacte
    root.geometry("900x600")

    # Fenêtre pour le fichier source
    tk.Label(root, text=f"Contenu du fichier source : {os.path.basename(source_file)}", 
             font=("Arial", 12, "bold")).pack(pady=(10, 0))
    txt_source = scrolledtext.ScrolledText(root, width=120, height=15, bg="#f0f0f0", wrap=tk.NONE)
    txt_source.pack(fill=tk.BOTH, expand=True, padx=10)
    txt_source.insert(tk.END, "\n".join(lignes_source))

    # Fenêtre pour les lignes ajoutées
    tk.Label(root, text=f"Lignes ajoutées depuis : {os.path.basename(ajout_file)}", 
             font=("Arial", 12, "bold")).pack(pady=(10, 0))
    txt_ajout = scrolledtext.ScrolledText(root, width=120, height=15, bg="#e0f7ff", wrap=tk.NONE)
    txt_ajout.pack(fill=tk.BOTH, expand=True, padx=10)
    txt_ajout.insert(tk.END, "\n".join(lignes_nouvelles) if lignes_nouvelles else "Aucune ligne nouvelle à ajouter.")

    # Fonction de sauvegarde du fichier final et fermeture de la fenêtre
    def sauvegarder_final():
        output_file = filedialog.asksaveasfilename(
            title="Enregistrer le fichier combiné",
            initialfile="combined_unique",
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt"), ("Fichier brut", "*.raw")]
        )
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lignes_source + lignes_nouvelles))
            messagebox.showinfo("Succès", f"Fichier combiné enregistré : {output_file}")
            root.destroy()  # <-- ferme la fenêtre principale

    tk.Button(root, text="Sauvegarder le fichier combiné", command=sauvegarder_final, 
              bg="green", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    afficher_diff_fichiers()
