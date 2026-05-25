document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const imagePath = urlParams.get("img") || urlParams.get("src");

  const imageTitle = document.getElementById("image-title");
  const imagePathDisplay = document.getElementById("image-path");

  if (imagePath) {
    const fileName = imagePath.split("/").pop();
    imagePathDisplay.innerText = imagePath;
    imagePathDisplay.href = imagePath;
    imageTitle.innerText = fileName;
    document.title = `${fileName} | kavakci.dev`;

    const viewer = OpenSeadragon({
      id: "openseadragon-viewer",
      prefixUrl:
        "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
      tileSources: {
        type: "image",
        url: imagePath,
      },
      showNavigationControl: false,
      defaultZoomLevel: 1,
      minZoomLevel: 0.1,
      visibilityRatio: 1.0,
      constrainDuringPan: true,
      imageLoaderLimit: 1,
    });

    const resetView = (immediately) => {
      viewer.viewport.zoomTo(1, null, immediately);
      const bounds = viewer.viewport.getBounds();
      viewer.viewport.panTo(
        new OpenSeadragon.Point(0.5, bounds.height / 2),
        immediately,
      );
    };

    viewer.addHandler("open", () => {
      resetView(true);
    });

    document.getElementById("zoom-in").onclick = () =>
      viewer.viewport.zoomBy(1.2);
    document.getElementById("zoom-out").onclick = () =>
      viewer.viewport.zoomBy(0.8);
    document.getElementById("home").onclick = () => resetView(false);
    document.getElementById("full-page").onclick = () =>
      viewer.setFullPage(true);

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        viewer.setFullPage(false);
      }
    });
  } else {
    if (imageTitle) imageTitle.innerText = "No image specified.";
  }
});
