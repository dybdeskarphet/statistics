document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const nbPath = urlParams.get("src");

  if (!nbPath) {
    document.getElementById("notebook-container").innerHTML =
      `<h2 style='color:#fabd2f'>Ready</h2><p>Use <code>?src=path/to/notebook.ipynb</code> in the URL.</p>`;
    return;
  }

  document.title = `Viewer - ${nbPath.split("/").pop()}`;
  nb.markdown = (text) => marked.parse(text);

  try {
    const response = await fetch(nbPath);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const notebook = nb.parse(await response.json());
    const container = document.getElementById("notebook-container");
    container.appendChild(notebook.render());

    // Single pass to wrap tables and tag code blocks for Prism
    container.querySelectorAll("pre, table").forEach((el) => {
      if (el.tagName === "TABLE") {
        const wrapper = document.createElement("div");
        Object.assign(wrapper.style, { overflowX: "auto", width: "100%" });
        el.replaceWith(wrapper);
        wrapper.appendChild(el);
      } else if (!el.className.includes("language-")) {
        el.classList.add("language-python");
      }
    });

    Prism.highlightAll();

    // Trigger MathJax to process the new content
    if (window.MathJax) {
      if (typeof window.MathJax.typesetPromise === "function") {
        window.MathJax.typesetPromise([container]);
      } else if (typeof window.MathJax.typeset === "function") {
        window.MathJax.typeset();
      }
    }

  } catch (err) {
    console.error(err);
    document.getElementById("notebook-container").innerHTML =
      `<h2 style='color:#fb4934'>Error loading notebook</h2><p>${err.message || err}</p>`;
  }
});