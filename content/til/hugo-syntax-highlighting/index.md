---
title: "Configuring Hugo Syntax Highlighting with Language Hints"
date: 2025-07-28
tiltags: ["hugo", "markdown", "programming", "webdev"]
summary: "How to properly configure Hugo's Chroma syntax highlighter to work with language hints in markdown code blocks."
url: "/til/hugo-syntax-highlighting"
---

Today I learned that markdown code blocks in Hugo have language hints that tell the Chroma syntax highlighter which programming language to use for proper coloring.

Syntax is like this:

````markdown
```LANG [OPTIONS]
CODE
```
````

Usage example:

````markdown
```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}
````
Hugo's Chroma highlighter applies JavaScript-specific syntax coloring instead of rendering plain text. But you need the right config settings in your `config.yml`:

```yaml
markup:
  highlight:
    codeFences: true      # Enable fenced code blocks
    guessSyntax: false    # Keep false - auto-detection is very limited
    style: dracula        # Color scheme
    noClasses: true       # Use inline CSS styles
    lineNos: false        # No line numbers for cleaner look
```

Here are some examples of different use cases:

**Python code:**
```python
def hello_world():
    print("Hello, World!")
```

**CSS styling:**
```css
.highlight {
    background-color: yellow;
    font-weight: bold;
}
```

**Bash commands:**
```bash
sudo apt update
cd /home/user
```

**Plain text (no highlighting):**
```text
This is just plain text
No syntax highlighting needed
```

**JSON data:**
```json
{
    "name": "John",
    "age": 30,
    "active": true
}
```

As someone who uses markdown codeblocks for different languages and also for text, this is quite useful.

More info(supported languages and identifiers) on syntax highlighting can be read on the [official docs](https://gohugo.io/content-management/syntax-highlighting/).

---

