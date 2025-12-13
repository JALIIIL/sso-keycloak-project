# 🚀 Quick Start - SSO Keycloak

## 📋 Prérequis

- Docker (v20+) et Docker Compose (v2+)
- Git
- Node.js (v18+) pour la Dummy App

## ⚡ Installation (3 étapes)

### 1. Cloner et configurer

```bash
git clone https://github.com/JALIIIL/sso-keycloak-project.git
cd sso-keycloak-project
cp .env.example .env
```

### 2. Modifier le fichier .env

Ouvrez `.env` et changez les mots de passe :

```bash
KEYCLOAK_ADMIN_PASSWORD=VotreMotDePasse
POSTGRES_PASSWORD=VotreMotDePasseDB
LDAP_ADMIN_PASSWORD=VotreMotDePasseLDAP
OIDC_CLIENT_SECRET=VotreClientSecret
```

⚠️ **Ne JAMAIS commit le fichier .env !**

### 3. Lancer le stack

```bash
docker-compose -f docker-compose.dev.yml up -d
```

Attendez 1 minute que tous les services démarrent.

## 🔍 Accès aux Services

- **Keycloak Admin** : http://localhost:8080/admin
  - Username: `admin`
  - Password: [Votre KEYCLOAK_ADMIN_PASSWORD]

- **phpLDAPadmin** : http://localhost:6443
- **Kibana** : http://localhost:5601

## ⚙️ Configuration Keycloak (Minimum)

### Créer un Realm

1. Connectez-vous à Keycloak
2. Cliquez sur "master" (en haut à gauche) → **Create Realm**
3. Nom : `sso-demo`
4. Cliquez **Create**

### Créer un Client OIDC

1. Dans le realm `sso-demo` → **Clients** → **Create client**
2. Remplissez :
   - **Client ID** : `dummy-app`
   - **Client authentication** : ON
   - **Valid redirect URIs** : `http://localhost:3000/*`
   - **Web origins** : `http://localhost:3000`
3. Cliquez **Save**
4. Copiez le **Client Secret** (onglet Credentials)
5. Mettez-le dans `.env` : `OIDC_CLIENT_SECRET=...`

### Créer un utilisateur test

1. **Users** → **Add user**
2. Username : `testuser`
3. Onglet **Credentials** → Définir un mot de passe
4. Désactiver **Temporary**

## 🧪 Test Rapide

Vérifiez que Keycloak fonctionne :

```bash
curl http://localhost:8080/health/ready
```

Résultat attendu : `{"status":"UP"}`

## 🛑 Arrêter

```bash
# Arrêter sans supprimer les données
docker-compose -f docker-compose.dev.yml down

# Reset complet (supprimer les volumes)
docker-compose -f docker-compose.dev.yml down -v
```

## 📝 Commandes Utiles

```bash
# Voir les logs
docker-compose -f docker-compose.dev.yml logs -f keycloak

# Redémarrer un service
docker-compose -f docker-compose.dev.yml restart keycloak

# Voir l'état des services
docker-compose -f docker-compose.dev.yml ps
```

## 🆘 Problèmes Fréquents

**Port déjà utilisé ?**
→ Changez les ports dans `.env` (ex: `KEYCLOAK_HTTP_PORT=8081`)

**Keycloak ne démarre pas ?**
→ Attendez 30s que PostgreSQL soit prêt, puis relancez

**Impossible de se connecter ?**
→ Vérifiez les logs : `docker-compose -f docker-compose.dev.yml logs keycloak`

## 📚 Documentation Complète

Pour plus de détails (LDAP, Kafka, Elasticsearch, etc.), consultez le README.md principal.

---

⚠️ **Ce setup est pour le développement uniquement !**
