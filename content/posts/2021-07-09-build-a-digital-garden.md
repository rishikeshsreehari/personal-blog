---
title: How I built my Digital Garden using Hugo
author: Rishikesh
date: 2021-07-09T21:44:03+00:00
excerpt: Digital Garden is a collection of notes, resources, ideas, quotes or summaries shared in public. This article explains how I built a digital garden using Hugo.
url: /build-a-digital-garden/
featured_image: /wp-content/uploads/2021/07/kkk-1200x800.png
ssb_old_counts:
  - 'a:5:{s:7:"twitter";i:0;s:9:"pinterest";i:0;s:7:"fbshare";i:0;s:6:"reddit";i:0;s:6:"tumblr";N;}'
ssb_cache_timestamp:
  - 463328
categories:
  - DIY
  - Productivity
  - Project

---
<p class="has-drop-cap">
  <a href="https://notes.rishikeshs.com" title="https://notes.rishikeshs.com">Digital Garden</a> is a collection of notes, resources, ideas, quotes or summaries shared in public. Unlike a blog post or a published essay, there is no publication date in a digital garden. Everything published in a <a href="https://maggieappleton.com/garden-history" target="_blank" rel="noreferrer noopener" title="https://maggieappleton.com/garden-history">Digital Garden is evergreen</a> and grows over time. Nothing is finished work and the garden evolves over time. Digital Gardens are usually lightweight and focuses on text & content over fancy styling features of modern websites.
</p>

<a href="https://maggieappleton.com/garden-history" target="_blank" rel="noreferrer noopener" title="https://maggieappleton.com/garden-history">Read more about the History and Ethos of Digital gardens.</a>

<div class="is-layout-flex wp-block-buttons">
  <div class="wp-block-button">
    <a class="wp-block-button__link" href="https://notes.rishikeshs.com" target="_blank" rel="noreferrer noopener">Check my DIGITAL GARDEN</a>
  </div>
</div>

## Features 

  * Publication Dates are not important to Digital Gardeners. Posts are connected via references or common themes.
  * There are no featured posts or chronological list of items. Readers can enter through any note, follow any trail and exit as they wish.
  * Digital Gardens are constantly evolving over time and are never complete. There is no pressure to publish a perfect post in digital gardens as notes grow over time just like plants in a garden.
  * Every Garden is unique as the patterns and relationships between notes vary from person to person.
  * Gardens are a way of learning in public thereby opening more possibilities for collaboration.

## How I built my Digital Garden using Hugo?

Since today&#8217;s internet is full of blogs and websites filled with scripts and trackers, I decided to keep my Digital Garden simple. I was already pissed with the performance of WordPress on this blog and wanted something lightweight. I explored various static website frameworks and finally decided to build one using [Hugo][1]. Hugo was the obvious choice as I already use <a href="https://obsidian.md/" target="_blank" rel="noreferrer noopener" title="https://obsidian.md/">Obsidian</a> which uses <a href="https://www.markdownguide.org/getting-started/#:~:text=What%20is%20Markdown%3F,than%20using%20a%20WYSIWYG%20editor." target="_blank" rel="noreferrer noopener" title="https://www.markdownguide.org/getting-started/#:~:text=What%20is%20Markdown%3F,than%20using%20a%20WYSIWYG%20editor.">markdown</a> for research and was excited to learn a new framework from scratch.

This is not an extensive tutorial that gives you [step by step instructions][2] on how to set up a website using Hugo. If you&#8217;re familiar with some web development or are curious enough, Hugo is pretty easy to learn. If you&#8217;re looking to build something quick with minimal code, look at some No-Code options compiled on <a href="https://nesslabs.com/digital-garden-set-up#:~:text=A%20digital%20garden%20is%20an,to%20be%20cultivated%20in%20public." target="_blank" rel="noreferrer noopener">Ness Labs</a>.

#### Setting up Hugo

<blockquote class="wp-block-quote">
  <p>
    Install Hugo on your computer. <a href="https://gohugo.io/getting-started/installing/" target="_blank" rel="noreferrer noopener" title="https://gohugo.io/getting-started/installing/">[Read more]</a>
  </p>
