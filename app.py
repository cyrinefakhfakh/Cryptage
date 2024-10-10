import tkinter as tk
from tkinter import messagebox, simpledialog

# Dictionnaire des utilisateurs et mots de passe (incluant l'admin)
users = {
    "admin": "adminpassword",  # Profil administrateur
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

# Fonction de chiffrement/déchiffrement par le code de César
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) + shift - shift_base) % 26 + shift_base)
        else:
            result += char
    return result

# Validation des entrées utilisateur
def validate_input():
    text = entry_text.get()
    if not text:
        messagebox.showerror("Erreur", "Le texte ne doit pas être vide.")
        return False
    if len(text) > 256:
        messagebox.showerror("Erreur", "Le texte est trop long (max 256 caractères).")
        return False
    try:
        shift = int(entry_shift.get())
    except ValueError:
        messagebox.showerror("Erreur", "Le décalage doit être un entier.")
        return False
    return True

# Fonction de chiffrement
def encrypt():
    if validate_input():
        text = entry_text.get()
        shift = int(entry_shift.get())
        encrypted_text = caesar_cipher(text, shift)
        messagebox.showinfo("Chiffré", f"Texte chiffré : {encrypted_text}")

# Fonction de déchiffrement
def decrypt():
    if validate_input():
        text = entry_text.get()
        shift = int(entry_shift.get())
        decrypted_text = caesar_cipher(text, -shift)
        messagebox.showinfo("Déchiffré", f"Texte déchiffré : {decrypted_text}")

# Fonction pour effacer le texte et le décalage
def clear_entries():
    entry_text.delete(0, tk.END)
    entry_shift.delete(0, tk.END)

# Fonction de gestion des utilisateurs (ajout/suppression)
def manage_users():
    if logged_in_user != "admin":
        messagebox.showerror("Erreur", "Seul l'administrateur peut gérer les utilisateurs.")
        return

    action = simpledialog.askstring("Action Admin", "Voulez-vous ajouter ou supprimer un utilisateur ? (ajouter/supprimer)")
    
    if action == "ajouter":
        new_user = simpledialog.askstring("Ajouter utilisateur", "Entrez le nouveau nom d'utilisateur :")
        new_pass = simpledialog.askstring("Ajouter mot de passe", "Entrez le mot de passe :")
        if new_user and new_pass:
            users[new_user] = new_pass
            messagebox.showinfo("Succès", f"Utilisateur {new_user} ajouté avec succès !")
    elif action == "supprimer":
        del_user = simpledialog.askstring("Supprimer utilisateur", "Entrez le nom d'utilisateur à supprimer :")
        if del_user in users:
            del users[del_user]
            messagebox.showinfo("Succès", f"Utilisateur {del_user} supprimé avec succès !")
        else:
            messagebox.showerror("Erreur", f"Utilisateur {del_user} introuvable.")

# Fonction de connexion
def login():
    global logged_in_user
    username = entry_username.get()
    password = entry_password.get()
    
    if username in users and users[username] == password:
        logged_in_user = username
        messagebox.showinfo("Succès", "Connexion réussie !")
        login_window.destroy()  # Ferme la fenêtre de connexion
        open_main_window()  # Ouvre la fenêtre principale
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

# Ouvre la fenêtre principale après connexion
def open_main_window():
    global entry_text, entry_shift, button_encrypt, button_decrypt

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Code de César")
    root.configure(bg="#f0f0f0")  # Couleur de fond
    root.resizable(False, False)  # Empêche de redimensionner la fenêtre

    # Validation des nombres uniquement dans le champ du décalage
    vcmd = (root.register(only_numbers), '%S')

    # Création des widgets
    label_text = tk.Label(root, text="Texte à chiffrer/déchiffrer:", bg="#f0f0f0")
    label_text.pack(pady=10)

    entry_text = tk.Entry(root, width=50)
    entry_text.pack(pady=5)

    label_shift = tk.Label(root, text="Décalage:", bg="#f0f0f0")
    label_shift.pack(pady=10)

    entry_shift = tk.Entry(root, width=5, validate="key", validatecommand=vcmd)
    entry_shift.pack(pady=5)

    button_encrypt = tk.Button(root, text="Chiffrer", command=encrypt, state=tk.DISABLED, bg="#075e95", fg="white")
    button_encrypt.pack(pady=5)

    button_decrypt = tk.Button(root, text="Déchiffrer", command=decrypt, state=tk.DISABLED, bg="#075e95", fg="white")
    button_decrypt.pack(pady=5)

    button_clear = tk.Button(root, text="Effacer", command=clear_entries, bg="#075e95", fg="white")
    button_clear.pack(pady=5)

    if logged_in_user == "admin":
        button_manage_users = tk.Button(root, text="Gérer les utilisateurs", command=manage_users, bg="#075e95", fg="white")
        button_manage_users.pack(pady=10)

    # Lier les événements de saisie à la vérification des entrées
    entry_text.bind("<KeyRelease>", check_valid_inputs)
    entry_shift.bind("<KeyRelease>", check_valid_inputs)

    # Boucle principale
    root.mainloop()

# Activation/Désactivation des boutons selon les entrées
def check_valid_inputs(*args):
    if entry_text.get() and entry_shift.get().isdigit():
        button_encrypt.config(state=tk.NORMAL)
        button_decrypt.config(state=tk.NORMAL)
    else:
        button_encrypt.config(state=tk.DISABLED)
        button_decrypt.config(state=tk.DISABLED)

# Limiter les chiffres uniquement dans l'entrée du décalage
def only_numbers(char):
    return char.isdigit()

# Fenêtre de connexion
logged_in_user = None

login_window = tk.Tk()
login_window.title("Connexion")
login_window.geometry("400x300")
login_window.configure(bg="#E0E0E0")

# Widgets de la fenêtre de connexion
label_username = tk.Label(login_window, text="Nom d'utilisateur:", bg="#E0E0E0")
label_username.pack(pady=5)

entry_username = tk.Entry(login_window, width=30)
entry_username.pack(pady=5)

label_password = tk.Label(login_window, text="Mot de passe:", bg="#E0E0E0")
label_password.pack(pady=5)

entry_password = tk.Entry(login_window, show="*", width=30)
entry_password.pack(pady=5)

button_login = tk.Button(login_window, text="Se connecter", command=login, bg="#075e95", fg="white")
button_login.pack(pady=10)

# Boucle principale de la fenêtre de connexion
login_window.mainloop()

