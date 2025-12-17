# 🚀 Guide de Démarrage Rapide - SSO Keycloak

## Prérequis

- ✅ Docker Desktop installé et démarré
- ✅ Git installé
- ✅ Terminal (PowerShell, CMD, ou Bash)

---

## 📦 Étapes de Démarrage

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/JALIIIL/sso-keycloak-project.git
cd sso-keycloak-project
```

### 2️⃣ Configurer les variables d'environnement

```bash
# Copier le template
cp .env.example .env

# Éditer .env avec tes propres valeurs
# Exemple :
# KEYCLOAK_ADMIN=admin
# KEYCLOAK_ADMIN_PASSWORD=admin_secure_2024
# POSTGRES_PASSWORD=keycloak_db_password
```

⚠️ **Ne jamais commiter le fichier `.env` !**

### 3️⃣ Démarrer le stack Docker

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 4️⃣ Vérifier que les services sont actifs

```bash
# Voir les conteneurs actifs
docker ps

# Voir les logs Keycloak
docker-compose -f docker-compose.dev.yml logs -f keycloak
```

**Attendre 2-3 minutes** que Keycloak démarre complètement.

### 5️⃣ Accéder à Keycloak Admin Console

🔗 **URL** : http://localhost:8080/admin

**Credentials** :
- Username : `admin`
- Password : Celui défini dans `.env`

---

## 🔧 Commandes Utiles

### Arrêter les services

```bash
docker-compose -f docker-compose.dev.yml down
```

### Redémarrer les services

```bash
docker-compose -f docker-compose.dev.yml restart
```

### Reset complet (efface toutes les données)

```bash
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

### Voir les logs en temps réel

```bash
# Tous les services
docker-compose -f docker-compose.dev.yml logs -f

# Keycloak uniquement
docker-compose -f docker-compose.dev.yml logs -f keycloak

# PostgreSQL uniquement
docker-compose -f docker-compose.dev.yml logs -f postgres
```

---

## 🎯 Configuration Initiale Keycloak

### Créer un Realm

1. Dans l'admin console → **"Create realm"**
2. **Realm name** : `sso-demo`
3. **Create**

### Créer un Client OIDC

1. **Clients** → **"Create client"**
2. **Client ID** : `dummy-app`
3. **Client Protocol** : `openid-connect`
4. Activer **Standard flow** et **Direct access grants**
5. **Valid redirect URIs** : `http://localhost:3000/*`
6. **Save**

### Créer un utilisateur de test

1. **Users** → **"Add user"**
2. **Username** : `test-user`
3. **Email** : `test@example.com`
4. **Create**
5. Onglet **"Credentials"** → Set password : `Test1234!`
6. Désactiver **"Temporary"**
7. **Save**

---

## ❌ Troubleshooting

### Keycloak ne démarre pas

```bash
# Vérifier les logs
docker-compose -f docker-compose.dev.yml logs keycloak

# Solution : attendre 2-3 min ou reset complet
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

### Port 8080 déjà utilisé

```bash
# Identifier le processus
netstat -ano | findstr :8080

# Tuer le processus
taskkill /PID <PID> /F
```

### "Connection refused"

✅ Vérifie que Docker Desktop est démarré
```bash
docker ps
```

✅ Redémarre les conteneurs
```bash
docker-compose -f docker-compose.dev.yml restart
```

---

## 📊 Interfaces Disponibles

| Service | URL | Credentials |
|---------|-----|-------------|
| **Keycloak Admin** | http://localhost:8080/admin | `admin` / (voir `.env`) |
| **PostgreSQL** | `localhost:5432` | `keycloak` / (voir `.env`) |
| **phpLDAPadmin** | http://localhost:6443 | (si configuré) |
| **Kibana** | http://localhost:5601 | (si configuré) |

---

## 📚 Documentation Supplémentaire

- [SETUP.md](./SETUP.md) - Guide détaillé complet
- [README.md](../README.md) - Vue d'ensemble du projet
- [Architecture](../README.md#-architecture-du-projet)

---

**🤝 Besoin d'aide ?** Consulte la documentation ou contacte l'équipe du projet.
