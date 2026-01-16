# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

# Runtime stage
FROM node:18-alpine
WORKDIR /app

# Copier les dépendances et fichiers de la build
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Copier server.js et public/ (pas de src/)
COPY server.js ./
COPY public ./public

# Exposer le port
EXPOSE 3000

# Lancer l'app
CMD ["node", "server.js"]
