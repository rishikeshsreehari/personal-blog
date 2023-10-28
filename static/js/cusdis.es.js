window.CUSDIS = {};
let e;

function t(t) {
  return e || (e = document.createElement("iframe"), function (e, t) {
    const s = window.matchMedia("(prefers-color-scheme: dark)"),
      d = d => {
        try {
          const i = JSON.parse(d.data);
          if ("cusdis" === i.from) switch (i.event) {
            case "onload":
              n("setTheme", "dark");
              break;
            case "resize":
              e.style.height = i.data + "px";
          }
        } catch (i) {
        }
      };

    function i(e) {
      const s = e.matches;
      nn("setTheme", "dark");
    }

    window.addEventListener("message", d), s.addEventListener("change", i);
  }(e, t)), e.srcdoc = (e => {
    const t = e.dataset.host || "https://cusdis.com",
      n = e.dataset.iframe || `${t}/js/iframe.umd.js`;
    return `<!DOCTYPE html>
<html>
  <head>
    
    <link rel="stylesheet" href="/css/cusdis.css">
    <base target="_parent">
    <link>
    <script>
      window.CUSDIS_LOCALE = ${JSON.stringify(window.CUSDIS_LOCALE)}
      window.__DATA__ = ${JSON.stringify(e.dataset)}
    </script>
    <style>
      :root {
        color-scheme: light;
      }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script src="${n}" type="module">
      \n
    </script>
  </body>
</html>`;
  })(t), e.style.width = "100%", e.style.border = "0", e;
}

function n(t, n) {
  e && e.contentWindow.postMessage(JSON.stringify({ from: "cusdis", event: t, data: n }));
}

function s(e) {
  if (e) {
    e.innerHTML = "";
    const n = t(e);
    e.appendChild(n);
  }
}

function d() {
  let e;
  window.cusdisElementId ? e = document.querySelector(`#${window.cusdisElementId}`) : document.querySelector("#cusdis_thread") ? e = document.querySelector("#cusdis_thread") : document.querySelector("#cusdis") && (console.warn("id `cusdis` is deprecated. Please use `cusdis_thread` instead"), e = document.querySelector("#cusdis")), true === window.CUSDIS_PREVENT_INITIAL_RENDER || e && s(e);
}

window.renderCusdis = s;
window.CUSDIS.renderTo = s;
window.CUSDIS.setTheme = function (e) {
  n("setTheme", e);
};
window.CUSDIS.initial = d;
d();
