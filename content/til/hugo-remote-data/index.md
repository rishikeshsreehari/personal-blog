---
title: "Hugo can fetch live data during build using resources.GetRemote"
publishdate: 2025-02-16
tiltags: ["hugo", "web", "development", "SSG"]
summary: "Hugo's resources.GetRemote lets you fetch external data during site build"
url: "/til/hugo-remote-data"
---

Today I learned about Hugo's `resources.GetRemote` function while trying to add Hacker News discussion stats to [one of my blog posts](/file-over-app/). I wanted to display the upvotes and comments count from HN in a nice badge, and discovered that Hugo can fetch this data during build time.

{{< photocaption src="hn-stats-on-hugo.webp" alt="Hackernews discussion stats on Hugo Post" width="40%" >}}An example of Hackernews discussion stats on Hugo Post{{< /photocaption >}}


Here's an example of how I used it to fetch Hacker News discussion stats:

```
{{ $id := .Get "id" }}
{{ with resources.GetRemote (printf "https://hacker-news.firebaseio.com/v0/item/%s.json" $id) }}
  {{ with .Content | unmarshal }}
    Upvotes: {{ .score }}
    Comments: {{ .descendants }}
  {{ end }}
{{ end }}

```

To make this reusable, I created a shortcode that displays an interactive badge with live stats from HN:

```
{{ $id := .Get "id" }}
<div class="hn-discussion">
  <a href="https://news.ycombinator.com/item?id={{ $id }}" target="_blank" rel="noopener noreferrer">
    <div class="hn-badge">
      <div class="hn-content">
        <svg width="20" height="20" viewBox="0 0 16 16" class="hn-logo">
          <rect x="0" y="0" width="16" height="16" fill="#ff6600"/>
          <text x="3" y="12" fill="white" style="font-family: Arial; font-weight: bold; font-size: 12px;">Y</text>
        </svg>
        <div class="hn-text">
          <span class="hn-main-text">View Hacker News Discussion</span>
          <div class="hn-stats">
            {{ with resources.GetRemote (printf "https://hacker-news.firebaseio.com/v0/item/%s.json" $id) }}
              {{ with .Content | unmarshal }}
                <span class="stat-item"> {{ .score }} upvotes</span>
                <span class="stat-divider">•</span>
                <span class="stat-item"> {{ .descendants }} comments</span>
              {{ end }}
            {{ end }}
          </div>
        </div>
      </div>
    </div>
  </a>
</div>

```

Please also note that you have to enable external data fetching in your Hugo configuration by explicitly allowing requests to hacker-news.firebaseio.com. For instance, I added the following to my config.toml:

```
security:
  http:
    methods:
      - GET
    urls:
      - https://hacker-news.firebaseio.com/*

```
This ensures that Hugo permits fetching remote data from the specified URL while keeping security restrictions in place.

Hugo’s resources.GetRemote opens up a lot of possibilities for fetching external data in static sites while keeping everything efficient. Super useful! I might also convert the live fitness data on my [now](/now) page using Strava API and update the data on build rather than relying on a separate webjob!
