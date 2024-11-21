---

title: "Changelog"
#layout: "library"
url: "/log/"
summary: Changelog of rishikeshs.com adhering to the Personal Blog Versioning Manifesto
disable_comments: true
ShowReadingTime: false
---
This blog adheres to the *Personal Blog Versioning Manifesto*. All changes and commits to this blog are versioned using a structured format and displayed in reverse chronological order.

```
  Version Format: YY.Push.Type.DDMM

  24.50.M.1904
  │  │   │   └── Type: Nature of change (e.g., M - Multiple, U - Update, F - Fixes, etc.)
  │  │   └────── Date: DDMM format (19th April in this example)
  │  └────────── Push: Sequential counter (reset to 0 at the beginning of each year)
  └─────────── Year: Current year (last two digits)

```
The Push counter is particularly useful for tracking the number of changes made in a given year, resetting to zero at the start of each year. This ensures a clear view of the blog’s yearly activity.

For example:

- v24.625.M.2111: The 625th change made in 2024, recorded on November 21st.
- v24.626.M.2111: The 626th change made in 2024, logged later on the same day with mixed updates, including fixes, updates, and new features.

These changelogs are generated automatically using [`pre_push.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py) triggered by a [pre-push](https://github.com/rishikeshsreehari/personal-blog/blob/main/hooks/pre-push) hook.

<!--LOG_PLACEHOLDER_START-->
### **v24.628.M.2111** (2024-11-21)

#### **Fixes**

1. **Fixed formatting issues in watch/kishkindha**  
   - *Commit:* [`a491c7f`](https://github.com/rishikeshsreehari/personal-blog/commit/a491c7f)  
   - *Files:*  
     1. [`content/watch/kishkindha.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/watch/kishkindha.md)
     2. [`content/watch/meyyazhakan.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/watch/meyyazhakan.md)

2. **Spelling fix on log**  
   - *Commit:* [`4526b6a`](https://github.com/rishikeshsreehari/personal-blog/commit/4526b6a)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)


#### **Updations**

1. **Updated link in footer for logs**  
   - *Commit:* [`a1eb04e`](https://github.com/rishikeshsreehari/personal-blog/commit/a1eb04e)  
   - *Files:*  
     1. [`themes/hugo-PaperMod/layouts/partials/footer.html`](https://github.com/rishikeshsreehari/personal-blog/blob/main/themes/hugo-PaperMod/layouts/partials/footer.html)

2. **Updated file over app with new additions**  
   - *Commit:* [`31792db`](https://github.com/rishikeshsreehari/personal-blog/commit/31792db)  
   - *Files:*  
     1. [`content/blog/file-over-app/index.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/blog/file-over-app/index.md)


---
### **v24.627.M.2111** (2024-11-21)

#### **Fixes**

