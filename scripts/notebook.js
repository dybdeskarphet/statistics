document.addEventListener("DOMContentLoaded", function () {
  nb.markdown = function (text) {
    return marked.parse(text);
  };

  nb.ansi = function (text, options) {
    return text;
  };

  nb.highlighter = function (text, pre, code, lang) {
    var language = Prism.languages[lang] || Prism.languages.python;
    pre.className = "language-" + (lang || "python");
    return Prism.highlight(text, language);
  };

  const urlParams = new URLSearchParams(window.location.search);
  const nbPath = urlParams.get("src");
  document.title = `Notebook Viewer - ${nbPath.split("/").pop()}`;
  if (nbPath) {
    (async () => {
      try {
        const response = await fetch(nbPath);

        if (!response.ok) {
          throw new Error("HTTP " + response.status);
        }

        const data = await response.json();
        var notebook = nb.parse(data);

        document
          .getElementById("notebook-container")
          .appendChild(notebook.render());

        Prism.highlightAll();

        // Table fixer
        const table = document.querySelector("table");
        if (table) {
          const wrapper = document.createElement("div");
          wrapper.style.overflowX = "auto";
          wrapper.style.width = "100%";
          table.parentNode.insertBefore(wrapper, table);
          wrapper.appendChild(table);
        }
      } catch (err) {
        console.error(err);
        document.getElementById("notebook-container").innerHTML =
          `<h2 style='color:#fb4934'>Error loading notebook</h2>
         <p>${err}</p>
         <p>Make sure you are running <code>python3 -m http.server</code> and the file path is correct.</p>`;
      }
    })();
  } else {
    document.getElementById("notebook-container").innerHTML =
      `<h2 style='color:#fabd2f'>Ready</h2>
     <p>Use <code>?src=path/to/notebook.ipynb</code> in the URL.</p>`;
  }
});
