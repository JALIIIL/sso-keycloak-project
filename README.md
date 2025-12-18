# 🔐 Keycloak SSO Project – Single Sign-On Architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Open-source Single Sign-On (SSO) architecture project using Keycloak, OpenLDAP, and full monitoring (Kafka/ELK), including a demonstration application (Dummy App) built with Node.js.

## 🎯 Project Objectives

-🔒 Implement a complete SSO architecture with Keycloak (OIDC/SAML server)
-📚 Integrate an OpenLDAP directory for identity federation
-🖥️ Develop a Node.js/Express Dummy App using OIDC flows
-📡 Set up a Kafka message bus for SSO events
-📈 Configure Elasticsearch + Kibana for monitoring and logs (Python Consumer + ELK)
-✅ Test nominal flows and error scenarios (expired tokens, brute force, etc.)

## 📊 Project Architecture

`### 🏗️ Complete Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ARCHITECTURE SSO KEYCLOAK                         │
└──────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│   👤 Utilisateur    │
│    (Navigateur)     │
└──────────┬──────────┘
           │ HTTP(S)
           ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                          COUCHE APPLICATION                               │
│  ┌────────────────────┐         OIDC Authorization Code Flow            │
│  │   Dummy App        │  ←──────────────────────────────────────────┐   │
│  │  (Node.js/Express) │                                              │   │
│  │   Port 3000        │  Routes:  /login → /callback → /protected   │   │
│  └─────────┬──────────┘                                              │   │
│            │ OIDC Protocol (JWT Tokens)                              │   │
│            │ Events → Kafka                                          │   │
└────────────┼─────────────────────────────────────────────────────────┼───┘
             ↓                                                         ↑
┌──────────────────────────────────────────────────────────────────────────┐
│                      COUCHE AUTHENTIFICATION (SSO)                        │
│  ┌────────────────────────────────────────────────────────────┐          │
│  │              🔐 Keycloak Server (Port 8080)                 │          │
│  │                                                             │          │
│  │  Realms:                    Clients:                       │          │
│  │  • master (admin)           • dummy-app (OIDC)             │          │
│  │  • sso-demo (app)                                          │          │
│  │                                                             │          │
│  │  Fonctionnalités:                                          │          │
│  │  • User Federation (LDAP)   • Event Listeners (Kafka)      │          │
│  │  • Token Management         • Session Management           │          │
│  │  • Multi-Factor Auth        • Brute Force Protection       │          │
│  └─────────┬────────────────────────────┬─────────────────────┘          │
│            │                            │                                 │
└────────────┼────────────────────────────┼─────────────────────────────────┘
             ↓                            ↓
      ┌─────────────┐             ┌──────────────┐
      │ PostgreSQL  │             │   OpenLDAP   │
      │  (Port      │             │  (Port 389/  │
      │   5432)     │             │     636)     │
      │             │             │              │
      │  Tables:    │             │  Base DN:    │
      │  • REALM    │             │  dc=example, │
      │  • CLIENT   │             │  dc=org      │
      │  • USER_    │             │              │
      │    SESSION  │             │  Attributes: │
      │  • TOKEN    │             │  • uid, cn   │
      └─────────────┘             │  • mail      │
                                  │  • memberOf  │
                                  └──────────────┘
                                         ↕
                                  ┌──────────────┐
                                  │phpLDAPadmin  │
                                  │ (Port 6443)  │
                                  │  (Web UI)    │
                                  └──────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                     COUCHE MONITORING & EVENTS                            │
│                                                                           │
│     Keycloak Events + App Logs                                           │
│                ↓                                                          │
│    ┌────────────────────┐      ┌─────────────────┐                      │
│    │   Zookeeper        │ ←────│     Kafka       │                      │
│    │   (Port 2181)      │      │   (Port 9092)   │                      │
│    │   Coordination     │      │                 │                      │
│    └────────────────────┘      │  Topics:        │                      │
│                                │  • keycloak-    │                      │
│                                │    events       │                      │
│                                │  • app-logs     │                      │
│                                │  • security-    │                      │
│                                │    alerts       │                      │
│                                └────────┬────────┘                      │
│                                         ↓                                │
│                              ┌──────────────────────┐                   │
│                              │  Kafka Consumer      │                   │
│                              │  (Python Script)     │                   │
│                              │                      │                   │
│                              │  Analyse:            │                   │
│                              │  • Brute force       │                   │
│                              │  • Token abuse       │                   │
│                              │  • Anomalies         │                   │
│                              └──────────┬───────────┘                   │
│                                         ↓                                │
│                     ┌──────────────────────────────────┐               │
│                     │  📊 Elasticsearch + Kibana       │               │
│                     │  (Ports 9200, 5601)              │               │
│                     │                                  │               │
│                     │  Dashboards:                     │               │
│                     │  • Login success/failure rate    │               │
│                     │  • Geographic analysis           │               │
│                     │  • Token expiration monitoring   │               │
│                     │  • Security alerts               │               │
│                     └──────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────────────────┘
```

### 🔄 Flux de Données Détaillé

