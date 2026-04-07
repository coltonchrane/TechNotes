---
layout: default
title: How to Download, Run, and Configure Tailscale
parent: Networking
nav_order: 5
---

# How to Download, Run, and Configure Tailscale

Tailscale is a zero-config VPN that creates a secure mesh network between your devices using the WireGuard protocol. This guide provides a step-by-step walkthrough for installing, authenticating, and managing Tailscale across different environments.

## 1. Installation

Tailscale supports a wide variety of platforms. Depending on your operating system, use one of the following methods to install the client.

### Linux (Standard Installation)
The most efficient way to install Tailscale on Linux is using the official one-line script, which handles repository addition and package installation automatically.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

### macOS and Windows
For desktop operating systems, it is recommended to use the graphical installers:
- **macOS:** Download from the Mac App Store or use the standalone `.pkg` from the official website.
- **Windows:** Download and run the `.msi` installer from the Tailscale download page.

## 2. Running and Authenticating

After installation, the Tailscale service needs to be started and linked to your Tailnet (your private network).

### Starting the Service on Linux
Use the following command to bring the Tailscale interface up:

```bash
sudo tailscale up
```

### Completing Authentication
When you run the `up` command for the first time, a login URL will be generated in your terminal. Copy this link into your web browser and sign in using your SSO provider (such as Google, Microsoft, or GitHub). Once authenticated, your device will be assigned a unique internal IP address (100.x.y.z).

## 3. Configuration and Advanced Features

Tailscale offers powerful features beyond simple connectivity that can be configured directly from the command line.

### Setting Up an Exit Node
If you want to route your internet traffic through a specific machine (e.g., to access the web from a trusted home connection while on public Wi-Fi), you can configure a machine as an exit node.

**To advertise as an exit node:**
```bash
sudo tailscale up --advertise-exit-node
```

**To use an exit node on a client:**
```bash
sudo tailscale up --exit-node=<exit-node-ip-or-hostname>
```

### Enabling Tailscale SSH
Tailscale can manage SSH authentication for you, allowing you to SSH into machines on your Tailnet without managing manual SSH keys.

```bash
sudo tailscale up --ssh
```

## 4. Managing the Network

### Checking Connection Status
To view all devices currently connected to your Tailnet and their respective IP addresses, use the status command:

```bash
tailscale status
```

### Disconnecting and Stopping
If you need to disconnect from the network without uninstalling the software, use the `down` command:

```bash
sudo tailscale down
```

---
**Source:** [GitHub Issue #51](https://github.com/coltonchrane/AutoNotes/issues/51) | **Contributor:** @coltonchrane