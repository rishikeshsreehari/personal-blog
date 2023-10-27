window.CUSDIS = {};
let iframeElement;

function createIframe(t) {
  return iframeElement || (iframeElement = document.createElement("iframe"), function(iframeElement, t) {
    const s = window.matchMedia("(prefers-color-scheme: dark)");
    const d = (event) => {
      try {
        const data = JSON.parse(event.data);
        if ("cusdis" === data.from) {
          switch (data.event) {
            case "onload":
              "auto" === t.dataset.theme && postMessage("setTheme", s.matches ? "dark" : "light");
              break;
            case "resize":
              iframeElement.style.height = data.data + "px";
          }
        }
      } catch (error) {}
    };

    function setTheme(mediaQuery) {
      const matches = mediaQuery.matches;
      "auto" === t.dataset.theme && postMessage("setTheme", matches ? "dark" : "light");
    }

    window.addEventListener("message", d);
    s.addEventListener("change", setTheme);
  })(iframeElement, t);

  iframeElement.srcdoc = ((t) => {
    const host = t.dataset.host || "https://cusdis.com";
    const iframeSrc = t.dataset.iframe || `${host}/js/iframe.umd.js`;
    return `<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="${host}/js/style.css">
    <base target="_parent" />
    <link>
    <script>
      window.CUSDIS_LOCALE = ${JSON.stringify(window.CUSDIS_LOCALE)}
      window.__DATA__ = ${JSON.stringify(t.dataset)}
    <\/script>
    <style>
      :root {
        color-scheme: light;
      }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script src="${iframeSrc}" type="module">
      \n
    <\/script>
  </body>
</html>`;
  })(t);

  iframeElement.style.width = "100%";
  iframeElement.style.border = "0";
  return iframeElement;
}

function postMessage(event, data) {
  iframeElement && iframeElement.contentWindow.postMessage(JSON.stringify({
    from: "cusdis",
    event: event,
    data: data
  }));
}

function renderIframe(element) {
  if (element) {
    element.innerHTML = "";
    const iframe = createIframe(element);
    element.appendChild(iframe);
  }
}

function initialize() {
  let targetElement;
  window.cusdisElementId ? targetElement = document.querySelector(`#${window.cusdisElementId}`) : document.querySelector("#cusdis_thread") ? targetElement = document.querySelector("#cusdis_thread") : document.querySelector("#cusdis") && (console.warn("id `cusdis` is deprecated. Please use `cusdis_thread` instead"), targetElement = document.querySelector("#cusdis"));
  !0 === window.CUSDIS_PREVENT_INITIAL_RENDER || targetElement && renderIframe(targetElement);
}

window.renderCusdis = renderIframe;
window.CUSDIS.renderTo = renderIframe;
window.CUSDIS.setTheme = function (theme) {
  postMessage("setTheme", theme);
};
window.CUSDIS.initial = initialize;
initialize();
