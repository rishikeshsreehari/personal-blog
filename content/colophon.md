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

###### *Last Updated on 25-10-2023*


This blog has been inspired by numberous blogs by incredibly talented individuals out there in the web universe. Over time, I've compiled a list of things that I loved in different blogs I've visited and this blog is an end result of that. As someone who started coding less than a year back, this blog is not the best, but overtime as I gain programming skills, I intend to perfect it over time.


The blog is built using the [Hugo](https://gohugo.io/) framework with the [PaperMod](https://github.com/adityatelange/hugo-PaperMod/) theme. It is currently hosted on [Netlify](https://www.netlify.com/) and the source code of the website can be found [here](https://github.com/rishikeshsreehari/personal-blog). I use [VS Code](https://code.visualstudio.com/) for all coding and pushing changes to GitHub repository. Currently the domain name is registered at [Hostinger](https://hostinger.in?REFERRALCODE=1RISHIKESH12), but I plan to switch to [PorkBun](https://porkbun.com/) soon. [Obsidian](https://obsidian.md/) is my tool of choice while writing blogposts. I do not track any personal data for analytics and use [GoatCounter](https://www.goatcounter.com/) for simple analytics. Comments are handled using [Cusdis](https://cusdis.com/), a privacy friendly alternative to Disqus. I also use geo-targeted affiliate links using [Genius](https://my.geni.us/home)at select pages which helps me earn some extra income from the blog.

All pages containing data like [library](/library),[travel](/travel),[timeline](/timeline),etc are fetched from the .yaml files and these are updated manually as and when required. Only exception to this is the [now](/now) page where a google script updates the data automatically using a google script that is triggered automatically everyday. Whenever there is change is pushed into the repository, during deployment on Netlify,python codes located in the script directories read the .yaml files from the data folder and generates svgs required in different pages

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
- Implement automatic versioning during deployment.
- Implement grammar and broken link check during deployment.
- Add a family tree in About page

## Known Issues

-  CSS issues while displaying dialogue boxes on timeline page on smaller devices.

*In case you find any bug that is not listed here, please do [contact](/contact) me.*


## Changelog

A list of major changes done to this blog in the descending order:





