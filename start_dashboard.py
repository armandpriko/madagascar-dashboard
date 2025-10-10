#!/usr/bin/env python3
"""
Script de démarrage du dashboard
Lance le serveur backend et ouvre le frontend
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import threading

def start_backend():
    """Démarrer le serveur Flask backend"""
    print("🚀 Démarrage du serveur backend...")
    backend_dir = Path("backend")
    os.chdir(backend_dir)
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur backend")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du backend: {e}")

def open_frontend():
    """Ouvrir le frontend dans le navigateur"""
    time.sleep(3)  # Attendre que le serveur démarre
    frontend_path = Path("../frontend/index.html").resolve()
    webbrowser.open(f"file://{frontend_path}")
    print("🌐 Frontend ouvert dans le navigateur")

def main():
    print("🌍 Dashboard Environnemental Madagascar")
    print("=" * 50)
    
    # Vérifier que les données existent
    data_file = Path("backend/data/dashboard_data.json")
    if not data_file.exists():
        print("📊 Génération des données...")
        subprocess.run([sys.executable, "generate_data.py"], check=True)
    
    # Démarrer le backend dans un thread séparé
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Ouvrir le frontend
    frontend_thread = threading.Thread(target=open_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    try:
        # Attendre indéfiniment
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du dashboard")
        sys.exit(0)

if __name__ == "__main__":
    main()
