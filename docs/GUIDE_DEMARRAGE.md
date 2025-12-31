# 🚀 Quick Start Guide - SSO Keycloak

## Prerequisites

- ✅ Docker Desktop installed and running
- ✅ Git installed
- ✅ Terminal (PowerShell, CMD, or Bash)

---

## 📦 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/JALIIIL/sso-keycloak-project.git
cd sso-keycloak-project
```

### 2️⃣ Configure environment variables

```bash
# Copy the template
cp .env.example .env

# Edit .env with your values
# Example:
# KEYCLOAK_ADMIN=admin
# KEYCLOAK_ADMIN_PASSWORD=admin_secure_2024
# POSTGRES_PASSWORD=keycloak_db_password
```

⚠️ **Never commit the `.env` file!**

### 3️⃣ Start the Docker stack

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 4️⃣ Verify services are running

```bash
# View running containers
docker ps

# View Keycloak logs
docker-compose -f docker-compose.dev.yml logs -f keycloak
```

**Wait 2-3 minutes** for Keycloak to fully start.

### 5️⃣ Access Keycloak Admin Console

🔗 **URL** : http://localhost:8080/admin

**Credentials** :
- Username : `admin`
- Password : The one set in `.env`

---

## 🔧 Useful Commands

### Stop services

```bash
docker-compose -f docker-compose.dev.yml down
```

### Restart services

```bash
docker-compose -f docker-compose.dev.yml restart
```

### Full reset (wipes all data)

```bash
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

### View real-time logs

```bash
# All services
docker-compose -f docker-compose.dev.yml logs -f

# Keycloak only
docker-compose -f docker-compose.dev.yml logs -f keycloak

# PostgreSQL only
docker-compose -f docker-compose.dev.yml logs -f postgres
```

---

## 🎯 Initial Keycloak Configuration

### Create a Realm

1. In the admin console → **"Create realm"**
2. **Realm name**: `sso-demo`
3. **Create**

### Create an OIDC Client

1. **Clients** → **"Create client"**
2. **Client ID**: `dummy-app`
3. **Client Protocol**: `openid-connect`
4. Enable **Standard flow** and **Direct access grants**
5. **Valid redirect URIs**: `http://localhost:3000/*`
6. **Save**

### Create a test user

1. **Users** → **"Add user"**
2. **Username**: `test-user`
3. **Email**: `test@example.com`
4. **Create**
5. Credentials → Set password: `Test1234!`
6. Disable **"Temporary"**
7. **Save**

---

## ❌ Troubleshooting

### Keycloak won't start

```bash
# Check logs
docker-compose -f docker-compose.dev.yml logs keycloak

# Solution: wait 2-3 min or full reset
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

### Port 8080 already in use

```bash
# Identify process
netstat -ano | findstr :8080

# Kill process
taskkill /PID <PID> /F
```

### "Connection refused"

✅ Ensure Docker Desktop is running
```bash
docker ps
```

✅ Restart containers
```bash
docker-compose -f docker-compose.dev.yml restart
```

---

## 📊 Available Interfaces

| Service | URL | Credentials |
|---------|-----|-------------|
| **Keycloak Admin** | http://localhost:8080/admin | `admin` / (see `.env`) |
| **PostgreSQL** | `localhost:5432` | `keycloak` / (see `.env`) |
| **phpLDAPadmin** | http://localhost:6443 | (if configured) |
| **Kibana** | http://localhost:5601 | (if configured) |

---

## 📚 Additional Documentation

- [SETUP.md](./SETUP.md) - Full detailed guide
- [README.md](../README.md) - Project overview
- [Architecture](../README.md#-architecture-du-projet)

---

**🤝 Need help?** Check the documentation or contact the project team.
