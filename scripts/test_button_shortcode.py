"""Regression check for issue #43: a white gap appears below the button shortcode.

The shortcode puts an inline-block <a> inside a <div>. Because it sits on the
text baseline, the parent line box reserves descender space under it, which
shows up as an empty strip below the button. The anchor must be top-aligned
so the line box is sized by the button itself.

Hugo is not required: the test renders the shortcode's .Get calls with sample
values and checks the anchor in the emitted HTML. It does not measure pixels;
a browser check is still needed to confirm the visual gap is gone.
"""
import re
import sys
from pathlib import Path

SHORTCODE = Path(__file__).resolve().parent.parent / "layouts" / "shortcodes" / "button.html"

SAMPLE = {"url": "https://example.com/", "text": "Click me", "align": None}


def render(template: str) -> str:
    def get_value(match: re.Match) -> str:
        key = match.group(1)
        default = match.group(2)
        value = SAMPLE.get(key)
        if value is None:
            value = default if default is not None else ""
        return value

    # Handles {{ .Get "key" }} and {{ .Get "key" | default "fallback" }}
    return re.sub(
        r'\{\{\s*\.Get\s+"([^"]+)"\s*(?:\|\s*default\s+"([^"]*)"\s*)?\}\}',
        get_value,
        template,
    )


def main() -> int:
    html = render(SHORTCODE.read_text(encoding="utf-8"))
    anchor = re.search(r"<a\b[^>]*style=\"([^\"]*)\"", html)
    if not anchor:
        print("FAIL: no styled <a> found in rendered button shortcode")
        return 1
    style = anchor.group(1)
    if not re.search(r"vertical-align\s*:\s*top", style):
        print("FAIL: button anchor is missing vertical-align: top; "
              "baseline gap remains below the button")
        return 1
    print("OK: rendered button anchor is top-aligned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
