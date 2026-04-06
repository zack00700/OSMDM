# O.S MDM V2.1 — OpenSID Master Data Management

MDM complet avec module maritime et module premium. Import multi-sources, détection doublons (exact + fuzzy), Golden Records, connecteurs API/ERP, write-back, data quality scoring, notifications, webhooks, scheduler.

**Démo en ligne** : [osmdm.onrender.com](https://osmdm.onrender.com)

---

## Démarrage rapide

### Option 1 : Local (développement)
```bash
pip install -r requirements.txt
python3 start.py
```
Ouvrez **http://127.0.0.1:3000**

> `start.py` génère automatiquement un `MDM_SECRET` et le sauvegarde dans `.env` au premier lancement.

### Option 2 : Docker (production on-premise)
```bash
cp .env.example .env
# Éditez .env avec vos valeurs (surtout MDM_SECRET)
docker compose up -d
```

### Option 3 : Render (cloud — recommandé)
1. Créez un **Web Service** sur [render.com](https://render.com)
2. Connectez votre repo GitHub
3. **Build Command** : `pip install -r requirements.txt`
4. **Start Command** : `python start_render.py`
5. Ajoutez les variables d'environnement :

| Variable | Valeur |
|----------|--------|
| `MDM_SECRET` | Cliquez "Generate" |
| `MDM_CORS_ORIGINS` | `*` ou votre URL Render |
| `MDM_PLAN` | `starter`, `business`, ou `enterprise` |

> **Premier lancement** : un compte admin est créé automatiquement.
> - Email : `admin@osmdm.local`
> - Mot de passe : `admin123`
> - **Changez le mot de passe immédiatement** via Mon profil.

---

## CI/CD

Le CI/CD est automatique via **GitHub Actions** :

- **À chaque push** sur `main` : les tests pytest tournent sur Python 3.10, 3.11 et 3.12 + lint syntaxique
- **Déploiement** : Render redéploie automatiquement à chaque push sur `main`

Fichier de config : `.github/workflows/ci.yml`

```
Push → GitHub Actions (tests + lint) → Render (déploiement auto)
```

---

## Plans et licences

L'outil supporte 3 plans configurables via la variable `MDM_PLAN` :

| Plan | Core | Maritime | Premium | Prix indicatif |
|------|:----:|:--------:|:-------:|---------------|
| **Starter** | ✅ | ❌ | ❌ | 990€ / 10 900 DH /mois |
| **Business** | ✅ | ✅ | ❌ | 1 990€ / 21 900 DH /mois |
| **Enterprise** | ✅ | ✅ | ✅ | Sur devis |

Par défaut : `enterprise` (tous les modules activés).

Le plan contrôle l'accès aux modules côté backend (routes bloquées avec 403) et côté frontend (onglets cachés dans la sidebar).

---

## Configuration

Toute la configuration se fait via **variables d'environnement** (voir `.env.example`) :

| Variable | Description | Obligatoire |
|----------|-------------|:-----------:|
| `MDM_SECRET` | Clé secrète JWT (32+ caractères) | **Oui (prod)** |
| `MDM_CORS_ORIGINS` | Origines autorisées (séparées par `,`) | Non |
| `MDM_PLAN` | `starter`, `business`, ou `enterprise` | Non (défaut: enterprise) |
| `MDM_ENCRYPT_KEY` | Clé de chiffrement des credentials DB | Non |
| `MDM_DEBUG` | Mode debug (`true`/`false`) | Non |
| `MDM_DB_ENGINE` | `sqlite` (défaut) ou `postgresql` | Non |
| `MDM_PG_URL` | URL PostgreSQL | Si postgresql |

---

## Structure

```
osmdm/
├── backend/
│   ├── app.py              # API Flask principale (2374 lignes)
│   ├── maritime.py         # Module maritime (1364 lignes)
│   └── premium.py          # Module premium (867 lignes)
├── frontend/
│   ├── server.py           # Proxy Flask (port 3000 local, port $PORT sur Render)
│   ├── static/js/
│   │   ├── app.js          # JS principal (1300+ lignes)
│   │   └── maritime.js     # JS maritime (1089 lignes)
│   └── templates/
│       └── index.html      # Interface HTML complète
├── tests/
│   └── test_api.py         # 52 tests pytest
├── data/                   # SQLite DB (auto-créée)
├── uploads/                # Fichiers importés
├── .github/workflows/
│   └── ci.yml              # CI/CD GitHub Actions
├── start.py                # Lanceur local (auto-génère .env)
├── start_render.py         # Lanceur Render (un seul port)
├── render.yaml             # Config Render
├── Dockerfile              # Build Docker
├── docker-compose.yml      # Orchestration Docker
├── .env.example            # Template variables d'environnement
├── requirements.txt        # Dépendances Python
└── LICENSE                 # Licence propriétaire
```

---

## Fonctionnalités

### Core (tous les plans)
- **Import multi-sources** : CSV, Excel, bases de données (SQL Server, PostgreSQL, MySQL), APIs REST
- **Import DB multi-tables** : sélection par checkboxes, import en batch avec progression
- **Détection doublons** : exact + fuzzy (thefuzz), champs filtrés par source
- **Golden Records** : fusion supervisée avec sélection champ par champ
- **Write-back** : repousser les GR vers les DB sources (INSERT/UPDATE/UPSERT) + dry-run
- **Connecteurs API/ERP** : REST custom, presets (MarineTraffic, Salesforce, SAP, Odoo)
- **Reporting/BI** : KPIs, graphiques, tableaux croisés dynamiques
- **Export CSV** : entités + Golden Records
- **Audit trail** : toutes les actions tracées avec user, date, détails
- **Gestion utilisateurs** : admin, editor, viewer avec contrôle d'accès
- **Règles de fusion** : stratégies configurables par champ

### Module Maritime (Business + Enterprise)
- **Navires** : validation IMO (checksum Luhn), MMSI, normalisation des noms
- **Armateurs** : base consolidée, classification, flotte
- **Ports** : référentiel UN/LOCODE, coordonnées GPS, caractéristiques
- **Escales** : suivi ETA/ETD/ATA/ATD, cargaison, agent, statut
- **Dashboard maritime** : KPIs dédiés, graphiques par type/pavillon

### Module Premium (Enterprise)
- **Data Quality Scoring** : complétude (50%), conformité (30%), fraîcheur (20%)
- **Règles de validation** : 9 types (required, regex, min/max length, range, enum, email, phone)
- **Versioning Golden Records** : historique complet avec diff et restauration
- **Notifications in-app** : fil de notifications, badge temps réel, mark read
- **Webhooks** : endpoints HTTP avec signature HMAC-SHA256, 5 types d'événements
- **Scheduler** : synchronisation automatique des connecteurs API
- **Data Lineage** : traçabilité de chaque champ d'un Golden Record

### ask O.S (Assistant IA)
- Chatbot intégré dans l'interface (bouton en bas à droite)
- Requiert une clé API Anthropic pour fonctionner (optionnel)

---

## Sécurité

- **Mots de passe** : bcrypt avec 12 rounds (migration auto depuis SHA-256)
- **Authentification** : JWT avec secret obligatoire en production
- **Rate limiting** : 5 tentatives/min sur login, 100 req/min par défaut
- **Credentials DB** : chiffrés (XOR+base64) avant stockage
- **CORS** : configurable et restrictif via `MDM_CORS_ORIGINS`
- **Headers** : CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- **SQL injection** : validation des identifiants avec regex + quote_identifier
- **Plans** : routes bloquées côté backend si le module n'est pas dans le plan

---

## Tests

```bash
pip install pytest pytest-cov

# Lancer les 52 tests
pytest tests/ -v

# Avec couverture HTML
pytest tests/ -v --cov=backend --cov-report=html
```

Les tests couvrent : auth, CRUD entités, import CSV, doublons, golden records, export, audit, users, reporting, sécurité headers, connexions DB, data quality, validation rules, notifications, webhooks, scheduler, data lineage.

---

## API (principaux endpoints)

### Core
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/health` | Health check (sans auth) |
| `GET` | `/api/plan` | Plan actuel et modules |
| `POST` | `/api/auth/login` | Authentification |
| `GET` | `/api/auth/me` | Utilisateur courant |
| `GET` | `/api/dashboard/stats` | Statistiques dashboard |
| `GET/POST` | `/api/entities` | CRUD entités |
| `GET` | `/api/entities/sources` | Liste des sources |
| `POST` | `/api/import/csv` | Import fichier CSV/Excel |
| `POST` | `/api/duplicates/detect` | Détection doublons |
| `POST` | `/api/golden-records/merge` | Fusion → Golden Record |
| `GET/POST` | `/api/connections` | CRUD connexions DB |
| `POST` | `/api/connections/:id/import` | Import depuis DB externe |
| `GET` | `/api/reporting/overview` | KPIs et tendances |
| `GET` | `/api/export/csv` | Export CSV |

### Maritime (plan Business+)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET/POST` | `/api/maritime/vessels` | CRUD navires |
| `GET/POST` | `/api/maritime/owners` | CRUD armateurs |
| `GET/POST` | `/api/maritime/ports` | CRUD ports |
| `GET/POST` | `/api/maritime/port-calls` | CRUD escales |

### Premium (plan Enterprise)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/premium/quality/bulk` | Scores qualité globaux |
| `GET/POST` | `/api/premium/validation-rules` | CRUD règles validation |
| `GET` | `/api/premium/notifications` | Notifications in-app |
| `GET/POST` | `/api/premium/webhooks` | CRUD webhooks |
| `GET/POST` | `/api/premium/scheduler/*` | Contrôle scheduler |
| `GET` | `/api/premium/lineage/golden-record/:id` | Data lineage |

---

## Dépendances

```
flask>=3.0.0          # Framework web
pandas>=2.0.0         # Manipulation données
openpyxl>=3.1.0       # Import/export Excel
PyJWT>=2.8.0          # Authentification JWT
bcrypt>=4.0.0         # Hachage mots de passe
pymssql>=2.2.0        # Connexion SQL Server
thefuzz>=0.20.0       # Détection doublons fuzzy
python-Levenshtein>=0.21.0  # Accélération thefuzz
python-dateutil>=2.8.0      # Parsing dates
```

---

## Licence

Propriétaire — OpenSID. Tous droits réservés.

## Contact

- **Email** : contact@opensid.ma
- **Web** : [osmdm.onrender.com](https://osmdm.onrender.com)
