---
layout: default
title: Flashing Ubuntu 25 on a Dell Laptop
parent: Linux
nav_order: 2
---

# Flashing Ubuntu 25 on a Dell Laptop

This guide provides a comprehensive walkthrough for installing Ubuntu 25 on Dell laptop hardware, with a specific focus on the critical BIOS configurations required for a successful installation and optimal hardware performance.

## 1. Prerequisites

Before starting the process, ensure you have prepared the following:
- **USB Drive:** At least 12GB of capacity (all data on it will be erased).
- **ISO Image:** The Ubuntu 25 ISO image from the [official Ubuntu releases page](https://releases.ubuntu.com/).
- **Power:** Ensure the laptop is connected to an AC power source to prevent shutdown during BIOS changes or installation.
- **Backup:** Perform a full backup of your existing data. Switching storage modes can render existing Windows installations unbootable.

## 2. Creating the Bootable Media

Choose one of the following methods to prepare your installation media.

### 2.1 Using BalenaEtcher (GUI)
1. Download and launch [BalenaEtcher](https://www.balena.io/etcher/).
2. Select the downloaded Ubuntu 25 ISO.
3. Select your target USB drive.
4. Click **Flash!** and authenticate if prompted.

### 2.2 Using Terminal (CLI)
Identify your USB drive path using `lsblk` (e.g., `/dev/sdb`). **Warning:** Ensure you target the correct device to avoid data loss on your host system.
```bash
# Replace /dev/sdX with your actual USB device path
sudo dd if=ubuntu-25-desktop-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

## 3. Configuring Dell BIOS Settings

Dell laptops utilize specific proprietary configurations that must be adjusted for Linux compatibility.

### 3.1 Accessing the BIOS
1. Restart your laptop.
2. Repeatedly tap the **F2** key at the Dell logo screen.

### 3.2 Storage Configuration (SATA/NVMe Mode)
Dell often ships with "RAID On" enabled via Intel RST. Ubuntu requires **AHCI** mode to properly communicate with the NVMe/SATA controller.
1. Navigate to **System Configuration** > **SATA Operation**.
2. Select **AHCI**. 
3. *Note:* If you intend to dual-boot, you must configure Windows for AHCI before making this change.

### 3.3 Secure Boot
Ubuntu 25 supports Secure Boot, but disabling it is often recommended to ensure third-party drivers (like Nvidia or specialized Wi-Fi cards) load correctly.
1. Navigate to **Secure Boot** > **Secure Boot Enable**.
2. Select **Disabled**.

### 3.4 Fast Boot
1. Navigate to **POST Behavior** > **Fastboot**.
2. Set it to **Thorough**. This ensures the system initializes all hardware and USB controllers fully before passing control to the bootloader.

## 4. Booting and Installing

1. Insert the prepared USB drive and restart.
2. Tap **F12** repeatedly to enter the **One-Time Boot Menu**.
3. Select your USB drive under **UEFI Boot**.
4. In the GRUB menu, select **Try or Install Ubuntu**.
5. Follow the installation wizard. When prompted for "Installation Type," selecting **Erase disk and install Ubuntu** is recommended for a clean experience on the new AHCI configuration.

## 5. Post-Installation Steps

Once the installation is complete and the system reboots, perform these final steps:

### 5.1 System Updates
Update the package index and upgrade all installed components:
```bash
sudo apt update && sudo apt upgrade -y
```

### 5.2 Firmware Updates
Dell systems support firmware updates directly through Linux. Check for BIOS/Firmware updates using:
```bash
sudo fwupdmgr get-updates
sudo fwupdmgr update
```

---
**Source:** [GitHub Issue #25](https://github.com/coltonchrane/TechNotes/issues/25) | **Contributor:** @coltonchrane
---