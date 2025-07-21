---
title: "How to Access Google Drive in WSL2"
date: 2025-07-21
tiltags: ["programming", "wsl", "windows", "linux", "troubleshooting"]
summary: "When installing bike pedals, the left pedal is reverse threaded - turn clockwise to loosen, counterclockwise to tighten."
url: "/til/google-drive-wsl"
---

Today I learned that Google Drive doesn't auto-mount in WSL2 like regular Windows drives. Even though `ls /mnt/g/` showed my Google Drive folder, I couldn't access anything inside it.

The fix:

```
sudo mount -t drvfs G: /mnt/g
cd "/mnt/g/My Drive"

```

WSL2 needs you to manually mount network/virtual drives using drvfs. After mounting, all my Google Drive files were accessible normally.

Simple solution, but took way too long to figure out!

Took way too long to figure out thanks to LLM hallucinations - sometimes [Stack Exchange](https://superuser.com/questions/1781174/google-drive-in-wsl) is still to the rescue! 🤦‍♂️



---