**1. Authentification (Flux Nominal)**
```
User → Dummy App (/login)
  ↓
Redirect → Keycloak (/auth?client_id=dummy-app&redirect_uri=...)
  ↓
Keycloak affiche formulaire
  ↓
User entre credentials
  ↓
Keycloak vérifie contre LDAP
  ↓
Authorization Code généré
  ↓
Redirect → Dummy App (/callback?code=ABC123)
  ↓
Dummy App échange code contre tokens (POST /token)
  ↓
Keycloak retourne: access_token, refresh_token, id_token (JWT)
  ↓
Event "LOGIN_SUCCESS" → Kafka → Elasticsearch
  ↓
User accède aux ressources protégées
```

**2. Gestion des Erreurs**
```
Token Expiré → Refresh avec refresh_token → Nouveau access_token
Brute Force → Keycloak bloque compte → Event vers Kafka → Alerte ELK
Keycloak Down → Circuit breaker → Message d'erreur utilisateur
LDAP Indisponible → Fallback DB locale (si configuré)
```

---
## 📦 Services Déployés

| Service | Description | Port |
|---------|-------------|----|--|
| **Keycloak** | Serveur SSO/IdP (OIDC, SAML) | 8080 |
| **PostgreSQL** | Base de données Keycloak | 5432 |
| **OpenLDAP** | Annuaire LDAP pour utilisateurs | 389, 636 |
| **phpLDAPadmin** | Interface web de gestion LDAP | 6443 |
| **Kafka + Zookeeper** | Bus de messages pour events | 9092 |
| **Elasticsearch** | Stockage des logs | 9200 |
| **Kibana** | Visualisation des logs | 5601 |
| **Dummy App** | Application de démo Node.js/OIDC | 3000 |

## 🚀 Quick Start

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/JALIIIL/sso-keycloak-project.git
cd sso-keycloak-project
```

### 2️⃣ Configurer les variables d'environnement

```bash
cp .env.example .env
# ⚠️ Modifiez TOUS les mots de passe dans .env !
```

### 3️⃣ Lancer le stack complet

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 4️⃣ Vérifier que tout fonctionne

```bash
docker-compose -f docker-compose.dev.yml ps
# Tous les services doivent être "Up" ou "healthy"
```

### 5️⃣ Accéder aux interfaces

- Keycloak Admin : http://localhost:8080/admin
- phpLDAPadmin : http://localhost:6443
- Kibana : http://localhost:5601

📖 **Pour plus de détails** : Consultez [docs/SETUP.md](docs/SETUP.md)

---

## 📁 Structure du Projet

```
sso-keycloak-project/
├── docker/                  # Configuration Docker des services
│   ├── keycloak/
│   ├── ldap/
│   ├── kafka/
│   └── elk/
├── dummy-app/               # Application Node.js/Express avec OIDC
├── scripts/                 # Scripts d'automatisation
├── monitoring/              # Consumer Kafka Python pour anomalies
├── docs/                    # Documentation du projet
│   └── SETUP.md             # Guide d'installation complet
├── .env.example             # Template des variables d'environnement
├── docker-compose.dev.yml   # Stack Docker pour développement
├── docker-compose.prod.yml  # Stack Docker pour production
└── README.md                # Ce fichier
```

---

## 🛠️ Technologies Utilisées

- **Keycloak 23.0** : Serveur SSO open-source (Red Hat)
- **OpenLDAP 1.5.0** : Annuaire LDAP pour fédération d'utilisateurs
- **PostgreSQL 15** : Base de données relationnelle
- **Kafka 7.5** : Bus de messages distribué
- **Elasticsearch + Kibana 8.11** : Stack ELK pour logs
- **Node.js + Express** : Backend Dummy App
- **Docker & Docker Compose** : Conteneurisation

---

## 📋 Roadmap du Projet

- [x] Setup du repository GitHub
- [x] Configuration Docker Compose (Keycloak, PostgreSQL, LDAP, Kafka, ELK)
- [x] Documentation SETUP.md complète
- [ ] Configuration LDAP dans Keycloak (User Federation)
- [ ] Développement de la Dummy App Node.js avec OIDC
- [ ] Consumer Kafka Python pour détection d'anomalies
- [ ] Tests des flux nominaux (login, callback, logout)
- [ ] Tests des flux d'erreur (token expiré, brute force, serveur down)
- [ ] Dashboards Kibana pour supervision
- [ ] Configuration TLS/HTTPS pour production
- [ ] Documentation finale et présentation

---

## 🔐 Sécurité

⚠️ **Ce projet est pour le développement/apprentissage uniquement !**

Pour la production, pensez à :
- ✅ Activer HTTPS/TLS partout
- ✅ Utiliser des secrets managers (Vault, AWS Secrets Manager)
- ✅ Configurer des rate limits (anti-brute force)
- ✅ Activer l'authentification Elasticsearch
- ✅ Générer des mots de passe forts et uniques

---

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche pour votre feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📞 Contact

Pour toute question ou suggestion, ouvrez une issue sur ce repository.

---

**Made with ❤️ for learning SSO architectures**
