document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const nbPath = urlParams.get("nb") || urlParams.get("src");

  const nbTitle = document.getElementById("notebook-title");
  const nbPathDisplay = document.getElementById("notebook-path");
  const container = document.getElementById("notebook-container");
  const toggleBtn = document.getElementById("toggle-code");

  toggleBtn?.addEventListener("click", () => {
    const isHidden = container.classList.toggle("hide-code");
    toggleBtn.innerText = isHidden ? "Show Code" : "Hide Code";
  });

  if (!nbPath) {
    if (nbTitle) nbTitle.innerText = "No notebook specified.";
    return;
  }

  const fileName = nbPath.split("/").pop();
  nbPathDisplay.innerText = nbPath;
  nbPathDisplay.href = nbPath;
  nbTitle.innerText = fileName;
  document.title = `${fileName} | kavakci.dev`;

  const getNotebookLib = () => {
    if (typeof nb !== "undefined") return nb;
    if (typeof window.nb !== "undefined") return window.nb;
    if (typeof notebook !== "undefined") return notebook;
    if (typeof window.notebook !== "undefined") return window.notebook;
    return null;
  };

  const waitForNb = () => {
    return new Promise((resolve, reject) => {
      const lib = getNotebookLib();
      if (lib) return resolve(lib);

      let attempts = 0;
      const interval = setInterval(() => {
        attempts++;
        const currentLib = getNotebookLib();
        if (currentLib) {
          clearInterval(interval);
          resolve(currentLib);
        }
        if (attempts > 60) {
          clearInterval(interval);
          reject(new Error("Notebook library timeout."));
        }
      }, 50);
    });
  };

  try {
    const notebookLib = await waitForNb();
    const response = await fetch(nbPath);
    if (!response.ok) throw new Error(`Fetch failed: ${response.status}`);

    const data = await response.json();
    const notebook = notebookLib.parse(data);
    const rendered = notebook.render();

    container.innerHTML = "";
    container.appendChild(rendered);

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([container])
        .catch((err) => console.error(err))
        .finally(() => {
          container.classList.add("is-ready");
        });
    } else {
      container.classList.add("is-ready");
    }

    if (window.Prism) {
      container.querySelectorAll("pre code").forEach((block) => {
        block.classList.add("language-python");
      });
      Prism.highlightAllUnder(container);
    }
  } catch (err) {
    console.error("notebook-viewer.js:", err);
    nbTitle.innerText = "Error loading notebook.";
    container.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
  }
});
