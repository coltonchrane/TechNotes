---
layout: default
title: Configuring a Custom Domain for GitHub Pages
parent: GitHub
nav_order: 2
---

# Configuring a Custom Domain for GitHub Pages

This guide provides a comprehensive walkthrough for setting up a custom domain for your GitHub Pages site, covering DNS configuration, repository settings, and security enforcement.

## 1. Determining Your Domain Type
Before configuring your settings, you must identify whether you are using an apex domain or a subdomain.

### 1.1 Apex Domains
An apex domain is the root of your domain without a prefix (e.g., `example.com`). Configuring an apex domain typically requires managing `A` records.

### 1.2 Subdomains
A subdomain includes a prefix before the root domain (e.g., `www.example.com` or `blog.example.com`). These are typically managed via `CNAME` records.

## 2. Configuring DNS Records at Your Registrar
You must update your DNS settings through your domain provider (such as GoDaddy, Namecheap, or Route 53).

### 2.1 Setting up an Apex Domain
To point your apex domain to GitHub Pages, create four `A` records pointing to the following IP addresses:
```text
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

### 2.2 Setting up a Subdomain
To point a subdomain to GitHub, create a `CNAME` record that points your chosen subdomain to your default GitHub Pages URL:
```text
Type: CNAME
Host: www
Target: <username>.github.io
```

## 3. Configuring the GitHub Repository
After updating your DNS records, you must register the domain in your repository settings so GitHub knows which site to serve.

### 3.1 Updating Pages Settings
1. Navigate to your repository on GitHub.
2. In the sidebar, click **Settings**.
3. In the "Code and automation" section, click **Pages**.
4. Under **Custom domain**, enter your domain name (e.g., `example.com`) and click **Save**.

### 3.2 Verification Process
GitHub will automatically run a DNS check. Note that DNS propagation can take up to 24 hours, though it typically completes much faster. If the check fails, verify your records using a tool like `dig` or `nslookup`.

## 4. Securing Your Site with HTTPS
GitHub Pages supports HTTPS for custom domains, providing encryption and improved SEO for your site.

### 4.1 Enforcing HTTPS
Once your DNS records are verified and your certificate is issued, navigate back to the **Pages** settings and check the **Enforce HTTPS** box. If the option is greyed out, wait a few minutes for the TLS certificate to finish generating and try refreshing the page.

---
**Source:** [GitHub Issue #17](https://github.com/coltonchrane/TechNotes/issues/17) | **Contributor:** @coltonchrane