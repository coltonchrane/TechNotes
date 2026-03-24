---
layout: default
title: Ubuntu 25 Cleanup
parent: Disk Management
nav_order: 3
---

# Ubuntu 25.04 Disk Cleanup Guide

This guide covers methods to reclaim disk space by removing unnecessary packages, caches, and logs.

## 1. System Package Cleanup (APT)
Ubuntu uses `apt` for package management. Over time, cached installers and old dependencies accumulate.

- **Remove unnecessary dependencies:**
  ```bash
  sudo apt autoremove --purge
  ```
- **Clear the local repository of retrieved package files:**
  ```bash
  sudo apt clean
  ```
- **Check how much space APT is using:**
  ```bash
  du -sh /var/cache/apt/archives
  ```

## 2. Snap Package Management
Snaps often keep multiple versions of the same application, consuming significant space.

- **List snaps and their versions:**
  ```bash
  snap list --all
  ```
- **Reduce the number of old versions kept (default is 3, minimum is 2):**
  ```bash
  sudo snap set system refresh.retain=2
  ```
- **Manually remove "disabled" snaps:**
  ```bash
  # This script removes old versions of snaps
  set -eu
  snap list --all | awk '/disabled/{print $1, $3}' |
      while read snapname revision; do
          sudo snap remove "$snapname" --revision="$revision"
      done
  ```

## 3. Log File Management
System logs can grow indefinitely if not managed.

- **Check journal log size:**
  ```bash
  journalctl --disk-usage
  ```
- **Vacuum logs older than 3 days:**
  ```bash
  sudo journalctl --vacuum-time=3d
  ```
- **Limit logs to a specific size (e.g., 500MB):**
  ```bash
  sudo journalctl --vacuum-size=500M
  ```

## 4. User Cache and Temp Files
- **Clear Thumbnail Cache:**
  ```bash
  rm -rf ~/.cache/thumbnails/*
  ```
- **Find large files/directories:**
  Install `ncdu` for an interactive disk usage analyzer:
  ```bash
  sudo apt install ncdu
  ncdu /
  ```

---

# Automation

The best way to automate this is via a custom shell script triggered by a **systemd timer** or a **cron job**.

### Recommended Automation Script (`/usr/local/bin/sys-cleanup.sh`)
```bash
#!/bin/bash
# Perform system maintenance
apt-get autoremove -y
apt-get clean
journalctl --vacuum-time=7d
# Clean old snap versions
snap list --all | awk '/disabled/{print $1, $3}' | while read snapname revision; do
    snap remove "$snapname" --revision="$revision"
done
```

### Scheduling with Cron
To run this weekly, add it to root's crontab:
1. `sudo crontab -e`
2. Add: `0 0 * * 0 /usr/local/bin/sys-cleanup.sh`

### GUI Option: BleachBit
For an automated GUI experience, **BleachBit** is the industry standard.
- **Install:** `sudo apt install bleachbit`
- **Automation:** It supports a CLI mode (`bleachbit --clean system.apt_cache`) which can also be scripted.
