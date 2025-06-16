---
title: 'File Over App: A Philosophy for Digital Longevity'
date: 2024-11-13
excerpt: My take on the 'file over app' philosophy and why it’s essential for keeping my data resilient and built to last.
description: My take on the 'file over app' philosophy and why it’s essential for keeping my data resilient and built to last.
url: /file-over-app/
cover:
  image: "fountain.webp"
  alt: "file over app"
  caption: "My take on the 'file over app' philosophy and why it’s essential for keeping my data resilient and built to last."
  relative: true

keywords:
  - "personal blog"
  - "small web"
  - "file over app"
  - "plain text files"
  - "digital longevity"
weight: 1
hiddenInHomeList: true
draft: false
enableWebmentions: false


---

{{< dropcap >}}


I recently [spoke](/meet/1) to a reader on the blog during [unoffice hours](/unoffice-hours), and we got into a discussion about Notion. While I agree that Notion's UI is sleek and feature-rich, I had my concerns. I used Notion for a while in early 2021 but eventually switched to Obsidian. This isn't a promotion for Obsidian—nor am I affiliated—but I made the switch because I wanted a tool that's local-first, fast, and lets me export files that can outlast any app.

{{< /dropcap >}}


Obsidian, like Notion, uses Markdown for note-taking, but Obsidian stores everything as plain text files on my device. I believe in the long-term value of open, accessible file formats like Markdown, HTML, and plain text. Just as plain text has outlived many technologies, these formats will likely outlive me. Being tied to an app creates potential issues in the long run.

### The Philosophy of File Over App

When I think about note-taking, I believe we should take a long-term view. An undergrad today might want to refer back to their notes in their 30s or 40s. In this context, preferring files over apps makes sense. This idea isn't new; it resonates with something [Steph Ango](https://stephango.com/file-over-app), the CEO of Obsidian, said:

>"File over app is a philosophy: if you want to create digital artifacts that last, they must be files you can control, in formats that are easy to retrieve and read. Use tools that give you this freedom."

