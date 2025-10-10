#!/usr/bin/env python3
"""
Script de démarrage simple du dashboard
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("🌍 Dashboard Environnemental Madagascar")
    print("=" * 50)
    
    print("🚀 Démarrage du serveur backend...")
    print("🌐 Le dashboard sera accessible à l'adresse: http://localhost:5000")
    print("📱 Ouvrez le fichier frontend/index.html dans votre navigateur")
    print("\n🛑 Appuyez sur Ctrl+C pour arrêter le serveur")
    
    # Démarrer le serveur simplifié
    try:
        subprocess.run([sys.executable, "simple_app.py"], cwd="backend")
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du dashboard")

if __name__ == "__main__":
    main()
