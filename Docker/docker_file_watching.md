# Implementing File Watching in Docker

This guide covers setting up hot-reloading/file-watching for a stack consisting of React, Kotlin Micronaut, and Postgres.

## 1. React (Frontend)
React (via Vite or Webpack) usually requires `CHOKIDAR_USEPOLLING=true` when running inside Docker on certain filesystems (like Windows/macOS hosts) to detect changes reliably.

### Dockerfile snippet
```dockerfile
# Use a development node image
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV CHOKIDAR_USEPOLLING=true
CMD ["npm", "run", "dev"]
```

### docker-compose.yml
```yaml
frontend:
  build: ./frontend
  volumes:
    - ./frontend:/app
    - /app/node_modules
  ports:
    - "5173:5173"
  environment:
    - CHOKIDAR_USEPOLLING=true
```

---

## 2. Kotlin Micronaut (Backend)
Micronaut supports "Continuous Execution" using the Gradle or Maven watchers.

### docker-compose.yml
Map the source code and use the `-t` (continuous) flag for Gradle.

```yaml
backend:
  build: ./backend
  volumes:
    - ./backend:/home/app
  ports:
    - "8080:8080"
  command: ./gradlew -t run
```

*Note: For Micronaut, ensure `micronaut.io.watch.enabled=true` is set in `application.yml` for development.*

---

## 3. Postgres (Database)
While Postgres doesn't "watch" files for code changes, you often want to watch initialization scripts or configuration.

### docker-compose.yml
```yaml
db:
  image: postgres:15-alpine
  volumes:
    - ./postgres/init:/docker-entrypoint-initdb.d
    - postgres_data:/var/lib/postgresql/data
  environment:
    - POSTGRES_PASSWORD=password
    - POSTGRES_DB=notes_db

volumes:
  postgres_data:
```

---

## Troubleshooting
- **Inotify Limits:** If watching many files, you might need to increase the host's inotify limit:
  `sudo sysctl -w fs.inotify.max_user_watches=524288`
- **Permissions:** Ensure the user inside the container has write access to the mounted volumes if the app generates files (like build artifacts).
