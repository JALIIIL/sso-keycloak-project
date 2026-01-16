const express = require('express');
const session = require('express-session');
const passport = require('passport');
const { Strategy } = require('passport-openidconnect');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

/* ---------- Vérification des variables d'environnement ---------- */
const requiredEnv = [
  'CLIENT_ID',
  'CLIENT_SECRET',
  'SESSION_SECRET',
  'KEYCLOAK_URL',
  'KEYCLOAK_REALM',
  'CALLBACK_URL',
];
requiredEnv.forEach((v) => {
  if (!process.env[v]) console.warn(`⚠️ Attention: ${v} n'est pas défini dans .env`);
});

/* ---------- Session ---------- */
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: process.env.NODE_ENV === 'production',
      httpOnly: true,
      maxAge: 60 * 60 * 1000,
    },
  })
);

app.use(passport.initialize());
app.use(passport.session());

/* ---------- Keycloak / OIDC ---------- */
const keycloakURL = process.env.KEYCLOAK_URL;        // ex: http://localhost:8080
const realm = process.env.KEYCLOAK_REALM;           // sso-demo

// URL publique vue par le navigateur (ici aussi localhost)
const keycloakPublicURL =
  typeof keycloakURL === 'string' && keycloakURL.includes('keycloak:8080')
    ? 'http://localhost:8080'
    : keycloakURL;

console.log('DEBUG: keycloakURL =', keycloakURL);
console.log('DEBUG: keycloakPublicURL =', keycloakPublicURL);
console.log('DEBUG: callbackURL =', process.env.CALLBACK_URL);

passport.use(
  'oidc',
  new Strategy(
    {
      issuer: `${keycloakURL}/realms/${realm}`,
      authorizationURL: `${keycloakPublicURL}/realms/${realm}/protocol/openid-connect/auth`,
      tokenURL: `${keycloakURL}/realms/${realm}/protocol/openid-connect/token`,
      userInfoURL: `${keycloakURL}/realms/${realm}/protocol/openid-connect/userinfo`,
      clientID: process.env.CLIENT_ID,
      clientSecret: process.env.CLIENT_SECRET,
      callbackURL: process.env.CALLBACK_URL, // http://localhost:3000/callback
      scope: 'openid profile email',
    },
    (issuer, profile, done) => {
      profile.roles = profile._json?.realm_access?.roles || ['user'];
      return done(null, profile);
    }
  )
);

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

/* ---------- Middleware ---------- */
app.use(express.static(path.join(__dirname, 'public')));

function ensureAuth(req, res, next) {
  if (req.isAuthenticated()) return next();
  res.redirect('/login-page');
}

/* ========== ROUTES ========== */

// Page d’accueil : redirige vers login-page ou dashboard
app.get('/', (req, res) => {
  if (req.isAuthenticated()) return res.redirect('/dashboard');
  res.redirect('/login-page');
});

// Démarrage du flux OIDC
app.get('/login', passport.authenticate('oidc'));

// Page de login custom (HTML dans public/login-page.html)
app.get('/login-page', (req, res) => {
  if (req.isAuthenticated()) return res.redirect('/dashboard');
  res.sendFile(path.join(__dirname, 'public', 'login-page.html'));
});

// Callback OIDC après login Keycloak
app.get(
  '/callback',
  passport.authenticate('oidc', { failureRedirect: '/login-page' }),
  (req, res) => res.redirect('/dashboard')
);

// Page « créer un compte » (front) : redirige ensuite vers /login
app.get('/register', (req, res) => {
  if (req.isAuthenticated()) return res.redirect('/dashboard');
  res.sendFile(path.join(__dirname, 'public', 'register.html'));
});

// Dashboard protégé
app.get('/dashboard', ensureAuth, (req, res) =>
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'))
);

// API pour récupérer les infos utilisateur (utilisée par dashboard.html)
app.get('/api/user', ensureAuth, (req, res) =>
  res.json({
    authenticated: true,
    user: {
      id: req.user.id,
      displayName: req.user.displayName || req.user.name || 'User',
      name: req.user.displayName || req.user.name || 'User',
      email: req.user._json?.email || 'Not specified',
      roles: req.user.roles || ['user'],
    },
  })
);

// Logout : termine la session locale + Keycloak, puis retourne sur login-page
app.get('/logout', (req, res, next) => {
  req.logout(function (err) {
    if (err) return next(err);

    const redirectAfterLogout = 'http://localhost:3000/login-page';

    const logoutURL =
      `${keycloakPublicURL}/realms/${realm}/protocol/openid-connect/logout` +
      `?post_logout_redirect_uri=${encodeURIComponent(redirectAfterLogout)}` +
      `&client_id=${encodeURIComponent(process.env.CLIENT_ID)}`;

    res.redirect(logoutURL);
  });
});

// Healthcheck simple
app.get('/health', (req, res) => res.status(200).json({ status: 'ok' }));

/* ---------- Serveur ---------- */
app.listen(PORT, () =>
  console.log(`✅ App running on http://localhost:${PORT}`)
);
