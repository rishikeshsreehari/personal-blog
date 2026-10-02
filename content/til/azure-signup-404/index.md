---
title: "Azure Signup 404 Error Due to Pi-hole"
date: 2026-08-19
tiltags: ["azure", "pihole", "networking", "troubleshooting"]
summary: "Azure's captcha verification can return a 404 if Pi-hole is blocking the required domains."
url: "/til/azure-captcha-pihole"
---

{{< photocaption src="azure-signup-error-404.png" alt="Azure 404 error on signup" width="80%" >}}404 Error on Azure Signup pages{{< /photocaption >}}


Today I learned that if you're trying to sign up or log in to Azure and the captcha verification page throws a 404, it might be your Pi-hole blocking the domains Azure uses for human verification.

Temporarily disabling Pi-hole (or whitelisting the relevant domains) fixed it for me.