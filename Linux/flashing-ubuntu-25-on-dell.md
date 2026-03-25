---
layout: default
title: Flashing Ubuntu 25 on a Dell Laptop
parent: Linux
nav_order: 2
---

# Flashing Ubuntu 25 on a Dell Laptop

This guide provides a comprehensive walkthrough for installing Ubuntu 25 on Dell laptop hardware, with a specific focus on the critical BIOS configurations required for a successful installation.

## 1. Prerequisites

Before starting the process, ensure you have prepared the following:
- A USB flash drive with at least 12GB of capacity.
- The Ubuntu 25 ISO image (available from the official Ubuntu releases page).
- A full backup of your existing data, as this process may involve disk formatting.

## 2. Creating the Bootable Media

To begin, you must create a bootable USB drive using the ISO file.

### 2.1 Using BalenaEtcher
1. Download and launch [BalenaEtcher](https://www.balena.io/etcher/).
2. Select the downloaded Ubuntu 25 ISO.
3. Select your USB drive.
4. Click **Flash!** and wait for the process to complete.

### 2.2 Using Terminal (CLI)
If you prefer the command line, identify your USB drive using `lsblk` and use the `dd` utility:
```bash
# Replace /dev/sdX with your actual USB device path
sudo dd if=ubuntu-25-desktop-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

## 3. Configuring Dell BIOS Settings

Dell laptops require specific BIOS/UEFI adjustments to recognize the installer and the internal storage correctly.

### 3.1 Accessing the BIOS
1. Restart your laptop.
2. Repeatedly tap the **F2** key as soon as the Dell logo appears.

### 3.2 Storage Configuration (SATA/NVMe Mode)
By default, many Dell laptops are set to 'RAID On'. Ubuntu generally requires **AHCI** mode to detect internal SSDs.
1. Navigate to **System Configuration** > **SATA Operation**.
2. Change the selection to **AHCI**.
3. Apply the changes.

### 3.3 Secure Boot
While modern Ubuntu releases support Secure Boot, disabling it during installation can prevent common driver conflicts.
1. Navigate to **Secure Boot** > **Secure Boot Enable**.
2. Select **Disabled**.

### 3.4 Fast Boot
1. Navigate to **POST Behavior** > **Fastboot**.
2. Set it to **Thorough** to ensure all USB ports and hardware are initialized before booting.

## 4. Booting and Installing

1. Insert the USB drive and restart the laptop.
2. Tap the **F12** key repeatedly to enter the **One-Time Boot Menu**.
3. Select your USB drive under the **UEFI Boot** section.
4. When the GRUB menu appears, select **Try or Install Ubuntu**.
5. Once the desktop loads, open the installer and follow the wizard instructions for partitioning and user setup.

## 5. Post-Installation Steps

After the first boot, update your system to ensure all hardware drivers are current:
```bash
sudo apt update && sudo apt upgrade -y
```

---
**Source:** [GitHub Issue #25](https://github.com/coltonchrane/AutoNotes/issues/25) | **Contributor:** @coltonchrane