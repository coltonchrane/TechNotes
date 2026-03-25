---
layout: default
title: Powerlevel10k (p10k) Quick Reference Guide
parent: Zsh
nav_order: 1
---

# Powerlevel10k (p10k) Quick Reference Guide

Powerlevel10k (p10k) is a high-performance Zsh theme that provides detailed context directly in your terminal prompt. This guide serves as a reference for interpreting Git status symbols and managing theme configuration.

## 1. Prerequisites and Font Setup

To ensure all symbols and icons render correctly, you must install a Nerd Font. Powerlevel10k specifically recommends **MesloLGS NF**.

### Font Troubleshooting
If icons appear as question marks (`?`), boxes, or generic symbols, it is likely that the required font is not installed or the terminal application is not configured to use it. After installing the font, ensure your terminal emulator (e.g., iTerm2, Windows Terminal, Alacritty) has it selected in the font settings.

## 2. Configuration and Customization

### The Configuration Wizard
The easiest way to configure the theme is through the interactive configuration wizard. It allows you to choose styles such as *Lean*, *Classic*, or *Rainbow*.

```bash
p10k configure
```

### Manual Configuration
You can manually modify your prompt by editing the `~/.p10k.zsh` configuration file. This file allows you to change specific icons, colors, and behaviors.

```zsh
# Example: Manually changing the unstaged changes indicator icon
typeset -g POWERLEVEL9K_VCS_UNSTAGED_ICON='! '
```

## 3. Git Status Symbols Reference

When working within a Git repository, p10k uses specific indicators to represent the current state of your code and branch.

### Repository Context
- **Branch Icon**: Typically a specific branch symbol or the Unicode character `\uE220` ().
- **Repository Origin**: Icons for specific hosting services (such as the GitHub cat icon) are displayed if the remote URL matches a known provider.
- **merge**: Indicates the repository is in an unusual state, such as an active merge, rebase, or cherry-pick.

### Commit Tracking
- **⇣42**: The local branch is **behind** the remote by 42 commits.
- **⇡42**: The local branch is **ahead** of the remote by 42 commits.
- ***42**: There are 42 stashes currently stored.

### File and Change Indicators
- **~42**: There are 42 **merge conflicts** that need resolution.
- **+42**: There are 42 **staged** changes ready to be committed.
- **! 42**: There are 42 **unstaged** changes in the working directory.
- **? 42**: There are 42 **untracked** files.

---
**Source:** [GitHub Issue #31](https://github.com/coltonchrane/TechNotes/issues/31) | **Contributor:** @coltonchrane