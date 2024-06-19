---
title: "Colophon"
#layout: "library"
url: "/colophon/"
summary: single
type: page
disable_comments: true
ShowReadingTime: false

---

>An overview of how this blog is built and roadmap ahead

###### *Last Updated on 19-06-2024*


This blog has been inspired by numberous blogs by incredibly talented individuals out there in the web universe. Over time, I've compiled a list of things that I loved in different blogs I've visited and this blog is an end result of that. As someone who started coding less than a year back, this blog is not the best, but overtime as I gain programming skills, I intend to perfect it over time.


The blog is built using the [Hugo](https://gohugo.io/) framework with the [PaperMod](https://github.com/adityatelange/hugo-PaperMod/) theme. It is currently hosted on [Cloudflare Pages](https://pages.cloudflare.com/) and the source code of the website can be found [here](https://github.com/rishikeshsreehari/personal-blog). I use [VS Code](https://code.visualstudio.com/) for all coding and pushing changes to GitHub repository. Currently the domain name is registered at [PorkBun](https://porkbun.com/). [Obsidian](https://obsidian.md/) is my tool of choice while writing blogposts. I do not track any personal data for analytics and use [GoatCounter](https://www.goatcounter.com/) for simple analytics.

The comments on blog posts, feedback on [guestbook](/guestbook) and questions on [ama](/ama) pages are all static and are served from individual .json files. The form on these pages adds the entries to a google sheet, where moderation is done and a script pushes the updated corresponding jsons to the GitHub repo. Email is totally optional and is never shared publicly. The contact form on [contact](/contact) page uses [Web3Forms](https://web3forms.com/) as a test.

All pages containing data like [library](/library),[travel](/travel),[timeline](/timeline),etc are fetched from the .yaml files and these are updated manually as and when required. Only exception to this is the [now](/now) page where a google script updates the data automatically using a google script that is triggered automatically everyday. Whenever there is change is pushed into the repository, during deployment on Netlify,python codes located in the script directories read the .yaml files from the data folder and generates svgs required for different pages.

This blog follows the [personal blog versioning manifesto](/blog-version-manifesto) and the version numbers are incremented accordingly. The latest commit hash is also mentioned in the footer to view the latest changes. For changelogs, visit [changelog](/log) page.

## Roadmap

The following list lays out the plan I have for this blog in the long run:

- Move away from frameworks and write/own every piece of the source code.
- Setup a minimal solar version of the site inspired from [Low Tech Magazine](https://solar.lowtechmagazine.com/). The goal is to self-host a solar version of the website on a [Raspberry Pi](https://geni.us/rsh-rpi4) that is portable. 
-  Integrate the live weather using a personal weather station in the [now]('/now') page. This can be integrated with the solar hosting module mentioned earlier as well.
- Create an art page for my website to host my art/photography projects.
- Dark/Light toggle for all pages
- Create a statistics page to display statistics about this blog.
- Revisit the svg creation using python code and see if there are any better alternatives
- Lay outa plan for longevity of the blog by sticking with pure html and CSS. 
- Setup a URL shortner and also use it instead of [Genius Link](https://my.geni.us/home).
- Selfhost my newsletter using a service like [listmonk](https://listmonk.app/).
- Build a guestbook section for the blog where users can post testimonials.
- Implement grammar and broken link check during deployment.
- Add a family tree in About page

## Known Issues

[1.](https://github.com/rishikeshsreehari/personal-blog/issues/20)  CSS issues while displaying dialogue boxes on timeline page on smaller devices.

*In case you find any bug that is not listed here, please do [contact](/contact) me or create an issue on [GitHub](https://github.com/rishikeshsreehari/personal-blog/issues/new).*