---
layout: default
title: Docker Cleanup Guide
parent: Docker
nav_order: 1
---

# Docker Disk Space Management Guide

Docker can quickly consume significant disk space with old images, stopped containers, and unused volumes. This guide covers how to clean up and manage Docker's footprint.

## 1. Quick Cleanup (The "Nuclear" Option)

The easiest way to reclaim space is the `system prune` command.

### Basic Prune
Removes dangling images, stopped containers, unused networks, and build cache.
```bash
docker system prune
```

### Thorough Prune
Removes **all** unused images (not just dangling ones) and all unused volumes. **Use with caution.**
```bash
docker system prune -a --volumes
```

---

## 2. Targeted Cleanup

If you want to keep certain types of data, use specific prune commands:

- **Images:** `docker image prune` (add `-a` for all unused images).
- **Containers:** `docker container prune` (removes all stopped containers).
- **Volumes:** `docker volume prune` (removes all unattached volumes).
- **Build Cache:** `docker builder prune`.

---

## 3. Managing Log Sizes

Docker container logs can grow indefinitely if not capped. You can limit them globally by editing (or creating) `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```
*Note: This requires a Docker service restart: `sudo systemctl restart docker`.*

---

## 4. Monitoring Usage

To see exactly what is taking up space:
```bash
docker system df
```
For more detail:
```bash
docker system df -v
```

---

## 5. Automated Maintenance

Consider adding a cron job to run a basic prune weekly:
1. Run `crontab -e`.
2. Add this line:
   ```bash
   0 0 * * 0 /usr/bin/docker system prune -f
   ```
   *(This runs every Sunday at midnight).*
