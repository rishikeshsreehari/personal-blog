# Claude Code - Personal Blog

## Project Overview
Hugo-based personal blog at rishikeshs.com. Migrated from PaperMod to a custom theme called **Rishi**.

## Theme: Rishi
- Located at `themes/rishi/`
- Built from scratch — no CSS frameworks, plain CSS with custom properties only
- Will eventually be published as a standalone Hugo theme

### Design Principles
- Monochrome / grey and white palette
- Light/dark mode toggle (both modes required)
- Serif body text, sans-serif headings, monospace for code
- Minimal, typography-first design
- No visual clutter — let the content breathe

### Typography
- Body: Lora (serif) — Google Fonts
- Headings: Inter (sans-serif) — Google Fonts
- Code: Geist Mono — Google Fonts

### CSS Rules
- Plain CSS only — no Tailwind, no frameworks, no preprocessors
- Use CSS custom properties (variables) for all colors, fonts, spacing
- All theme-specific styles live in `themes/rishi/assets/css/main.css`
- Dark/light mode driven by `data-theme` attribute on `<html>` — not `prefers-color-scheme` alone
- Light: `--bg: #ffffff`, `--text: #1a1a1a`, `--border: #e4e4e4`
- Dark: `--bg: #111111`, `--text: #e2e2e2`, `--border: #2a2a2a`

### Theme vs Blog Separation
- Theme logic → `themes/rishi/` only
- Blog-specific content/config → root level
- Never hardcode blog name, URL, or personal info inside theme files
- All customization via `config.yml` params

---

## Hugo Config
- Config file: `config.yml`
- Theme: `rishi`
- Key params: `mainSections: ["blog"]`, `shorturl` (base URL for short links), `BookShelfDisplayCount`
- Custom features: ATOM feed, TXT/LLMs output, Markdown output format, custom `tiltag` taxonomy

---

## File Structure

### Theme layouts (`themes/rishi/layouts/`)
- `_default/baseof.html` — base template, sets `data-theme` on `<html>`
- `_default/single.html` — blog post/page template; includes `post-meta.html`, `comments.html`; microformats div uses `display:none`
- `_default/list.html` — section list (blog, TIL, etc.)
- `_default/archives.html` — grouped by year only (no month grouping); includes all content sections with filter buttons and type badges
- `_default/library.html` — books table from `site.Data.books`, sortable by date or rating
- `_default/til.html` — TIL list with filter buttons
- `_default/journal.html` — dated list layout
- `_default/fitness-log.html` — dated list layout
- `_default/timeline.html` — timeline page
- `layouts/index.html` — homepage with bio + recent posts
- `404.html` — 404 page

### Theme partials (`themes/rishi/layouts/partials/`)
- `head.html` — meta, Google Fonts, canonical, OG tags; inline JS prevents FOUC for theme toggle
- `header.html` — site title, nav, theme toggle (sun/moon SVG), hamburger for mobile; JS uses event listeners (not inline onclick) due to Hugo minifier
- `footer.html` — three-layer layout: buddy at top, single-line nav (webrings/colophon/version/privacy/feed), copyright at bottom; hardcoded `/atom.xml` (not `absURL`) to avoid localhost URL issues
- `buddy.html` — ASCII art companion cat; frame-based animation reacting to Abu Dhabi weather via wttr.in API; calculates state from blog activity (see Buddy System section below)
- `post-meta.html` — shows date · Malayalam calendar date · reading time, then short URL on next line; uses `$hasContent` flag to avoid orphaned `·` separators
- `comments.html` — custom comment system (see Comments section below)
- `social_icons.html` — NOT in theme; kept at root `layouts/partials/` for shortcode use only

### Root layouts (`layouts/`)
- `_default/` — output format templates only: `index.atom.xml`, `index.json`, `index.txt`, `index.markdown.md`, `single.markdown.md`, `list.markdown.md`
- `partials/` — only `social_icons.html` and `svg.html` (needed by shortcodes; do NOT add more here or they will override theme partials)
- `shortcodes/` — all blog-specific shortcodes live here

---

## Key Features

### Short URLs
- Data file: `data/shorturl.yaml` — maps `content_url` to `short_url`
- Config param: `params.shorturl` — base domain (e.g. `https://r1l.in`)
- Display: shown in `post-meta.html` as `↗ r1l.in/slug` on its own line below date
- Also shown in `single.html` footer as a pill button (bottom-right) with click-to-copy
- Lookup uses `.RelPermalink` to match `content_url`

