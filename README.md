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
│   👤 User           │
│    (Browser)        │
└──────────┬──────────┘
           │ HTTP(S)
           ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYER                                │
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
│                      AUTHENTICATION LAYER (SSO)                           │
│  ┌────────────────────────────────────────────────────────────┐          │
│  │              🔐 Keycloak Server (Port 8080)                 │          │
│  │                                                             │          │
│  │  Realms:                    Clients:                       │          │
│  │  • master (admin)           • dummy-app (OIDC)             │          │
│  │  • sso-demo (app)                                          │          │
│  │                                                             │          │
│  │  Features:                                                  │          │
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
│                     MONITORING & EVENTS LAYER                             │
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

### 🔄 Data Flow Details

**1. Authentication (Nominal Flow)**
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

**2. Error Handling**
```
Expired token → Refresh with refresh_token → New access_token
Brute force → Keycloak locks account → Event to Kafka → ELK alert
Keycloak down → Circuit breaker → User-facing error message
LDAP unavailable → Local DB fallback (if configured)
```

---
## 📦 Deployed Services

| Service | Description | Port |
|---------|-------------|------|
| **Keycloak** | SSO / IdP server (OIDC, SAML) | 8080 |
| **PostgreSQL** | Keycloak database | 5432 |
| **OpenLDAP** | LDAP directory for users | 389, 636 |
| **phpLDAPadmin** | LDAP management web UI | 6443 |
| **Kafka + Zookeeper** | Message bus for events | 9092 |
| **Elasticsearch** | Logs storage | 9200 |
| **Kibana** | Logs visualization | 5601 |
| **Dummy App** | Demo Node.js / OIDC application | 3000 |

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

## 📁 Project Structure

```
sso-keycloak-project/
├── docker/                  # Docker configuration for services
│   ├── keycloak/
│   ├── ldap/
│   ├── kafka/
│   └── elk/
├── dummy-app/               # Node.js/Express demo application (OIDC)
├── scripts/                 # Automation scripts
├── monitoring/              # Kafka consumer (Python) for anomalies
├── docs/                    # Project documentation
│   └── SETUP.md             # Full installation guide
├── .env.example             # Environment variables template
├── docker-compose.dev.yml   # Docker Compose for development
├── docker-compose.prod.yml  # Docker Compose for production
└── README.md                # This file
```

---

## 🛠️ Technologies Utilisées

- **Keycloak 23.0** : Serveur SSO open-source (Red Hat)
- **OpenLDAP 1.5.0** : LDAP directory for user federation
- **PostgreSQL 15** : Base de données relationnelle
- **Kafka 7.5** : Bus de messages distribué
- **Elasticsearch + Kibana 8.11** : Stack ELK pour logs
- **Node.js + Express** : Backend Dummy App
- **Docker & Docker Compose** : Conteneurisation

---

## 📋 Project Roadmap

- [x] GitHub repository setup
- [x] Docker Compose configuration (Keycloak, PostgreSQL, LDAP, Kafka, ELK)
- [x] Complete SETUP.md documentation
- [x] LDAP configuration in Keycloak (User Federation)
- [x] Dummy App Node.js OIDC development
- [ ] Kafka Python consumer for anomaly detection
- [x] Nominal flow tests (login, callback, logout)
- [ ] Error flow tests (expired token, brute force, server down)
- [ ] Kibana dashboards for monitoring
- [ ] TLS/HTTPS configuration for production
- [x] Final documentation and presentation

---

## 🔐 Security

⚠️ **This project is intended for development and learning purposes only.**

For production, consider:
- ✅ Enable HTTPS/TLS for all services
- ✅ Use a secrets manager (Vault, AWS Secrets Manager)
- ✅ Configure rate limiting (anti-brute force)
- ✅ Enable Elasticsearch authentication
- ✅ Generate strong, unique passwords

---

## 🤝 Contributing

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 📞 Contact

For questions or suggestions, please open an issue in this repository.

---

**Made with ❤️ for learning SSO architectures**
