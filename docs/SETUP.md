# 🚀 Guide de Setup - Projet SSO Keycloak

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Docker** (v20+) et **Docker Compose** (v2+)
- **Git**
- **Node.js** (v18+) et **npm** (pour la Dummy App)
- **Un éditeur de code** (VS Code recommandé)

### Vérification des prérequis

```bash
docker --version
docker-compose --version
git --version
node --version
npm --version
```

---

## 🔧 Installation Initiale

### 1. Cloner le repository

```bash
git clone https://github.com/JALIIIL/sso-keycloak-project.git
cd sso-keycloak-project
```

### 2. Créer votre fichier .env local

⚠️ **IMPORTANT** : Ne JAMAIS commit le fichier `.env` !

```bash
cp .env.example .env
```

### 3. Modifier les valeurs dans .env

Ouvrez `.env` et changez les valeurs par défaut :

```bash
# Changez TOUS les mots de passe pour le développement
KEYCLOAK_ADMIN_PASSWORD=VotreMotDePasseSecurise
POSTGRES_PASSWORD=VotreMotDePasseDB
LDAP_ADMIN_PASSWORD=VotreMotDePasseLDAP
APP_SESSION_SECRET=$(openssl rand -base64 32)
OIDC_CLIENT_SECRET=VotreClientSecret
ELASTIC_PASSWORD=VotreMotDePasseElastic
```

### 4. Lancer le stack complet

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 5. Vérifier que tous les services sont up

```bash
docker-compose -f docker-compose.dev.yml ps
```

Tous les services doivent avoir le status **"Up"** ou **"healthy"**.

---

## 🔍 Accès aux Services

Une fois le stack lancé, vous pouvez accéder à :

| Service | URL | Credentials |
|---------|-----|-------------|
| **Keycloak Admin** | http://localhost:8080/admin | admin / [Votre KEYCLOAK_ADMIN_PASSWORD] |
| **phpLDAPadmin** | http://localhost:6443 | cn=admin,dc=example,dc=org / [Votre LDAP_ADMIN_PASSWORD] |
| **Kibana** | http://localhost:5601 | - |
| **Elasticsearch** | http://localhost:9200 | - |

---

## ⚙️ Configuration de Keycloak

### 1. Créer un Realm "sso-demo"

1. Connectez-vous à Keycloak Admin Console
2. Cliquez sur le dropdown en haut à gauche ("master")
3. Cliquez sur **"Create Realm"**
4. Nom : `sso-demo`
5. Cliquez **"Create"**

### 2. Créer un Client OIDC

1. Dans le realm `sso-demo`, allez dans **Clients** → **Create client**
2. Remplissez :
   - **Client ID** : `dummy-app`
   - **Client authentication** : ON
   - **Valid redirect URIs** : `http://localhost:3000/*`
   - **Web origins** : `http://localhost:3000`
3. Cliquez **Save**
4. Allez dans l'onglet **"Credentials"** et copiez le **Client Secret**
5. Mettez cette valeur dans votre `.env` : `OIDC_CLIENT_SECRET=<client_secret>`

### 3. Créer des utilisateurs de test

1. Allez dans **Users** → **Add user**
2. Créez un utilisateur `testuser`
3. Allez dans l'onglet **Credentials** et définissez un mot de passe
4. Désactivez **"Temporary"** pour ne pas avoir à changer le MDP

---

## 🧪 Tests de Validation

### Test 1 : Keycloak fonctionne

```bash
curl http://localhost:8080/health/ready
```

Résultat attendu : `{"status":"UP"}`

### Test 2 : PostgreSQL est accessible

```bash
docker exec -it sso-postgres psql -U keycloak -d keycloak -c "\\dt"
```

Résultat attendu : Liste des tables Keycloak

### Test 3 : LDAP est up

```bash
docker exec -it sso-openldap ldapsearch -x -H ldap://localhost -b dc=example,dc=org -D "cn=admin,dc=example,dc=org" -w ${LDAP_ADMIN_PASSWORD}
```

### Test 4 : Kafka est accessible

```bash
docker exec -it sso-kafka kafka-topics --bootstrap-server localhost:9092 --list
```

### Test 5 : Elasticsearch est up

```bash
curl http://localhost:9200
```

---

## 🛑 Arrêter les services

```bash
# Arrêter sans supprimer les volumes
docker-compose -f docker-compose.dev.yml down

# Arrêter ET supprimer les volumes (reset complet)
docker-compose -f docker-compose.dev.yml down -v
```

---

## 📝 Commandes Utiles

### Voir les logs d'un service

```bash
docker-compose -f docker-compose.dev.yml logs -f keycloak
docker-compose -f docker-compose.dev.yml logs -f postgres
```

### Redémarrer un service

```bash
docker-compose -f docker-compose.dev.yml restart keycloak
```

### Reconstruire un service

```bash
docker-compose -f docker-compose.dev.yml up -d --build keycloak
```

---

## 🆘 Troubleshooting

### Erreur : "Port already in use"

Changez les ports dans votre `.env` :

```bash
KEYCLOAK_HTTP_PORT=8081
POSTGRES_PORT=5433
```

### Keycloak ne démarre pas

Vérifiez les logs :

```bash
docker-compose -f docker-compose.dev.yml logs keycloak
```

Problème fréquent : PostgreSQL n'est pas prêt. Attendez 30s et relancez.

### Impossible de se connecter à Keycloak

Vérifiez que le healthcheck passe :

```bash
docker inspect sso-keycloak | grep Health -A 10
```

---

## 🔐 Sécurité pour le Développement

⚠️ Ce setup est pour le **développement uniquement** !

Pour la production :
- ✅ Activer TLS/HTTPS
- ✅ Utiliser des secrets managers (Vault, AWS Secrets Manager)
- ✅ Activer l'authentification Elasticsearch
- ✅ Configurer les rate limits
- ✅ Utiliser des mots de passe forts

---

## 📚 Prochaines Étapes

1. [ ] Configurer LDAP dans Keycloak (voir `docs/LDAP.md`)
2. [ ] Développer la Dummy App Node.js (voir `dummy-app/`)
3. [ ] Configurer le consumer Kafka Python (voir `monitoring/`)
4. [ ] Tester les flux OIDC nominaux et d'erreurs
5. [ ] Mettre en place les dashboards Kibana

---

## 🤝 Contribution

Avant de push :

1. Vérifiez que `.env` n'est PAS tracké : `git status`
2. Testez localement : `docker-compose -f docker-compose.dev.yml up`
3. Committez avec des messages clairs
4. Créez une PR et demandez une review

---

## 📞 Support

Problèmes ? Contactez l'équipe ou ouvrez une issue sur GitHub.
