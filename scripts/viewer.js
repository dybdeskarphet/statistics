document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const imageSrc = urlParams.get("src");

  if (!imageSrc)
    return console.error("No image specified. Use ?src=filename.jpg");

  document.title = `Document Viewer - ${imageSrc.split("/").pop()}`;

  const viewer = OpenSeadragon({
    id: "openseadragon1",
    prefixUrl: "",
    showNavigationControl: false,
    tileSources: { type: "image", url: imageSrc },
    animationTime: 0.4,
    zoomPerScroll: 1.4,
  });

  const resetHome = () => {
    if (viewer.world.getItemCount() === 0) return;
    const item = viewer.world.getItemAt(0);
    const zoom = viewer.viewport.imageToViewportZoom(
      viewer.viewport.getContainerSize().x / item.getContentSize().x,
    );
    viewer.viewport.zoomTo(zoom, new OpenSeadragon.Point(0.5, 0), true);
  };

  viewer.addHandler("open", resetHome);

  const actions = {
    "zoom-in": () => {
      viewer.viewport.zoomBy(1.2);
      viewer.viewport.applyConstraints();
    },
    "zoom-out": () => {
      viewer.viewport.zoomBy(0.8);
      viewer.viewport.applyConstraints();
    },
    home: resetHome,
    rotate: () =>
      viewer.viewport.setRotation(viewer.viewport.getRotation() + 90),
    "full-page": () => viewer.setFullScreen(!viewer.isFullScreen()),
    download: () => {
      const link = document.createElement("a");
      link.href = imageSrc;
      link.download = imageSrc.split("/").pop();
      link.click();
    },
  };

  Object.entries(actions).forEach(([id, handler]) => {
    document.getElementById(id)?.addEventListener("click", handler);
  });

  const toolbar = document.querySelector(".toolbar");
  const showBtn = document.getElementById("show-toolbar");

  const toggleMenu = (hide) => {
    toolbar.classList.toggle("hidden", hide);
    showBtn.classList.toggle("visible", hide);
  };

  document
    .getElementById("hide-toolbar")
    ?.addEventListener("click", () => toggleMenu(true));
  showBtn?.addEventListener("click", () => toggleMenu(false));
});
