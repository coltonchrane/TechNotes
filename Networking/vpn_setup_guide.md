---
layout: default
title: VPN Setup Guide
parent: Networking
nav_order: 4
---

# VPN Setup and Connection Guide (WireGuard)

WireGuard is a modern, high-performance VPN that is easier to configure than OpenVPN or IPsec. This guide focuses on WireGuard for its simplicity and speed.

## 1. Deployment via Docker (Recommended)

Using `wg-easy` is the simplest way to manage WireGuard via a Web UI.

### Docker Compose Configuration
Create a `docker-compose.yml` file:

```yaml
services:
  wg-easy:
    environment:
      # Change this to your WAN IP or Dynamic DNS hostname
      - WG_HOST=vpn.example.com
      # Optional: Password for the Web UI
      - PASSWORD=your_secure_password
    image: ghcr.io/wg-easy/wg-easy
    container_name: wg-easy
    volumes:
      - ./.etc-wireguard:/etc/wireguard
    ports:
      - "51820:51820/udp"
      - "51821:51821/tcp"
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
      - net.ipv4.ip_forward=1
```

### Start the Container
```bash
docker compose up -d
```
Access the UI at `http://your-server-ip:51821` to create client profiles and download `.conf` files or scan QR codes.

---

## 2. Deployment on LXC (Proxmox/Standard)

For a lightweight standalone instance, LXCs are ideal.

### Preparation
On the **Host** (if using Proxmox), ensure the WireGuard module is available and the container has `nesting` and `keyctl` enabled.

### Inside the LXC
1. **Install WireGuard:**
   ```bash
   sudo apt update && sudo apt install wireguard -y
   ```

2. **Generate Keys:**
   ```bash
   umask 077
   wg genkey | tee privatekey | wg pubkey > publickey
   ```

3. **Configure the Interface (`/etc/wireguard/wg0.conf`):**
   ```ini
   [Interface]
   PrivateKey = <Server_Private_Key>
   Address = 10.0.0.1/24
   ListenPort = 51820
   PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

   [Peer]
   PublicKey = <Client_Public_Key>
   AllowedIPs = 10.0.0.2/32
   ```

4. **Enable IP Forwarding:**
   Edit `/etc/sysctl.conf` and uncomment:
   `net.ipv4.ip_forward=1`
   Then apply: `sudo sysctl -p`

5. **Start WireGuard:**
   ```bash
   sudo systemctl enable --now wg-quick@wg0
   ```

---

## 3. Connecting to the VPN

### Mobile (Android/iOS)
1. Download the WireGuard app.
2. If using `wg-easy`, scan the QR code generated in the Web UI.
3. Toggle "On".

### Desktop (Windows/macOS/Linux)
1. Install the WireGuard client.
2. Import the `.conf` file provided by your server.
3. Click "Activate".

---

## 4. Key Concepts & Troubleshooting

### Port Forwarding
You **must** forward **UDP port 51820** on your router to the internal IP of your Docker host or LXC.

### Split Tunneling vs. Full Tunnel
- **Full Tunnel:** Set `AllowedIPs = 0.0.0.0/0` in the client config. All traffic goes through the VPN.
- **Split Tunnel:** Set `AllowedIPs = 10.0.0.0/24, 192.168.1.0/24`. Only traffic destined for your home network goes through the VPN; internet browsing stays local.

### Kill Switch
WireGuard clients often have a "Block untunneled traffic" option. Enable this to ensure no data leaks if the VPN connection drops.

### Dynamic DNS (DDNS)
If your home IP changes, use a service like DuckDNS or Cloudflare with a DDNS script so your `WG_HOST` always points to the correct location.
