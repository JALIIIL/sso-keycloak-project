# Dummy Application - SSO Keycloak Demo

Application de démonstration Node.js/Express intégrant l'authentification SSO avec Keycloak via OpenID Connect (OIDC).

## 🎯 Objectif

Cette application sert de client OIDC pour valider l'intégration avec Keycloak et démontrer les flux d'authentification SSO.

## 📋 Prérequis

- Node.js 18+
- Docker & Docker Compose (pour Keycloak)
- Keycloak configuré avec le realm `sso-demo` et le client `dummy-app`

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/JALIIIL/sso-keycloak-project.git
cd sso-keycloak-project/dummy-app
```

### 2. Installer les dépendances

```bash
npm install
```

### 3. Configuration

Copier le fichier `.env.example` vers `.env` et configurer:

```bash
cp .env.example .env
```

Modifier les valeurs dans `.env`:

```env
# Keycloak Configuration
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=sso-demo

# Client Configuration
CLIENT_ID=dummy-app
CLIENT_SECRET=your-client-secret-here

# Application Configuration
CALLBACK_URL=http://localhost:3000/callback
PORT=3000
SESSION_SECRET=change-me-in-production
NODE_ENV=development
```

## 🎮 Utilisation

### Démarrage en mode développement

```bash
npm run dev
```

### Démarrage en mode production

```bash
npm start
```

L'application sera accessible sur `http://localhost:3000`

## 🔒 Flux d'authentification OIDC

1. **Accès à l'application** → Redirection vers Keycloak
2. **Authentification** → Saisie credentials sur Keycloak
3. **Authorization Code** → Keycloak redirige avec code
4. **Token Exchange** → Application échange code contre tokens
5. **Session** → Utilisateur authentifié

## 📁 Structure

```
dummy-app/
├── src/
│   ├── server.js          # Point d'entrée Express
│   ├── config/
│   │   └── keycloak.js    # Configuration OIDC
│   ├── routes/
│   │   ├── auth.js        # Routes authentification
│   │   └── protected.js   # Routes protégées
│   └── middleware/
│       └── auth.js        # Middleware vérification tokens
├── public/
│   ├── dashboard.html     # Interface utilisateur
│   └── styles.css
├── package.json
├── Dockerfile
├── .dockerignore
├── .env.example
└── README.md
```

## 🐳 Docker

### Build de l'image

```bash
docker build -t dummy-app .
```

### Lancement du conteneur

```bash
docker run -p 3000:3000 --env-file .env dummy-app
```

## 🔗 Endpoints

- `GET /` - Page d'accueil publique
- `GET /login` - Déclenche l'authentification OIDC
- `GET /callback` - Callback OIDC après authentification
- `GET /dashboard` - Page protégée (requiert authentification)
- `GET /userinfo` - Informations utilisateur connecté
- `GET /logout` - Déconnexion
- `GET /health` - Health check

## 🧪 Tests

### Tester l'authentification

1. Démarrer Keycloak: `docker-compose -f ../docker-compose.dev.yml up -d`
2. Créer un utilisateur test dans Keycloak (realm sso-demo)
3. Démarrer l'app: `npm run dev`
4. Accéder à `http://localhost:3000/dashboard`
5. Se connecter avec les credentials test

## 📊 Variables d'environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `KEYCLOAK_URL` | URL Keycloak | `http://localhost:8080` |
| `KEYCLOAK_REALM` | Nom du realm | `sso-demo` |
| `CLIENT_ID` | ID du client OIDC | `dummy-app` |
| `CLIENT_SECRET` | Secret du client | - |
| `CALLBACK_URL` | URL de callback | `http://localhost:3000/callback` |
| `PORT` | Port application | `3000` |
| `SESSION_SECRET` | Secret session Express | - |
| `NODE_ENV` | Environnement | `development` |

## 🛠️ Technologies

- **Express.js** - Framework web Node.js
- **openid-client** - Client OIDC pour Node.js
- **express-session** - Gestion sessions
- **Keycloak** - Serveur d'authentification

## 🐛 Debugging

Activer les logs détaillés:

```bash
DEBUG=* npm run dev
```

## 📝 Licence

MIT