### Malayalam Calendar Date
- Data file: `data/malayalam_calendar.json` — keys are `"YYYY-MM-DD"`, values are Malayalam date strings
- Shown in `post-meta.html` next to the publication date: `January 8, 2025 · ഇടവം 25, 1200`
- Only appears on pages with a non-zero date

### Post Meta (`post-meta.html`)
- Two-row layout: row 1 = date · Malayalam date · reading time; row 2 = short URL
- `$hasContent` flag prevents orphaned `·` separators on pages with no date
- Pages like About/Contact (no date, `ShowReadingTime: false`) show only the short URL row

### Comments
- Custom system backed by `data/comments.json` (keyed by URL slug)
- Form submits to Google Apps Script endpoint
- Cloudflare Turnstile CAPTCHA (`data-sitekey="0x4AAAAAAAxKySDyC3zOb0zW"`)
- Anti-spam question: "Is fire hot or cold?" → answer must be "hot"
- Honeypot field for bot detection
- Enabled globally via `params.comments: true`; disabled per-page with `disable_comments: true`
- Author replies detected by `"author-marker"` string in comment HTML

#### Comment Design (as of 2026-03-24)
- Avatar: DiceBear `lorelei-neutral` v9, 40×40px square with `border-radius: 6px`, `backgroundColor=f0f0f0` baked in (works in both light/dark mode)
  - URL pattern: `https://api.dicebear.com/9.x/lorelei-neutral/svg?seed={{ .Name | urlize }}&backgroundColor=f0f0f0&size=40`
- Layout: flex row — avatar left, comment body right (mirrors `.post-item` pattern)
- Comment header: name (bold, left) + optional badge + date (right, `justify-content: space-between`)
- Comment text: Lora (`--font-body`), `--text` color, `line-height: 1.7`
- Author replies: indented with `margin-left: calc(40px + var(--space-4))` — aligns author avatar with regular comment text start; collapses to `var(--space-4)` on mobile (`max-width: 600px`)
- Author badge: small bordered pill (same pattern as `.post-tags li a`), says "Author" for comments, "Answer" for AMA
- Separator: `border-bottom: 1px solid var(--border)` between comments (same as `.post-item`)
- **CSS spacing uses only defined variables**: `--space-1/2/3/4/6/8/12/16` — `--space-5` and `--space-10` do NOT exist, use `--space-4`/`--space-8` instead

#### AMA (`layouts/shortcodes/ama.html`)
- Data: `data/ama.json` — flat array, author replies inline with `author-marker` span
- Same comment design as `comments.html`; author badge says "Answer"
- Form at bottom (after entries); no Turnstile/anti-spam (simpler than blog comments)
- Range pattern: `range $commentsData` (forward order — oldest first)

#### Guestbook (`layouts/shortcodes/guestbook.html`)
- Data: `data/guestbook.json` — flat array, no author replies
- Same comment design; no author badge
- Entries shown newest-first via `$commentsData | collections.Reverse` (requires Hugo ≥ 0.121.0; current: 0.154.5 ✓)
- **Important**: must use `range $commentsData | collections.Reverse` + `.Name` (not index-based `range $index := seq ...` + `$entry.Name`) — the index approach can cause template context issues with `.Name` in URL attribute contexts
- Form at bottom; no Turnstile/anti-spam

#### Old extended CSS (NOT loaded by Rishi)
- `assets/css/extended/guestbook.css` and `assets/css/extended/ama.css` still exist but are PaperMod leftovers
- Rishi theme only loads `themes/rishi/assets/css/main.css` via `resources.Get "css/main.css"`
- These files can be deleted eventually; they do nothing in the current setup

### Library Page
- `content/library.md` uses `layout: "library"`
- `themes/rishi/layouts/_default/library.html` renders books from `site.Data.books`
- Sortable table: book title (linked), author, star rating, read date
- Sort controls: Newest→Oldest or Best→Worst

### Watch Pages
- List page (`/watch/`): uses `{{< watch >}}` shortcode — rows of name · stars · language · type · date
- Items with a `/watch/slug` URL in `data/watch.yaml` link to individual review pages
- Individual review pages: use `{{< watch-card name="..." >}}` shortcode
  - Shows: stars · type · year · language · runtime, then director/creator line
  - Minimal — no poster, no budget/financials, just what matters
