---
layout: default
title: Configuring a Custom Domain for GitHub Pages
parent: GitHub
nav_order: 2
---

# Configuring a Custom Domain for GitHub Pages

This guide provides a comprehensive walkthrough for setting up a custom domain for your GitHub Pages site, covering domain verification, DNS configuration, and security enforcement.

## 1. Understanding DNS Management and GitHub
A common question is whether GitHub can manage DNS records directly. **GitHub is not a DNS provider.** While GitHub hosts your website's content, you must use a third-party domain registrar (such as GoDaddy, Namecheap, or Route 53) to manage your DNS records. 

However, GitHub provides a **Domain Verification** feature at the account or organization level. Verifying your domain with GitHub ensures that other users cannot use your domain for their own Pages sites and speeds up the configuration process for individual repositories.

## 2. Verifying Your Domain (Account Level)
Before configuring specific repositories, it is recommended to verify ownership of your domain within your GitHub account settings.

1. In the upper-right corner of any page, click your profile photo, then click **Settings**.
2. In the "Code, planning, and automation" section of the sidebar, click **Pages**.
3. Click **Add a domain**.
4. Enter the domain you want to verify and click **Add domain**.
5. Follow the instructions to create a `TXT` record in your DNS configuration to prove ownership.
6. Once the `TXT` record propagates, click **Verify**.

## 3. Configuring DNS Records at Your Registrar
You must point your domain to GitHub’s servers by updating your DNS settings at your registrar.

### 3.1 Setting up an Apex Domain
To point an apex domain (e.g., `example.com`) to GitHub Pages, create four `A` records pointing to the following IP addresses:
```text
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

### 3.2 Setting up a Subdomain
To point a subdomain (e.g., `www.example.com`) to GitHub, create a `CNAME` record:
- **Type:** `CNAME`
- **Host:** `www` (or your chosen prefix)
- **Target:** `<username>.github.io` (The target must be your GitHub Pages default URL, not the apex domain).

## 4. Configuring the GitHub Repository
After your DNS records are set, you must link the domain to your specific repository.

### 4.1 Updating Pages Settings
1. Navigate to your repository on GitHub.
2. Click **Settings** > **Pages**.
3. Under **Custom domain**, enter your domain name and click **Save**.
4. GitHub will automatically create a `CNAME` file in the root of your repository (if using the `gh-pages` branch or root folder) to store this configuration.

### 4.2 DNS Check and Propagation
GitHub will perform a DNS check. Note that DNS propagation can take up to 24 hours. You can monitor progress using the `dig` command in your terminal:
```bash
dig example.com +nostats +nocomments +nocmd
```

## 5. Securing Your Site with HTTPS
GitHub provides automatic TLS certificates through Let's Encrypt for custom domains.

### 5.1 Enforcing HTTPS
1. In your repository's **Pages** settings, locate the **Enforce HTTPS** checkbox.
2. If the option is unavailable, the certificate is likely still being provisioned. This usually takes 15–60 minutes after DNS verification.
3. Once available, check the box to ensure all traffic is encrypted.

---
**Source:** [GitHub Issue #17](https://github.com/coltonchrane/AutoNotes/issues/17) | **Contributor:** @coltonchrane
---