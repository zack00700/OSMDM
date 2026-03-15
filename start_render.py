#!/usr/bin/env python3
"""
O.S MDM V2.1 — Démarrage pour Render.com
Render n'expose qu'un seul port ($PORT).
On lance le backend en thread et le frontend proxy sur $PORT.
"""
import subprocess, sys, os, time, signal, secrets, threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── AUTO-GÉNÉRATION DU SECRET ────────────────────
if not os.environ.get('MDM_SECRET'):
    # En production Render, MDM_SECRET doit être dans les Environment Variables
    # Si absent, on en génère un (mais les sessions seront perdues au redéploiement)
    os.environ['MDM_SECRET'] = secrets.token_hex(32)
    print("⚠️  MDM_SECRET non défini — généré automatiquement")
    print("   Ajoutez MDM_SECRET dans Render > Environment Variables pour la persistance")

# Port Render (défaut 10000)
PORT = int(os.environ.get('PORT', 10000))

def run_backend():
    """Lance le backend Flask en thread"""
    os.environ['MDM_BACKEND_PORT'] = '5001'
    subprocess.run([sys.executable, os.path.join(BASE_DIR, 'backend', 'app.py')])

# Lancer le backend en thread
backend_thread = threading.Thread(target=run_backend, daemon=True)
backend_thread.start()

# Attendre que le backend démarre
print("🚀  Démarrage backend (port 5001)...")
time.sleep(3)

# Lancer le frontend proxy sur le port Render
print(f"🌐  Démarrage frontend (port {PORT})...")
os.environ['FRONTEND_PORT'] = str(PORT)

# Modifier le port du frontend
from frontend.server import app as frontend_app
frontend_app.run(host='0.0.0.0', port=PORT, debug=False)
