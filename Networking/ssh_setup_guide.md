---
layout: default
title: SSH Setup Guide
parent: Networking
nav_order: 3
---

# SSH Server Setup and Connection Guide

This guide covers the basic steps to install an SSH server, configure it for security, and connect to it from a client.

## 1. Server-Side Installation

On Ubuntu/Debian-based systems:

```bash
sudo apt update
sudo apt install openssh-server
```

### Verify Status
```bash
sudo systemctl status ssh
```

## 2. Basic Configuration

The main configuration file is located at `/etc/ssh/sshd_config`.

### Common Security Hardening
Before making changes, back up the original file:
```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
```

Edit the file:
```bash
sudo nano /etc/ssh/sshd_config
```

Recommended changes:
- **Change Default Port:** `Port 2222` (Reduces automated script attacks)
- **Disable Root Login:** `PermitRootLogin no`
- **Key-Based Auth Only:** `PasswordAuthentication no`

### Apply Changes
```bash
sudo systemctl restart ssh
```

## 3. Firewall Configuration (UFW)

If using UFW, allow the SSH port:

```bash
sudo ufw allow ssh
# OR if you changed the port:
sudo ufw allow 2222/tcp
```

## 4. Connecting to the Server

### Basic Password Connection
```bash
ssh username@server_ip_address
```

### Connection with Custom Port
```bash
ssh -p 2222 username@server_ip_address
```

## 5. SSH Key Authentication (Recommended)

### Generate Keys on Client
```bash
ssh-keygen -t ed25519
```

### Copy Key to Server
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@server_ip_address
```

---

## 6. Common SSH Commands and Usages

### Execute a Remote Command (Without Logging In)
```bash
ssh username@server_ip_address "df -h"
```

### Copy Files (SCP)
- **Local to Server:**
  ```bash
  scp local_file.txt username@server_ip_address:/home/username/
  ```
- **Server to Local:**
  ```bash
  scp username@server_ip_address:/path/to/remote_file.txt /local/path/
  ```
- **Directory (Recursive):**
  ```bash
  scp -r local_dir username@server_ip_address:/remote/path/
  ```

### SSH Config File (`~/.ssh/config`)
Avoid typing the full IP and port every time by creating an alias on your **client machine**:
```bash
nano ~/.ssh/config
```
Add an entry:
```text
Host myserver
    HostName 192.168.1.50
    User colton
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
```
Now you can connect simply with: `ssh myserver`

### SSH Port Forwarding (SSH Tunnel)
Expose a remote service (like a Web UI on port 8080) to your local machine:
```bash
ssh -L 9000:localhost:8080 username@server_ip_address
```
Now you can visit `http://localhost:9000` in your browser to access the remote service.

### List Active SSH Sessions (On Server)
```bash
who
# OR
w
```

### Terminate All Other SSH Sessions
```bash
sudo pkill -u username -t pts/1
```