I relate deeply to this perspective. In fact, I have some bitter memories about data loss. When I was [interrailing](https://en.wikipedia.org/wiki/Interrail)(or EU railing) in Europe, I used Google Trips to plan my itinerary, make notes, and track expenses. When the app was [discontinued](https://en.wikipedia.org/wiki/Google_Travel), I lost all that data because I hadn't backed it up. Another time, in 2022, I tracked my food intake with HealthifyMe for a few months, only to discover that it offered no way to export or analyze the data. Though I managed to retrieve a raw data blob, it was too cumbersome to work with. If I'd kept that data in a simple, plain-text file, I could have easily processed it with a script.

### Personal Experience and Practical Applications
Today, almost all of my notes are in Obsidian. I'm aware that Obsidian might not last forever, but the files will. Markdown files can be read with any text editor, ensuring accessibility across future devices. Plain text has been and will continue to be universally readable. While this article is not about text files, text files are the god-mode of longevity when it comes to files. Derek Sivers talks a bit about this in his blog post, ['Write Plain Text Files'](https://sive.rs/plaintext). Since 1990, he's written, blogged, journaled, and even coded in plain text. Donald L. Brown Jr. also goes into detail about the longevity of plain text files in his short book titled ['A Plain Defense for Plain Text](https://plaintext.bearblog.dev/a-plain-defense-for-plain-text/)'.

>"Every device, including ones long gone, and ones not invented yet, can read and edit plain text. Whether in VR or a chip implanted in your earlobe, plain text will be there. Will Microsoft Word? Evernote? Notion? Maybe. But plain text? Always."  
-- Derek Sivers


In my setup, I sync everything to Google Drive (and iCloud) and back it up locally. My Obsidian vault contains everything from notes to interesting links I collect for my newsletter. For example, I keep a service log for my bike, saved as a note on Obsdidian:


```
#### Service Log - Triban RC100

3. Date of Service 03-12-2022
   Service done by Bike Shop Green Park, Delhi
   Odo: 5637 km
   Details: Stripdown, hub, dust cap replace, packed
   Cost: INR 2000
   Notes: INR 300 for home delivery
   
2. Date of Service: 28-09-2022
   Service done by UBC
   Odo: 4632 km
   Details: Hub Service, FD(Claris), BB and Crank installation
   Cost: INR 8500
   Notes: Bilal messed up my hub with the wrong bearings.
   
1. Date of Service: 20-07-2022 
   Serviced by Bilal at Home, Kerala
   Odo: 3768km
   Details: Chain/Cassette Change
   Cost: 2200 INR
   Notes: Last cassette/chain casted - 1150.215km

```
{{< photocaption>}}A simple service log of my bike!{{< /photocaption >}}


If Obsidian shuts down, it won't affect my ability to access these files. My directory structure remains intact, readable by any plain text editor. I take this philosophy into other projects as well. For instance, I haven’t found a calorie tracker that allows easy export and syncing, so I'm building my own system using a double-entry accounting format for calories.




```

C:\USERS\RISHI\ICLOUDDRIVE\ICLOUD~MD~OBSIDIAN\SECOND BRAIN
├───Archives
├───Notes
│   ├───Books
│   ├───Career
│   │   ├───Job
│   │   ├───Learning Notes
│   │   └───xxx
│   │       └───Daily Notes
│   ├───Crypto
│   ├───Cycling
│   ├───Daily
│   ├───Fitness
│   ├───Learning
│   │   ├───Artificial Intelligence
│   │   │   └───Deep Learning - Fast AI
│   │   │       └───Notes
│   │   ├───Buddhism
│   │   ├───Career
│   │   │   ├───Energy System Modelling - Tom Brown
│   │   │   └───Energy Systems TU Berlin - 2021
│   │   ├───Computer Science
│   │   ├───Drawing
│   │   ├───Energy Economics
│   │   ├───Generative Art
│   │   ├───Mathematics
│   │   ├───Python
│   │   ├───Theoretical Physics
│   │   ├───Visualisation
│   │   └───Web development
│   ├───Misc
│   ├───Personal
│   └───Running
├───Projects
│   ├───Art
└───Unprocessed

```
{{< photocaption>}}A truncated version of my Obsidian Directory{{< /photocaption >}}


### A Balanced Approach to File over App
I'm not 100% 'File over App'. I still rely on Apple's ecosystem for several things, but I try to back up and store data in accessible formats to reduce dependency. For example, my steps and calorie data sync to a .csv file from Apple Health, and my Strava workout data is stored in .csv files. My gym workout details, tracked in Strong, are scraped into text files. In all digital decisions, I aim to be 'File over App' as much as possible.

That said, some projects do rely on specific ecosystems. For example, my pension fund tracker, [npsnav.in](https://npsnav.in), is built with Cloudflare Pages and Workers. If Cloudflare were to shut down, I could migrate the code, but it would require effort. Similary my blog relies on Hugo Framework, which is a dependency I want to eliminate. My goal is to create a blog composed of HTML files with basic CSS and JS, reducing external dependencies.

### Tools Aligned with File-over-App Philosophy

{{< photocaption src="fountain.webp" alt="Codex Atlanticus" width="70%" >}}How screenwriting looks in [Fountain](https://fountain.io/){{< /photocaption >}}


These are a few tools and projects that align with this philosophy. Here's a list of apps that I've found useful, and if you have suggestions, let me know so I can add them:


- [Obsidian](https://fountain.io/) - A markdown-based personal knowledge management tool
- [Paisa.fyi](https://paisa.fyi) - An open-source personal finance manager using double-entry accounting
- [FlatHabits](https://flathabits.com/) - A habit tracker that uses org-text, a plain text format for data storage
- [Fountain](https://fountain.io/) - A plain text markup language for screenwriting
- [Plain Org](https://plainorg.com/) - A to-do list app using org mode text
- [Notable](https://notable.app/) - A note-taking app using markdown
- [ToDo.txt ](http://todotxt.org/)- A command-line to-do list tool
- [Bruno](https://www.usebruno.com/manifesto) - Ceate plain-text API files wih version control using Git. 
- [SilverBullet](https://silverbullet.md/) - An open-source PKM system with plain-text as back-end.
- [Logseq](https://logseq.com/) - An open-source knowledge based on markdown files.
- [Emacs with Org Mode](https://orgmode.org/) – A plain-text tool for managing notes, tasks, and projects, focused on flexibility and long-term accessibility.
- [OneFolder](https://onefolder.app/) - Open-source photo organizer storing tags, faces, and locations in metadata, ensuring no lock-in.
- [Lyrcs](https://lyrcs.app/) - A lyrics writing app that stores its content in plain text files. 
- [Markor](https://github.com/gsantner/markor) - A text editor for notes and to-do app for Android using simple markup formats. 
- [Ledger](https://ledger-cli.org/) and [hledger](https://hledger.org/) for plain-text accounting!
- [Maro](https://marp.app/) - Presentations using markdown. A full list of apps/services that allow creating slide decks can be viewed [here](https://gist.github.com/johnloy/27dd124ad40e210e91c70dd1c24ac8c8).

If you are working on a similar tool, happy to have a look and add them to the above list!

In the end, 'File over App' isn't just a philosophy - it's a guideline for making digital choices that prioritize the longevity of data. With each decision, I'm creating a lasting digital archive, one file at a time.

{{< hn-discussion id="42136054" >}}

---

#### Update #6 - 02-06-2025, 15:16 GST
- _Thanks again to Miika for suggesting presentation software that uses markdown!_


#### Update #5 - 26-12-2024, 12:16 GST
- _Thanks to Miika for suggesting Ledger and hledger!_



#### Update #5 - 06-12-2024, 17:50 IST
- _Thanks to [Srikanth](https://srikanthperinkulam.com/) for suggesting Marko!_


#### Update #4 - 28-11-2024, 10:50 IST
- _Thanks to [WetSponge](https://www.indiehackers.com/WetSponge?id=cmT3EJOZ4GVctbHWtiZh6N8ZmYF2) for recommending Lyrcs.app!_

#### Update #3 - 21-11-2024, 12:45 GST
- _Thanks to Antoine for recommending OneFolder and the great work behind!_

#### Update #2 - 19-11-2024, 19:03 GST
- _Thanks to Burno for recommending Emacs with Org Mode_

#### Update #1 - 18-11-2024, 13:30 GST

- _Somehow, this featured on the front page of Hacker News. 🎉_
- _Thanks to [@reddalo](https://news.ycombinator.com/user?id=reddalo) for suggesting Bruno._
- _Thanks to NotABug for recommending SilverBullet and Logseq._




{{< subscribe_block >}}


