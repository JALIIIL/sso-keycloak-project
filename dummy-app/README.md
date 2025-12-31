# Dummy Application - SSO Keycloak Demo

This is a Node.js/Express demo application that integrates SSO authentication with Keycloak using OpenID Connect (OIDC).

## 🎯 Purpose

The application serves as an OIDC client to validate Keycloak integration and demonstrate SSO authentication flows.

## 📋 Prerequisites

- Node.js 18+
- Docker & Docker Compose (for Keycloak)
- Keycloak configured with the `sso-demo` realm and the `dummy-app` client

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/JALIIIL/sso-keycloak-project.git
cd sso-keycloak-project/dummy-app
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configuration

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Example `.env` values:

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

## 🎮 Usage

### Development

```bash
npm run dev
```

### Production

```bash
npm start
```

The app will be available at `http://localhost:3000`.

## 🔒 OIDC Authentication Flow

1. **Access the app** → Redirect to Keycloak
2. **Authenticate** → Enter credentials on Keycloak
3. **Authorization Code** → Keycloak redirects with code
4. **Token Exchange** → App exchanges code for tokens
5. **Session** → User authenticated

## 📁 Structure

```
dummy-app/
├── src/
│   ├── server.js          # Express entrypoint
│   ├── config/
│   │   └── keycloak.js    # OIDC configuration
│   ├── routes/
│   │   ├── auth.js        # Authentication routes
│   │   └── protected.js   # Protected routes
│   └── middleware/
│       └── auth.js        # Token verification middleware
├── public/
│   ├── dashboard.html     # User interface
│   └── styles.css
├── package.json
├── Dockerfile
├── .dockerignore
├── .env.example
└── README.md
```

## 🐳 Docker

### Build image

```bash
docker build -t dummy-app .
```

### Run container

```bash
docker run -p 3000:3000 --env-file .env dummy-app
```

## 🔗 Endpoints

- `GET /` - Public home page
- `GET /login` - Trigger OIDC authentication
- `GET /callback` - OIDC callback after authentication
- `GET /dashboard` - Protected page (requires auth)
- `GET /api/user` - Current authenticated user info
- `GET /logout` - Logout
- `GET /health` - Health check

## 🧪 Testing Authentication

1. Start Keycloak: `docker-compose -f ../docker-compose.dev.yml up -d`
2. Create a test user in Keycloak (realm `sso-demo`)
3. Start the app: `npm run dev`
4. Open `http://localhost:3000/dashboard`
5. Login with the test credentials

## 📊 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KEYCLOAK_URL` | Keycloak base URL | `http://localhost:8080` |
| `KEYCLOAK_REALM` | Realm name | `sso-demo` |
| `CLIENT_ID` | OIDC client ID | `dummy-app` |
| `CLIENT_SECRET` | Client secret | - |
| `CALLBACK_URL` | Callback URL | `http://localhost:3000/callback` |
| `PORT` | App port | `3000` |
| `SESSION_SECRET` | Express session secret | - |
| `NODE_ENV` | Environment | `development` |

## 🛠️ Technologies

- **Express.js** - Node.js web framework
- **passport-openidconnect** - OIDC strategy for Passport (used in the app)
- **express-session** - Session management
- **Keycloak** - Authentication server

## 🐛 Debugging

Enable verbose logs:

```bash
DEBUG=* npm run dev
```

## 📝 License

MIT
