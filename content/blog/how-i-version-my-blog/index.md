---
title: 'How I Version My Blog?'
date: 2024-11-21
excerpt: The need for a versioning system in blogs and how I built a custom approach to track and log my blog's evolution.
description: The need for a versioning system in blogs and how I built a custom approach to track and log my blog's evolution.
url: /blog-version/
cover:
  image: "blog-version.webp"
  alt: "blog-version.webp"
  caption: "The need for a versioning system in blogs and how I built a custom approach to track and log my blog's evolution."
  relative: true

keywords:
  - "personal blog"
  - "small web"
  - "blog-version.webp"
  - "blog changelog"
  - "version control for blog"
  - "changelog for blogs"
weight: 1
hiddenInHomeList: true
draft: false

---

{{< dropcap >}}

When I moved this blog from WordPress to Hugo, I added a version number to the footer. While it served no practical purpose at the time, it made the blog feel more polished, more deliberate—an aesthetic touch, rather than utilitarian. I used to update it occasionally, but often used to forget about it and it was never automated.
{{< /dropcap >}}

A few months later, during a casual conversation, a friend asked, "You seem to tweak your blog a lot. How many times have you changed it?". It was meant to poke fun at my endless fiddling with the blog's design and features, but the question stayed in my mind. 

How many times had I updated my blog?
Could there be a way to track it? 
Should I?

Let's address the elephant in the room: version control for blogs isn't necessary, especially for personal blogs. It's not like software where a misplaced change can crash an entire system, or academic research where drafts evolve significantly over time.

### Version Control in Software

Version control systems truly shine when managing package releases or software distributions. You've probably encountered this yourself - a tech support representative asking about your app version or device firmware while troubleshooting.

The most widely used system is **[Semantic Versioning (SemVer)](https://semver.org/)**, which breaks down updates into:

- **Major:** Fundamental changes (e.g., version 2.0 vs. 1.0)
- **Minor:** New features or additions (e.g., version 1.2)
- **Patch:** Small fixes like typos or bugs (e.g., version 1.0.1)

Other systems include:

1. **[Calendar Versioning (CalVer)](https://calver.org/):** Tied to dates, like Ubuntu's 22.04
2. **[Sequential Versioning](https://fastercapital.com/keyword/sequential-versioning.html):** Incrementing numbers without specific meaning
3. **[Hash Versioning](https://miniscruff.github.io/hashver/):** Based on the hash of the latest commit
4. **Build Number Versioning:** Used in platforms like Stack Overflow

### Beyond Software

{{< photocaption src="blog-version.webp" alt="Draft Copy of Declaration of Independence" width="70%" >}}Draft Copy of Declaration of Independence. Credits:[US Gov](https://www.nps.gov/articles/independence-declarationdraft.htm){{< /photocaption >}}


Version control isn't limited to software though. We've all created documents with names like `FILE_Name_v1` or `Filename_revised` or the dreaded `FIleName_final_final_new`. Probably it's a natural human instinct and necessity to track changes. In fact, there are even [version control for recipes!](https://cogs-well-inc.helpscoutdocs.com/article/230-what-is-a-recipe-version)

In the academic world, Eric J Ma proposed [Semantic Versioning for Papers](https://ericmjl.github.io/blog/2015/4/3/semantic-versioning-for-papers-a-manifesto/), adapting semantic versioning for academic drafts. Will Darwin wrote about applying [version control to blogging](https://willdarwin.com/writing/vcs), using a modified semantic versioning system where:
- MAJOR changes require readers to re-read the post
- MINOR changes include adding resources, clarifying sentences, or adding footnotes
- PATCH changes cover spelling fixes, formatting, and technical cleanup

Several bloggers - [Evan Travers](https://evantravers.com/articles/2019/11/08/using-git-to-generate-a-changelog-for-your-blog/), [Søren Birkemeyer](https://annualbeta.com/blog/a-changelog-for-my-blog-posts/), [Timothy Miller](https://timothymiller.dev/posts/2020/adding-a-changelog-to-my-11ty-blog/), [Martin](https://www.tempertemper.net/blog/version-control-for-articles-and-blog-posts) & [Marcel Krčah](https://marcel.is/post-changelog/) - maintain changelogs for individual posts. While I appreciated this approach, I wanted something broader - a versioning system for the entire blog.

### Why Version in Blogs?

Blogs aren't static documents - they're living entities that evolve over time. A finance blog might need to revise outdated market advice, while a science blog must keep pace with new research findings. Technical tutorials require updates as software versions change, and even the most carefully curated resource lists eventually face broken links. Beyond these obvious changes, there’s the constant refinement of writing, the clarification of thoughts, and the improvement of explanations.

Traditional version tracking systems, built for software development, focus on code changes and breaking updates. But blog updates follow a different pattern. Content evolves gradually, old versions remain valuable for context, and changes can be subtle yet significant. Updates often happen across multiple posts, and maintaining links and resources becomes a crucial part of blog health.

I needed a system that could answer seemingly simple questions: 
- How many times was my blog updated in a year?
- What kinds of changes were made? 
- When was the last update? 
- Which parts of the blog are actively maintained? 


SemVer and CalVer weren’t designed to track blog updates or provide the transparency I wanted. They couldn't capture the nuanced evolution of blog content or provide the transparency I wanted for my readers. I needed something different - a system designed specifically for blog maintenance and evolution.

### My System

After some brainstorming and experimenting, I developed a versioning system tailored for blogs:

```
  YY.Push.Type.DDMM

  24.50.M.1904
  │  │   │   └── Type
  │  │   └────── Date
  │  └────────── Push
  └───────────── Year

```

| **Component** | **Description**                                                                 |
|---------------|---------------------------------------------------------------------------------|
| **YY**        | The year of the most recent update.                                             |
| **Push**      | A sequential counter tracking the total updates made during the year.           |
| **Type**      | Categorizes the nature of the update:                                           |
|               | **N**: New post.                                                               |
|               | **U**: Content update (e.g., clarifications or expansions).                    |
|               | **F**: Fix (e.g., typos or formatting corrections).                            |
|               | **X**: Feature update (e.g., design or functionality changes).                 |
|               | **M**: Mixed updates involving multiple types of changes.                      |
| **DDMM**      | The date (day and month) of the latest update.                                  |


For example the version number **v24.628.M.2111** tells me that:

- The blog was last updated in **2024**.
- There have been **628 updates** so far this year.
- The most recent update involved **multiple changes** on **November 21st**.

Despite my rudimentary coding skills and occasional ChatGPT hallucinations, I wrote a [small script](https://github.com/rishikeshsreehari/personal-blog/blob/main/scripts/pre_push.py)
(pre-push) that automatically updates the footer version number and generates a [changelog](/log) whenever I make changes to my blog. It does this:

1. **Tracks Changes:** Categorizes commits based on tags
2. **Updates the Footer:** Automatically updates version numbers
3. **Generates Changelogs:** Creates detailed logs


An example change log can be viewed below:

```
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

```

### Looking forward

This system works for me, but it's still experimental. Yes, it's complex. Yes, it might seem excessive for a personal blog. But it serves its purpose, enabling systematic tracking of how my blog evolves over time.

Nothing in this blog is set in stone. Things change and evolve, and now I can track that evolution systematically. Perhaps this will enable interesting insights at year's end, or maybe a timeline showing how the blog has grown.

It’s too early to call this approach a manifesto. Before formalizing anything, I need to gather more feedback, refine the system, and see how it holds up over time.

Would versioning work for your blog? Or do you prefer to keep updates invisible? Let me know—I’d love to hear your thoughts.



{{< subscribe_block >}}