- Watchlist page (`/watchlist/`): uses `{{< watchlist >}}` shortcode — table of title/year/language

### Archive Page (`/archive/`)
- Layout: `themes/rishi/layouts/_default/archives.html`
- Sections included: `blog`, `til`, `watch`, `journal`, `fitness-log` — add new sections to the `$sections` slice and `$typeNames` dict in the template
- Filter buttons at top (same pill style as TIL filters): All · Blog · TIL · Watch · Journal · Fitness — JS hides non-matching rows and collapses empty year blocks
- Each entry row: `date (Jan 2) · title (flex-grow) · [type badge]` — type badge right-aligned, links to section index
- CSS classes: `.archive-filters`, `.archive-filter-btn`, `.archive-filter-count`, `.archive-entry`, `.archive-entry-date`, `.archive-entry-title`, `.archive-entry-type`

### Data Tables (shared CSS)
- Class `.data-table` for library/watchlist tables
- Class `.data-sort-select` for sort dropdowns
- Star ratings use unicode `★` / `☆` characters

### Buddy System (Footer Companion)
- Located at `themes/rishi/layouts/partials/buddy.html`
- ASCII art companion cat that lives in the footer (inspired by Claude Code's /buddy feature)
- **Build-time stats**: Hugo calculates state from blog posts and activity
- **Runtime weather**: JavaScript fetches Abu Dhabi weather from `wttr.in` API (3-second timeout, 30-minute localStorage cache)
- **Frame-based animation**: Cycles through 2-3 ASCII art frames per weather state (not CSS animations)
- **Pure ASCII**: No emoji, just text art in monospace font
- **Theme-aware**: Uses `color: var(--text)` to match light/dark mode automatically

#### Activity States (calculated at build time):
- `active`: Posted within 30 days (default cat sprite)
- `resting`: 30-365 days since last post (80% opacity)
- `ghost`: 365+ days since last post (50% opacity, wandering spirit form with halo)

#### Weather Effects (runtime, frame-animated):
Each weather condition has multiple frames that cycle at different speeds:

- **Base/Clear**: Cat with tail swish (2000ms between frames)
  ```
  Frame 1: Normal cat
  Frame 2: Tail tilde moves right
  Frame 3: Ears change (/\-/\)
  ```

- **Night** (hour < 6 or > 19): Stars and dots above (2500ms)
  ```
  Stars twinkle in different positions
  ```

- **Sunny/Hot** (clear + temp > 38°C): Sun rays above, heat-exhausted eyes (2500ms)
  ```
  Frame 1: Full sun rays
  Frame 2: Sun rays alternate
  ```

- **Rain**: Rain drops falling, closed eyes (1500ms - fast)
  ```
  Rain drops shift positions
  ```

- **Cloudy**: Cloud formation above (2200ms)
  ```
  Cloud shape shifts slightly
  ```

- **Windy**: Motion lines (~~~), swaying (1200ms - fastest)
  ```
  Wind lines and cat position shift
  ```

- **Dust/Sand**: Dust particles (. : .), closed eyes (1800ms)
  ```
  Dust particles move around
  ```

- **Ghost**: Wandering spirit with halo and tilde (2000ms)
  ```
  Ghost floats with shifting tilde position
  ```

#### Animation Implementation:
- **Frame cycling via JavaScript**: `setInterval` updates sprite content by cycling through frame arrays
- **No CSS keyframe animations**: Removed to prevent conflicts with frame-based animation
- **Hover interaction**: CSS `buddy-bounce` animation on hover (0.6s)
- **State opacity**: CSS sets opacity based on `data-state` attribute (ghost: 0.5, resting: 0.8, active: 1.0)

#### Weather API Integration:
- **API**: `https://wttr.in/Abu%20Dhabi?format=j1` (same as /now page weather shortcode)
- **Timeout**: 3 seconds (AbortController)
- **Cache**: 30 minutes in localStorage (`buddy_weather_cache`)
- **Fallback**: If timeout or error, keeps default sprite (no error shown to user)
- **Console logging**: Logs weather data for debugging
- **Works for all states**: Ghost state now also reacts to weather (previously it didn't)

#### Footer Layout:
```
   /\_/\          ← Buddy at top
  ( ·   ·)
  (  ω  )
  (")_(")

Webrings · Colophon · v24.70.M.2912 · 49266c87 · Privacy · Feed  ← Single line nav

© 2026 Rishikesh Sreehari · Powered by Hugo & CloudFlare         ← Copyright at bottom
```

- All navigation links in one `.footer-nav` line
- Buddy positioned at top of footer with `margin: 0 auto var(--space-4)`
- Copyright at bottom in `.footer-copyright`
- Mobile responsive: smaller font size (0.6875rem) and sprite (0.75rem → 0.65rem)

#### Technical Details:
- **Sprite data structure**: Each weather state is an array of frame strings
- **Frame index**: Cycles through `currentFrames` array with modulo operator
- **Animation speed**: Variable `animationSpeed` (ms) changes per weather state
- **Inline script**: Runs immediately on page load (no DOMContentLoaded needed for footer)
- **No external dependencies**: Pure vanilla JavaScript, no libraries
- **Build-time separation**: Hugo template calculates state, JavaScript only handles weather + animation
- **CSS**: Minimal styling (transparent background, no border, centered, monospace font)

#### Sprite Format:
Each sprite is a multi-line string with exact spacing:
```javascript
`   /\\_/\\      ← Line 1 (ears)
  ( ·   ·)    ← Line 2 (eyes)
  (  ω  )     ← Line 3 (nose/mouth)
  (")_(")     ← Line 4 (paws)`
```

Line height: 1.05, font size: 0.75rem (desktop), 0.65rem (mobile <640px)

#### Files Modified:
- `themes/rishi/layouts/partials/buddy.html` — main buddy partial (Hugo template + inline JS)
- `themes/rishi/layouts/partials/footer.html` — restructured three-layer layout with buddy at top
- `themes/rishi/assets/css/main.css` — buddy sprite styles + footer layout + mobile responsive
- `config.yml` — removed old `footer_easter` and `footer_pet` params (no longer used)

#### Important Notes:
- **Do NOT use CSS keyframe animations** on `.buddy-sprite` — conflicts with frame-based animation
- **Frame animation uses `setTimeout`** in a loop, not `setInterval` (allows variable speed per state)
- **Weather determines `currentFrames` array**, then animation loop cycles through it
- **Ghost state is NOT excluded** from weather effects (changed from initial implementation)
- **Escape backslashes** in JavaScript template literals: `\\_` becomes `\_` in rendered sprite
- **Pre tag inherits styles** — must explicitly set `background: transparent` and `border: none` to avoid theme conflicts
- **Console logging** is intentional for debugging weather fetch — shows condition/temp/hour in browser console
- **Hugo template uses `{{- -}}` delimiters** to prevent extra whitespace in rendered HTML
- **Mobile breakpoint**: 640px (not 768px) to match rest of theme
- **Footer uses `var(--space-*)` variables** from theme — don't hardcode pixel values

#### Future Evolution Ideas (Not Implemented):
- Multiple species based on dominant blog stat (CURIOSITY→cat, CONSISTENCY→turtle, DEPTH→owl, etc.)
- Leveling system with visual upgrades (hats, accessories) at milestones
- "Reunion" animation when posting after long absence
- Rare variants (shiny, seasonal mutations)
- Thought bubbles with contextual messages
- External event reactions (international news, analytics spikes)

---

## Content Structure
- `blog/` — main blog posts (most have `hiddenInHomeList: true`)
- `til/` — Today I Learned entries with `tiltag` taxonomy
- `journal/` — journal entries
- `fitness-log/` — fitness log entries
- `watch/` — individual watch review pages
- `meet/` — meeting availability pages
- Custom pages: about, now, projects, library, archive, contact, colophon, guestbook, timeline, anti-library, watchlist, etc.

### Content Front Matter Notes
- `disable_comments: true` — suppresses comment section
- `ShowReadingTime: false` — hides reading time from post-meta
- `hideMeta: true` — hides entire post-meta block
- `hiddenInHomeList: true` — hides post from homepage recent list
- `updated_on: YYYY-MM-DD` — used by `{{< updated_on >}}` shortcode (shows date + Malayalam calendar date)

---

## Development Rules
- Do not push to GitHub unless explicitly asked
- Do not push the theme as a separate repo until asked
- Build for the blog first; generalize for publishing later
- Use relative links (`.RelPermalink`) everywhere in templates; only use `.Permalink` / `absURL` for OG meta, canonical, and feed URLs
- Never use inline `onclick` with quotes in Hugo templates — Hugo's minifier breaks them; use `id` + `addEventListener` instead
