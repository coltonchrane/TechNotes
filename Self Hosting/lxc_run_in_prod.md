# Ubuntu Production Deployment Guide (LXC on Proxmox)
**Environment:** Ubuntu 24.04 LXC | Residential ISP

**Stack:** React + Kotlin Micronaut + PostgreSQL

---

## 1. LXC Provisioning (Proxmox Host)
Run these on your Proxmox Host to create the containers using Ubuntu 24.04:

```bash
# Update templates and download Ubuntu 24.04
pveam update
pveam download local ubuntu-24.04-standard_24.04-1_amd64.tar.zst

# Database (2GB RAM, 16GB Disk)
pct create 200 local:vztmpl/ubuntu-24.04-standard_24.04-1_amd64.tar.zst --hostname pg-db --memory 2048 --net0 name=eth0,bridge=vmbr0,ip=dhcp --rootfs local:16 --unprivileged 1
# Backend (2GB RAM, 10GB Disk)
pct create 201 local:vztmpl/ubuntu-24.04-standard_24.04-1_amd64.tar.zst --hostname kt-backend --memory 2048 --net0 name=eth0,bridge=vmbr0,ip=dhcp --rootfs local:10 --unprivileged 1
# Frontend/Nginx (1GB RAM, 8GB Disk)
pct create 202 local:vztmpl/ubuntu-24.04-standard_24.04-1_amd64.tar.zst --hostname react-frontend --memory 1024 --net0 name=eth0,bridge=vmbr0,ip=dhcp --rootfs local:8 --unprivileged 1
# Cloudflare Tunnel (512MB RAM, 2GB Disk)
pct create 203 local:vztmpl/ubuntu-24.04-standard_24.04-1_amd64.tar.zst --hostname cf-tunnel --memory 512 --net0 name=eth0,bridge=vmbr0,ip=dhcp --rootfs local:2 --unprivileged 1

# Start all
pct start 200 && pct start 201 && pct start 202 && pct start 203
```

---

## 2. Configuration by Container

### Database (LXC 200 - Ubuntu)
```bash
pct enter 200
apt update && apt install -y postgresql
# Allow connections from Backend (LXC 201)
echo "listen_addresses = '*'" >> /etc/postgresql/16/main/postgresql.conf
echo "host all all 192.168.1.0/24 md5" >> /etc/postgresql/16/main/pg_hba.conf
systemctl restart postgresql
```

### Backend: Kotlin Micronaut (LXC 201 - Ubuntu)
```bash
pct enter 201
# Install Java 17/21
apt update && apt install -y openjdk-21-jre-headless
# Deploy Micronaut JAR
# (Copy your .jar file via 'pct push 201 myapp.jar /opt/myapp.jar')
# Run as systemd service
```

### Frontend: React + Nginx (LXC 202 - Ubuntu)
```bash
pct enter 202
apt update && apt install -y nginx
# Copy build artifacts to /var/www/html
# Update /etc/nginx/sites-available/default to handle React routing and proxy /api
```

```nginx
location / {
    try_files $uri /index.html;
}

location /api/ {
    proxy_pass http://192.168.1.201:8080/; # Point to Backend LXC
}
```

### Cloudflare Tunnel (LXC 203 - Ubuntu)
```bash
pct enter 203
apt update && apt install -y curl
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
dpkg -i cloudflared.deb
# Authenticate and run:
cloudflared tunnel run --token YOUR_TOKEN
```

---

## 3. Connectivity Matrix

| Service | Hostname | Internal IP | External Route |
|---|---|---|---|
| PostgreSQL | pg-db | 192.168.1.200 | None (Internal Only) |
| Micronaut | kt-backend | 192.168.1.201 | None (Proxied by Nginx) |
| React | react-frontend | 192.168.1.202 | Proxied by Cloudflare |
| CF Tunnel | cf-tunnel | 192.168.1.203 | Outbound Gateway |

---

## 4. Production Hardening
- **Static IPs:** Assign static IPs to LXCs in Proxmox Dashboard for reliable communication between services.
- **Fail2Ban:** Install on the Nginx LXC.
- **Backups:** Use Proxmox Snapshots and `pg_dump` to an external NFS share.
