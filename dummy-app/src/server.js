const express = require('express');
const session = require('express-session');
const passport = require('passport');
const { Strategy } = require('passport-openidconnect');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

/* ================================
   Session & Passport
================================ */
app.use(
  session({
    secret: process.env.SESSION_SECRET || 'change-me',
    resave: false,
    saveUninitialized: false
  })
);

app.use(passport.initialize());
app.use(passport.session());

/* ================================
   Keycloak / OIDC Configuration
================================ */
const keycloakURL = process.env.KEYCLOAK_URL || 'http://localhost:8080';
const realm = process.env.KEYCLOAK_REALM || 'sso-demo';

passport.use(
  'oidc',
  new Strategy(
    {
      authorizationURL: `${keycloakURL}/realms/${realm}/protocol/openid-connect/auth`,
      tokenURL: `${keycloakURL}/realms/${realm}/protocol/openid-connect/token`,
      userInfoURL: `${keycloakURL}/realms/${realm}/protocol/openid-connect/userinfo`,
      clientID: process.env.CLIENT_ID || 'dummy-app',
      clientSecret: process.env.CLIENT_SECRET,
      callbackURL:
        process.env.CALLBACK_URL || 'http://localhost:3000/callback',
      scope: 'openid profile email'
    },
    (issuer, profile, done) => {
      profile.roles =
        profile._json?.realm_access?.roles || ['user'];
      return done(null, profile);
    }
  )
);

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

/* ================================
   Static files
================================ */
app.use(express.static(path.join(__dirname, '../public')));

/* ================================
   Routes
================================ */
app.get('/', (req, res) => {
  if (req.isAuthenticated()) {
    return res.redirect('/dashboard');
  }
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.get('/login', passport.authenticate('oidc'));

app.get(
  '/callback',
  passport.authenticate('oidc', { failureRedirect: '/' }),
  (req, res) => {
    res.redirect('/dashboard');
  }
);

app.get('/dashboard', ensureAuth, (req, res) => {
  res.sendFile(path.join(__dirname, '../public/dashboard.html'));
});

app.get('/api/user', ensureAuth, (req, res) => {
  res.json({
    authenticated: true,
    user: {
      id: req.user.id,
      name: req.user.displayName,
      email: req.user._json?.email,
      roles: req.user.roles
    }
  });
});

app.get('/logout', (req, res) => {
  const logoutURL = `${keycloakURL}/realms/${realm}/protocol/openid-connect/logout?redirect_uri=http://localhost:3000`;
  req.logout(() => {
    res.redirect(logoutURL);
  });
});

/* ================================
   Auth middleware
================================ */
function ensureAuth(req, res, next) {
  if (req.isAuthenticated()) return next();
  res.redirect('/login');
}

/* ================================
   Server
================================ */
app.listen(PORT, () => {
  console.log(`✅ Dummy app running on http://localhost:${PORT}`);
});
