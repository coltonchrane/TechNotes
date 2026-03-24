---
layout: default
title: Docker Run In Prod
parent: Networking
nav_order: 1
---

# Ubuntu Production Deployment Guide (Docker)
**Environment:** Ubuntu 22.04/24.04 LTS | Proxmox VM | Residential ISP
**Stack:** React (Vite) + Kotlin Micronaut + PostgreSQL

---

## 1. Ubuntu Host Preparation
Install Docker Engine on Ubuntu (Standard Repository):
```bash
sudo apt update && sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
# Logout and login for group changes to take effect
```

---

## 2. Connectivity: Path A vs Path B

### Path A: Public IP (Direct)
Use this if you have a public IP and can port forward 80/443.
- **DNS:** A Record → Your Public IP.
- **Reverse Proxy:** Use Nginx Proxy Manager (NPM).

### Path B: Cloudflare Tunnel (Recommended)
**No open ports required.** Best for CGNAT or security-conscious setups.
1. Create a Tunnel in [Cloudflare Zero Trust](https://one.dash.cloudflare.com/).
2. Copy your `TUNNEL_TOKEN`.

---

## 3. Production Docker Compose (`docker-compose.yml`)
This configuration uses a secure internal network and handles the full stack.

```yaml
services:
  # --- Connectivity Layer ---
  tunnel:
    image: cloudflare/cloudflared:latest
    restart: unless-stopped
    command: tunnel --no-autoupdate run --token ${TUNNEL_TOKEN}
    networks:
      - internal

  # --- Frontend: React (Nginx) ---
  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    networks:
      - internal

  # --- Backend: Kotlin Micronaut (JVM) ---
  backend:
    build: ./backend
    restart: unless-stopped
    environment:
      - MICRONAUT_ENVIRONMENTS=prod
      - DATASOURCES_DEFAULT_URL=jdbc:postgresql://db:5432/myapp
      - DATASOURCES_DEFAULT_USERNAME=user
      - DATASOURCES_DEFAULT_PASSWORD_FILE=/run/secrets/db_password
      - JAVA_OPTS=-Xmx512m -Xms256m
    secrets:
      - db_password
    depends_on:
      db:
        condition: service_healthy
    networks:
      - internal

  # --- Database: PostgreSQL ---
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal

networks:
  internal:

volumes:
  pgdata:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## 4. Stack-Specific Hardening

### React (Frontend)
Use a multi-stage `Dockerfile.prod` to serve static files efficiently:
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS build
WORKDIR /app
COPY . .
RUN npm ci && npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### Micronaut (Backend)
In your `application-prod.yml`, ensure you are using connection pooling (Hikari) and proper logging levels.

---

## 5. Summary Checklist
- [ ] **Ubuntu Firewall:** `sudo ufw allow ssh` and `sudo ufw enable`. (No 80/443 needed if using Tunnel).
- [ ] **Secrets:** Ensure `./secrets/db_password.txt` is not committed to Git.
- [ ] **Backups:** Use `docker exec db pg_dumpall` for scheduled backups.
