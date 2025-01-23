import os
import requests
import sys
import subprocess

# URL du fichier exécutable hébergé sur GitHub
EXE_URL = 'https://raw.githubusercontent.com/votre-utilisateur/client-update/main/client.exe'
# Nom local du fichier exécutable
LOCAL_EXE = 'client.exe'
# URL du fichier de version sur GitHub
VERSION_URL = 'https://raw.githubusercontent.com/votre-utilisateur/client-update/main/version.txt'

def get_remote_version():
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de la version distante: {e}")
        return None

def get_local_version():
    if os.path.exists("version.txt"):
        with open("version.txt", "r") as f:
            return f.read().strip()
    return None

def update_executable():
    try:
        response = requests.get(EXE_URL, stream=True)
        response.raise_for_status()
        with open(LOCAL_EXE, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Exécutable mis à jour avec succès.")
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de l'exécutable: {e}")

def check_for_updates():
    remote_version = get_remote_version()
    local_version = get_local_version()
    
    if remote_version and remote_version != local_version:
        print("Nouvelle version disponible. Mise à jour en cours...")
        update_executable()
        with open("version.txt", "w") as f:
            f.write(remote_version)
        print("Redémarrage de l'exécutable mis à jour...")
        subprocess.Popen([LOCAL_EXE])
        sys.exit()
    else:
        print("Vous avez déjà la dernière version de l'exécutable.")

if __name__ == "__main__":
    check_for_updates()
    # Lancer l'exécutable
    if os.path.exists(LOCAL_EXE):
        subprocess.Popen([LOCAL_EXE])
