---
title: "Colophon"
#layout: "library"
url: "/colophon/"
summary: An Overview of How This Blog is Built and Roadmap Ahead
type: page
disable_comments: true
ShowReadingTime: false

---

### An Overview of How This Blog is Built and Roadmap Ahead

##### Last updated on 17-07-2024

This blog has been inspired by numerous blogs by incredibly talented individuals out there in the web universe. Over time, I've compiled a list of things that I loved in different blogs I've visited, and this blog is an end result of that. As someone who started coding less than a year back, this blog is not the best, but over time, as I gain programming skills, I intend to perfect it.

This site is built like a maze and contains easter eggs here and there. For instance, [the useless button](/button) is an interesting page. If you find any, please do [message me](/contact).

The blog is built using the [Hugo](https://gohugo.io/) framework with a modified [PaperMod](https://github.com/adityatelange/hugo-PaperMod/) theme. It is currently hosted on [CloudFlare Pages](https://pages.cloudflare.com) and the source code of the website can be found [here](https://github.com/rishikeshsreehari/personal-blog). I use [VS Code](https://code.visualstudio.com/) for all coding and pushing changes to the GitHub repository. All my domains are registered on [PorkBun.](https://porkbun.com/) [Obsidian](https://obsidian.md/) is my tool of choice while writing blog posts. I do not track any personal data for analytics and use [GoatCounter](https://www.goatcounter.com/) for simple analytics. The comments on pages are static and are fetched from a .json file during the build process with the URL as the identifier. The comment form is handled using Google Forms and is moderated using Google Sheets, which adds the comment to the .json file upon approval. 

On [library](/library), [anti-library](/anti-library), [lifestack](/lifestack), and other pages, I use Amazon affiliate links that let me earn some revenue in case someone purchases by clicking the link without costing anything extra to the reader. I use [Genius Links](https://geni.us/t50YtV0) for localizing links and geo-targeting to the respective Amazon storefront of the user. Apart from Amazon affiliate links, I also use some other affiliate links, just like the Genius Referral link in the previous sentence. Please note that none of these cause the reader to pay anything extra and it supports my work.

All pages containing data like [library](/library), [travel](/travel), [timeline](/timeline), etc., are fetched from .yaml files and these are updated manually as and when required. The only exception to this is the [now](/now) page where a Google script updates the data automatically using a Google script that is triggered every day. Whenever there is a change pushed into the repository, during deployment on Cloudflare, Python codes located in the script directories read the .yaml files from the data folder and generate SVGs required in different pages.

## Roadmap

The following list lays out the plan I have for this blog in the long run:

- Move away from frameworks and write/own every piece of the source code.
- Set up a minimal solar version of the site inspired by [Low Tech Magazine](https://solar.lowtechmagazine.com/). The goal is to self-host a solar version of the website on a [Raspberry Pi](https://geni.us/rsh-rpi4) that is portable.
- Integrate live weather using a personal weather station on the [now](/now) page. This can be integrated with the solar hosting module mentioned earlier as well.
- Create an art page for my website to host my art/photography projects.
- Add a dark/light toggle for all pages.
- Create a statistics page to display statistics about this blog.
- Revisit the SVG creation using Python code and convert it to inline SVG.
- Lay out a plan for the longevity of the blog by sticking with pure HTML and CSS.
- Set up a URL shortener and use it instead of [Genius Link](https://my.geni.us/home).
- Self-host my newsletter using a service like [listmonk](https://listmonk.app/).
- Implement grammar and broken link checks during deployment.
- Add a family tree to the About page.
- Add a fitness page to update my fitness stats.
- Rewrite the backend of comment system using Flask.

## Known Issues

- CSS issues while displaying dialogue boxes on the timeline page on smaller devices.

*In case you find any bug that is not listed here, please do [contact](/contact) me.*

A changelog of the website can be seen on the [log](/log) page. I've written about the rationale behind this blog's versioning [here](/blog-version-manifesto). The hash at the footer of the website redirects to the GitHub commit page showing the details about the latest commit. I respect privacy of my readers and more can be read [here](/privacy-policy).