1. **Spelling correction in changelog**  
   - *Commit:* [`8b1b25a`](https://github.com/rishikeshsreehari/personal-blog/commit/8b1b25a)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)


#### **Updations**

1. **Updated now page**  
   - *Commit:* [`3e4c7a0`](https://github.com/rishikeshsreehari/personal-blog/commit/3e4c7a0)  
   - *Files:*  
     1. [`content/now.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/now.md)

2. **Updated colophon**  
   - *Commit:* [`fd28466`](https://github.com/rishikeshsreehari/personal-blog/commit/fd28466)  
   - *Files:*  
     1. [`content/colophon.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/colophon.md)

3. **Updated log page**  
   - *Commit:* [`843c220`](https://github.com/rishikeshsreehari/personal-blog/commit/843c220)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)


---
### **v24.626.M.2111** (2024-11-21)

#### **Fixes**

1. **Formatting issue in watch/kishkindha**  
   - *Commit:* [`bbb631a`](https://github.com/rishikeshsreehari/personal-blog/commit/bbb631a)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)
     2. [`content/watch/kishkindha.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/watch/kishkindha.md)


#### **Updations**

1. **Updated changelog format in prepush.py**  
   - *Commit:* [`4829739`](https://github.com/rishikeshsreehari/personal-blog/commit/4829739)  
   - *Files:*  
     1. [`scripts/pre_push.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py)

2. **Updated log with latest format**  
   - *Commit:* [`c35ccb2`](https://github.com/rishikeshsreehari/personal-blog/commit/c35ccb2)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)


---
### **v24.625.M.2111** (2024-11-21)

#### **Additions**
1. **Added setup-hooks.ch**  
   - *Commit:* [`2526007`](https://github.com/rishikeshsreehari/personal-blog/commit/2526007)  
   - *Files:*  
     1. [`setup-hooks.ch`](https://github.com/rishikeshsreehari/personal-blog/blob/main/setup-hooks.ch)  

#### **Updations**
1. **Updated Readme**  
   - *Commit:* [`69c52f5`](https://github.com/rishikeshsreehari/personal-blog/commit/69c52f5)  
   - *Files:*  
     1. [`README.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/README.md)  

2. **Updated gitignore to exclude some files**  
   - *Commit:* [`04a55e9`](https://github.com/rishikeshsreehari/personal-blog/commit/04a55e9)  
   - *Files:*  
     1. [`.gitignore`](https://github.com/rishikeshsreehari/personal-blog/blob/main/.gitignore)  

3. **Updated hooks location**  
   - *Commit:* [`89a9f22`](https://github.com/rishikeshsreehari/personal-blog/commit/89a9f22)  
   - *Files:*  
     1. [`hooks/pre-push`](https://github.com/rishikeshsreehari/personal-blog/blob/main/hooks/pre-push)  

#### **Removals**
1. **Updated gitignore to remove some files**  
   - *Commit:* [`59f7d20`](https://github.com/rishikeshsreehari/personal-blog/commit/59f7d20)  
   - *Files:*  
     1. [`.hugo_build.lock`](https://github.com/rishikeshsreehari/personal-blog/blob/main/.hugo_build.lock)  
     2. [`.vscode/settings.json`](https://github.com/rishikeshsreehari/personal-blog/blob/main/.vscode/settings.json)  

2. **Removed link_update.txt**  
   - *Commit:* [`1740506`](https://github.com/rishikeshsreehari/personal-blog/commit/1740506)  
   - *Files:*  
     1. [`link_update.txt`](https://github.com/rishikeshsreehari/personal-blog/blob/main/link_update.txt)  

3. **Removed netlify.toml**  
   - *Commit:* [`00e923e`](https://github.com/rishikeshsreehari/personal-blog/commit/00e923e)  
   - *Files:*  
     1. [`README.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/README.md)  
     2. [`netlify.toml`](https://github.com/rishikeshsreehari/personal-blog/blob/main/netlify.toml)  

---

### **v24.624.U.2111** (2024-11-21)

#### **Updations**
1. **Updated hooks location**  
   - *Commit:* [`89a9f22`](https://github.com/rishikeshsreehari/personal-blog/commit/89a9f22)  
   - *Files:*  
     1. [`hooks/pre-push`](https://github.com/rishikeshsreehari/personal-blog/blob/main/hooks/pre-push)  

---

### **v24.623.M.2111** (2024-11-21)

#### **Fixes**
1. **Fixed a CF link issue in footer**  
   - *Commit:* [`4faabe3`](https://github.com/rishikeshsreehari/personal-blog/commit/4faabe3)  
   - *Files:*  
     1. [`themes/hugo-PaperMod/layouts/partials/footer.html`](https://github.com/rishikeshsreehari/personal-blog/blob/main/themes/hugo-PaperMod/layouts/partials/footer.html)  

#### **Updations**
1. **Updated footer with log page hyperlinked**  
   - *Commit:* [`0c70178`](https://github.com/rishikeshsreehari/personal-blog/commit/0c70178)  
   - *Files:*  
     1. [`themes/hugo-PaperMod/layouts/partials/footer.html`](https://github.com/rishikeshsreehari/personal-blog/blob/main/themes/hugo-PaperMod/layouts/partials/footer.html)  

---

### **v24.622.U.2111** (2024-11-21)

#### **Updations**
1. **Updated simplified workflow with production branch removed**  
   - *Commit:* [`a4e5ecc`](https://github.com/rishikeshsreehari/personal-blog/commit/a4e5ecc)  
   - *Files:*  
     1. [`.github/workflows/build.yml`](https://github.com/rishikeshsreehari/personal-blog/blob/main/.github/workflows/build.yml)  

2. **Removed update_version.py from build.py**  
   - *Commit:* [`d56ef4d`](https://github.com/rishikeshsreehari/personal-blog/commit/d56ef4d)  
   - *Files:*  
     1. [`scripts/build.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/build.py)  

---

### **v24.621.M.2111** (2024-11-21)

#### **Updations**
1. **Updated pre_push.py GUI**  
   - *Commit:* [`0d931ee`](https://github.com/rishikeshsreehari/personal-blog/commit/0d931ee)  
   - *Files:*  
     1. [`scripts/pre_push.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py)  

2. **Updated changlog**  
   - *Commit:* [`b032130`](https://github.com/rishikeshsreehari/personal-blog/commit/b032130)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)  

#### **Removals**
1. **Removed notes.md**  
   - *Commit:* [`bcc12c4`](https://github.com/rishikeshsreehari/personal-blog/commit/bcc12c4)  
   - *Files:*  
     1. [`notes.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/notes.md)  

---

### **v24.620.M.2111** (2024-11-21)

#### **Fixes**
1. **Fixed commit hash issue in footer**  
   - *Commit:* [`d108110`](https://github.com/rishikeshsreehari/personal-blog/commit/d108110)  
   - *Files:*  
     1. [`themes/hugo-PaperMod/layouts/partials/footer.html`](https://github.com/rishikeshsreehari/personal-blog/blob/main/themes/hugo-PaperMod/layouts/partials/footer.html)  

2. **Removed unnecessary files**  
   - *Commit:* [`15daf29`](https://github.com/rishikeshsreehari/personal-blog/commit/15daf29)  
   - *Files:*  
     1. [`hook.log`](https://github.com/rishikeshsreehari/personal-blog/blob/main/hook.log)  
     2. [`hook_debug.log`](https://github.com/rishikeshsreehari/personal-blog/blob/main/hook_debug.log)  
     3. [`push.txt`](https://github.com/rishikeshsreehari/personal-blog/blob/main/push.txt)  
     4. [`scripts/git_hooks.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/git_hooks.py)  
     5. [`scripts/update_version.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/update_version.py)  

#### **Updations**
1. **Updated config.yml**  
   - *Commit:* [`4245b37`](https://github.com/rishikeshsreehari/personal-blog/commit/4245b37)  
   - *Files:*  
     1. [`config.yml`](https://github.com/rishikeshsreehari/personal-blog/blob/main/config.yml)  

2. **Added removal type in pre_push.py**  
   - *Commit:* [`8ac92be`](https://github.com/rishikeshsreehari/personal-blog/commit/8ac92be)  
   - *Files:*  
     1. [`scripts/pre_push.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py)  

---

### **v24.619.U.2111** (2024-11-21)

#### **Updations**
1. **Updated log.md with frontmatter**  
   - *Commit:* [`f79cade`](https://github.com/rishikeshsreehari/personal-blog/commit/f79cade)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)  

---

### **v24.618.U.2111** (2024-11-21)

#### **Updations**
1. **Added hyperlinks to files and hash in changelog**  
   - *Commit:* [`ff1ef42`](https://github.com/rishikeshsreehari/personal-blog/commit/ff1ef42)  
   - *Files:*  
     1. [`scripts/pre_push.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py)  

---

### **v24.617.M.2111** (2024-11-21)

#### **Fixes**
1. **Fixed an issue updatechangelog function in prepush**  
   - *Commit:* [`b4a1330`](https://github.com/rishikeshsreehari/personal-blog/commit/b4a1330)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)  
     2. [`data/version.json`](https://github.com/rishikeshsreehari/personal-blog/blob/main/data/version.json)  
     3. [`scripts/pre_push.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py)  

2. **Fixed an issue with pre-push**  
   - *Commit:* [`069fcee`](https://github.com/rishikeshsreehari/personal-blog/commit/069fcee)  
   - *Files:*  
     1. [`scripts/pre_push.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py)  

#### **Updates**
1. **Updated prepush logic for correct log format**  
   - *Commit:* [`7929af0`](https://github.com/rishikeshsreehari/personal-blog/commit/7929af0)  
   - *Files:*  
     1. [`content/log.md`](https://github.com/rishikeshsreehari/personal-blog/blob/main/content/log.md)  
     2. [`scripts/pre_push.py`](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py)
<!--LOG_PLACEHOLDER_END-->