</blockquote>

<blockquote class="wp-block-quote">
  <p>
    Create a folder where you want to build your websites.
  </p>
</blockquote>

<blockquote class="wp-block-quote">
  <p>
    Open Terminal or Command Prompt and navigate to that folder(For eg. &#8220;C:\Users\rishi\Desktop\digital-garden&#8221;) <a href="https://riptutorial.com/cmd/example/8646/navigating-in-cmd4" target="_blank" rel="noreferrer noopener" title="https://riptutorial.com/cmd/example/8646/navigating-in-cmd4">[Read more to learn navigation in terminal]</a>
  </p>
</blockquote>

<blockquote class="wp-block-quote">
  <p>
    Type the following code: &#8220;hugo new site example&#8221;. This command will create a new site called example. <a href="https://gohugo.io/getting-started/quick-start/" target="_blank" rel="noreferrer noopener" title="https://gohugo.io/getting-started/quick-start/">[Read more]</a>
  </p>
</blockquote>

<blockquote class="wp-block-quote">
  <p>
    Now you need to add a theme. For <a href="https://notes.rishikeshs.com/" target="_blank" rel="noreferrer noopener" title="https://notes.rishikeshs.com/">my digital garden</a>, I use a theme called &#8216;<a href="https://janraasch.github.io/hugo-bearblog/" target="_blank" rel="noreferrer noopener" title="https://janraasch.github.io/hugo-bearblog/">Hugo Bear Blog</a>&#8216;. You can download other themes from the <a href="https://themes.gohugo.io/" target="_blank" rel="noreferrer noopener" title="https://themes.gohugo.io/">Hugo theme library</a>. Download the theme package from the corresponding website, in this case from Github.
  </p>
</blockquote>

<blockquote class="wp-block-quote">
  <p>
    Unzip the file and copy the folder inside the &#8220;themes/&#8221; directory in your website folder.
  </p>
</blockquote>

<blockquote class="wp-block-quote">
  <p>
    Navigate to &#8220;themes/hugo-bearblog/exampleSite/&#8221; and copy the config.toml file. Paste the config.toml file inside the main directory.
  </p>
</blockquote>

<blockquote class="wp-block-quote">
  <p>
    Open the config.toml file using a text editor and make necessary changes. Make sure that the theme name in config.toml matches with the theme folder inside the &#8220;themes/&#8221; directory.
  </p>
</blockquote><figure class="wp-block-image size-large is-style-default">

<img decoding="async" loading="lazy" width="580" height="285" src="https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/Capture.png?resize=580%2C285&#038;ssl=1" alt="digital-garden-hugo" class="wp-image-408" srcset="https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/Capture.png?resize=1024%2C504&ssl=1 1024w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/Capture.png?resize=300%2C148&ssl=1 300w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/Capture.png?resize=768%2C378&ssl=1 768w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/Capture.png?w=1034&ssl=1 1034w" sizes="(max-width: 580px) 100vw, 580px" data-recalc-dims="1" /> <figcaption>Setting up the server</figcaption></figure> 

<blockquote class="wp-block-quote">
  <p>
    In the terminal type &#8220;hugo server&#8221;. The site will be compiled and you will get a localhost address to access the site live from the browser.
  </p>
</blockquote><figure class="wp-block-image size-large is-style-default">

<img decoding="async" loading="lazy" width="580" height="383" src="https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/aa.png?resize=580%2C383&#038;ssl=1" alt="" class="wp-image-410" srcset="https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/aa.png?resize=1024%2C677&ssl=1 1024w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/aa.png?resize=300%2C198&ssl=1 300w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/aa.png?resize=768%2C508&ssl=1 768w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/aa.png?resize=1200%2C793&ssl=1 1200w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/aa.png?w=1374&ssl=1 1374w" sizes="(max-width: 580px) 100vw, 580px" data-recalc-dims="1" /> <figcaption>Using Atom to edit config.toml file.</figcaption></figure> 

<blockquote class="wp-block-quote">
  <p>
    Using an editor like <a href="https://atom.io/" target="_blank" rel="noreferrer noopener">Atom</a>, make necessary changes in the theme to customise as per your wish. To convert the theme into my liking for the digital garden, I removed codes that were used for displaying dates and sorting lists. If you want to duplicate my website, you can access the theme <a href="https://drive.google.com/file/d/1_qsSy7T72CAv_S20mlCMmyPiVoJbCLH9/view?usp=sharing" target="_blank" rel="noreferrer noopener">from here</a>.
  </p>
</blockquote>

<blockquote class="wp-block-quote">
  <p>
    To create a new post, type &#8221; hugo new cycling&#8221;, which will create a new post called cycling.
  </p>
</blockquote><figure class="wp-block-image size-large is-style-default">

<img decoding="async" loading="lazy" width="580" height="345" src="https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/faf.png?resize=580%2C345&#038;ssl=1" alt="Setting up digital garden" class="wp-image-411" srcset="https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/faf.png?w=697&ssl=1 697w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/faf.png?resize=300%2C178&ssl=1 300w" sizes="(max-width: 580px) 100vw, 580px" data-recalc-dims="1" /> <figcaption>Compiling the website.</figcaption></figure> 

<blockquote class="wp-block-quote">
  <p>
    Once you have done the necessary changes locally, press Ctrl+C to stop the server. Type &#8221; hugo&#8221; to compile the website. This will create the static Html for your website to be hosted inside &#8220;public/&#8221; directory.
  </p>
</blockquote><figure class="wp-block-image size-large is-style-default">

<img decoding="async" loading="lazy" width="580" height="265" src="https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/fil.png?resize=580%2C265&#038;ssl=1" alt="" class="wp-image-412" srcset="https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/fil.png?resize=1024%2C468&ssl=1 1024w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/fil.png?resize=300%2C137&ssl=1 300w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/fil.png?resize=768%2C351&ssl=1 768w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/fil.png?resize=1536%2C701&ssl=1 1536w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/fil.png?resize=1200%2C548&ssl=1 1200w, https://i0.wp.com/rishikeshs.com/wp-content/uploads/2021/07/fil.png?w=1708&ssl=1 1708w" sizes="(max-width: 580px) 100vw, 580px" data-recalc-dims="1" /> <figcaption>Using Filezilla to manage files on the server</figcaption></figure> 

<blockquote class="wp-block-quote">
  <p>
    Using an FTP client called <a href="https://filezilla-project.org/" target="_blank" rel="noreferrer noopener" title="https://filezilla-project.org/">Filezilla</a>, I upload the contents of the public directory to the corresponding domain on my server. I have set it to automatically synchronise so that every time I make any change, Filezilla automatically updates my website on the cloud.
  </p>
</blockquote>

If you don&#8217;t have hosting of your own, you can use <a href="https://pages.github.com/" target="_blank" rel="noreferrer noopener" title="https://pages.github.com/">Gitpages</a> or <a href="https://www.netlify.com/" target="_blank" rel="noreferrer noopener" title="https://www.netlify.com/">Netlify</a>. For me building, this <a href="https://notes.rishikeshs.com" target="_blank" rel="noreferrer noopener" title="https://notes.rishikeshs.com">Digital Garden</a> was a lot of fun. I would definitely recommend you to build one from scratch so that you can customise it as per your liking.  
  
If you&#8217;re trying to build a Digital Garden and need assistance, <a href="https://rishikeshs.com/contact/" target="_blank" rel="noreferrer noopener" title="Contact">contact me</a> so that I can assist you in setting up one.

<pre class="wp-block-preformatted"><em><strong>Enjoyed this article? If so, check out my <a href="https://rishikesh.substack.com/" target="_blank" rel="noreferrer noopener">10+1 Things</a> Newsletter that I send out every Saturday. It contains 11 interesting Things I thought were worth sharing including books,articles, projects, and other things I'm curious about. <a href="https://rishikesh.substack.com/archive">Click here </a>if you would like to check out the previous issues and may be subscribe! &nbsp;</strong></em></pre>

 [1]: https://gohugo.io/
 [2]: https://gohugo.io/getting-started/