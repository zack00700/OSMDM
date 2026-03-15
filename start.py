#!/usr/bin/env python3
"""O.S MDM V2.1 — Script de démarrage unique"""
import subprocess, sys, os, time, signal, secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, '.env')
processes = []

# ── AUTO-GÉNÉRATION DU SECRET ────────────────────────
# Si MDM_SECRET n'est pas dans l'environnement, on le charge ou le crée
if not os.environ.get('MDM_SECRET'):
    # Essayer de charger depuis .env
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())
    # Si toujours pas de secret, en générer un et le sauvegarder
    if not os.environ.get('MDM_SECRET'):
        new_secret = secrets.token_hex(32)
        os.environ['MDM_SECRET'] = new_secret
        # Sauvegarder dans .env pour les prochains lancements
        existing_lines = []
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, 'r') as f:
                existing_lines = f.readlines()
        # Vérifier si MDM_SECRET existe déjà dans le fichier
        has_secret = any(l.strip().startswith('MDM_SECRET=') for l in existing_lines)
        if not has_secret:
            with open(ENV_FILE, 'a') as f:
                if existing_lines and not existing_lines[-1].endswith('\n'):
                    f.write('\n')
                f.write(f'MDM_SECRET={new_secret}\n')
            print(f"🔑  Secret JWT généré et sauvegardé dans .env")
        else:
            print(f"🔑  Secret JWT généré pour cette session")

def stop_all(sig=None, frame=None):
    print("\n🛑  Arrêt de O.S MDM...")
    for p in processes:
        try: p.terminate()
        except: pass
    sys.exit(0)

signal.signal(signal.SIGINT,  stop_all)
signal.signal(signal.SIGTERM, stop_all)

print("=" * 55)
print("   O.S MDM V2.1 — OpenSID Master Data Management")
print("=" * 55)

print("\n📦  Installation des dépendances...")
subprocess.run([sys.executable, '-m', 'pip', 'install', '-r',
    os.path.join(BASE_DIR, 'requirements.txt'),
    '--break-system-packages', '-q'], check=False)

# Passer l'environnement complet aux sous-processus
env = os.environ.copy()

print("🚀  Démarrage backend  (port 5001)...")
processes.append(subprocess.Popen(
    [sys.executable, os.path.join(BASE_DIR, 'backend', 'app.py')], env=env))
time.sleep(2)

print("🌐  Démarrage frontend (port 3000)...")
processes.append(subprocess.Popen(
    [sys.executable, os.path.join(BASE_DIR, 'frontend', 'server.py')], env=env))
time.sleep(1)

print("\n" + "=" * 55)
print("✅  O.S MDM V2.1 est démarrée !")
print("=" * 55)
print("\n  🌐  Interface  →  http://127.0.0.1:3000")
print("  🔌  API        →  http://127.0.0.1:5001/api")
print("  ❤️  Health     →  http://127.0.0.1:5001/api/health")
print("\n  ─────────────────────────────────────────")
print("  Appuyez sur Ctrl+C pour arrêter\n")

try:
    processes[0].wait()
except KeyboardInterrupt:
    stop_all()
