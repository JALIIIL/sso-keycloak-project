# 🚀 Quick Start - SSO Keycloak

## 📋 Prerequisites

- Docker (v20+) and Docker Compose (v2+)
- Git
- Node.js (v18+) for the Dummy App

## ⚡ Installation (3 steps)

### 1. Clone and configure

```bash
git clone https://github.com/JALIIIL/sso-keycloak-project.git
cd sso-keycloak-project
cp .env.example .env
```

### 2. Edit the .env file

Open `.env` and update passwords:

```bash
KEYCLOAK_ADMIN_PASSWORD=YourStrongPassword
POSTGRES_PASSWORD=YourDBPassword
LDAP_ADMIN_PASSWORD=YourLDAPPassword
OIDC_CLIENT_SECRET=YourClientSecret
```

⚠️ **Never commit the .env file!**

### 3. Start the stack

```bash
docker-compose -f docker-compose.dev.yml up -d
```

Wait about 1 minute for services to start.

## 🔍 Accessing services

- **Keycloak Admin** : http://localhost:8080/admin
  - Username: `admin`
  - Password: [Your KEYCLOAK_ADMIN_PASSWORD]

- **phpLDAPadmin** : http://localhost:6443
- **Kibana** : http://localhost:5601

## ⚙️ Keycloak minimum configuration

### Create a Realm

1. Log in to Keycloak
2. Click on "master" (top-left) → **Create Realm**
3. Name: `sso-demo`
4. Click **Create**

### Create an OIDC Client

1. In the `sso-demo` realm → **Clients** → **Create client**
2. Fill in:
   - **Client ID**: `dummy-app`
   - **Client authentication**: ON
   - **Valid redirect URIs**: `http://localhost:3000/*`
   - **Web origins**: `http://localhost:3000`
3. Click **Save**
4. Copy the **Client Secret** (Credentials tab)
5. Put it in `.env`: `OIDC_CLIENT_SECRET=...`

### Create a test user

1. **Users** → **Add user**
2. Username: `testuser`
3. Credentials tab → Set a password
4. Disable **Temporary**

## 🧪 Quick test

Verify Keycloak is running:

```bash
curl http://localhost:8080/health/ready
```

Expected result: `{"status":"UP"}`

## 🛑 Stop

```bash
# Stop without removing data
docker-compose -f docker-compose.dev.yml down

# Full reset (remove volumes)
docker-compose -f docker-compose.dev.yml down -v
```

## 📝 Useful commands

```bash
# View logs
docker-compose -f docker-compose.dev.yml logs -f keycloak

# Restart a service
docker-compose -f docker-compose.dev.yml restart keycloak

# View service status
docker-compose -f docker-compose.dev.yml ps
```

## 🆘 Common issues

**Port already in use?**
→ Change ports in `.env` (e.g. `KEYCLOAK_HTTP_PORT=8081`)

**Keycloak won't start?**
→ Wait 30s for PostgreSQL to be ready, then restart

**Unable to login?**
→ Check logs: `docker-compose -f docker-compose.dev.yml logs keycloak`

## 📚 Full documentation

For more details (LDAP, Kafka, Elasticsearch, etc.), see the main README.md.

---

⚠️ **This setup is for development only!**
