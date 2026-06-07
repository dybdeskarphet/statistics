async function loadContent() {
  const container = document.getElementById("content-container");
  if (!container) return;

  try {
    const response = await fetch("notes.toml");
    const text = await response.text();

    const sectionBlocks = text
      .split(/\[\[sections\]\]/)
      .map((s) => s.trim())
      .filter((s) => s);

    sectionBlocks.forEach((block) => {
      const section = { title: "", items: [] };

      const titleMatch = block.match(/^title\s*=\s*("[^"]*")/m);
      if (titleMatch) {
        try {
          section.title = JSON.parse(titleMatch[1]);
        } catch (e) {
          section.title = titleMatch[1].replace(/^"|"$/g, "");
        }
      }

      const itemsContent = extractArrayFromSegment(block, 0);
      if (itemsContent) {
        section.items = parseObjectsInArray(itemsContent);
      } else {
        const notesContent = extractArrayFromSegment(
          block.replace("title =", "xxx ="),
          0,
        );
        if (notesContent) section.items = parseObjectsInArray(notesContent);
      }

      renderSection(section, container);
    });

    const finalize = () => {
      const loadingMsg = container.querySelector("p");
      if (loadingMsg && loadingMsg.innerText.includes("Loading"))
        loadingMsg.remove();
      container.classList.add("is-ready");
    };

    if (window.MathJax && window.MathJax.startup) {
      window.MathJax.startup.promise
        .then(() => window.MathJax.typesetPromise([container]))
        .catch((err) => console.error("MathJax error:", err))
        .finally(finalize);
    } else {
      finalize();
    }
  } catch (err) {
    console.error("Content Load Error:", err);
    container.innerHTML = `<div class="alert alert-error">Error loading content: ${err.message}</div>`;
  }
}

function extractArrayFromSegment(text, startIdx) {
  const match = text.substring(startIdx).match(/\w+\s*=\s*\[/);
  if (!match) return null;

  const absoluteStart = startIdx + match.index + match[0].length - 1;
  let bracketCount = 0;
  let openerFound = false;

  for (let i = absoluteStart; i < text.length; i++) {
    if (text[i] === "[") {
      bracketCount++;
      openerFound = true;
    } else if (text[i] === "]") {
      bracketCount--;
      if (bracketCount === 0 && openerFound) {
        return text.substring(absoluteStart + 1, i);
      }
    }
  }
  return null;
}

function extractObjectContent(text, startIdx) {
  let bracketCount = 0;
  let openerFound = false;

  for (let i = startIdx; i < text.length; i++) {
    if (text[i] === "{") {
      bracketCount++;
      openerFound = true;
    } else if (text[i] === "}") {
      bracketCount--;
      if (bracketCount === 0 && openerFound) {
        return text.substring(startIdx + 1, i);
      }
    }
  }
  return null;
}

function parseObjectsInArray(text) {
  const objects = [];
  let i = 0;
  while (i < text.length) {
    if (text[i] === "{") {
      const objText = extractObjectContent(text, i);
      if (objText !== null) {
        objects.push(parseObjectProperties(objText));
        let count = 0;
        for (let j = i; j < text.length; j++) {
          if (text[j] === "{") count++;
          if (text[j] === "}") {
            count--;
            if (count === 0) {
              i = j;
              break;
            }
          }
        }
      }
    }
    i++;
  }
  return objects;
}

function parseObjectProperties(text) {
  const obj = {};
  let cleanedText = text;

  const arrayMatch = text.match(/(\w+)\s*=\s*\[/);
  if (arrayMatch) {
    const key = arrayMatch[1];
    let absoluteStart = arrayMatch.index + arrayMatch[0].length - 1;
    let bracketCount = 0;
    let openerFound = false;
    let endIdx = -1;
    for (let i = absoluteStart; i < text.length; i++) {
      if (text[i] === "[") {
        bracketCount++;
        openerFound = true;
      } else if (text[i] === "]") {
        bracketCount--;
        if (bracketCount === 0 && openerFound) {
          endIdx = i;
          break;
        }
      }
    }

    if (endIdx !== -1) {
      const content = text.substring(absoluteStart + 1, endIdx);
      obj[key] = parseObjectsInArray(content);
      cleanedText =
        text.substring(0, arrayMatch.index) + text.substring(endIdx + 1);
    }
  }

  const pairRegex = /(\w+)\s*=\s*("[^"]*")/g;
  let match;
  while ((match = pairRegex.exec(cleanedText)) !== null) {
    const key = match[1];
    try {
      obj[key] = JSON.parse(match[2]);
    } catch (e) {
      obj[key] = match[2].replace(/^"|"$/g, "");
    }
  }
  return obj;
}

function renderSection(section, container) {
  if (!section.title) return;

  const secElement = document.createElement("section");
  const h2 = document.createElement("h2");
  h2.innerText = section.title;
  secElement.appendChild(h2);

  if (section.items && section.items.length > 0) {
    secElement.appendChild(renderList(section.items));
  }

  container.appendChild(secElement);
}

function renderList(items) {
  const ul = document.createElement("ul");
  items.forEach((item) => {
    const li = document.createElement("li");

    if (item.items) {
      li.innerText = item.title;
      li.appendChild(renderList(item.items));
    } else {
      const viewer =
        item.type === "nb" ? "notebook.html?nb=" : "viewer.html?img=";
      let html = `<a href="${viewer}${item.path}">${item.title}</a>`;
      if (item.extra_img) {
        html += ` (<a href="viewer.html?img=${item.extra_img}">img</a>)`;
      }
      li.innerHTML = html;
    }
    ul.appendChild(li);
  });
  return ul;
}

document.addEventListener("DOMContentLoaded", loadContent);
