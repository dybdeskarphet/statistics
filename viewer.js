document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  const imageSrc = urlParams.get("src");

  if (!imageSrc) {
    console.error("No image specified. Use ?src=filename.jpg");
    return;
  }

  var viewer = OpenSeadragon({
    id: "openseadragon1",
    prefixUrl: "",
    showNavigationControl: false,
    tileSources: {
      type: "image",
      url: imageSrc,
    },
    animationTime: 0.4,
    zoomPerScroll: 1.4,
  });

  viewer.addHandler("open", function () {
    var zoomLevel =
      viewer.viewport.getContainerSize().x /
      viewer.world.getItemAt(0).getContentSize().x;
    zoomLevel = viewer.viewport.imageToViewportZoom(zoomLevel);
    viewer.viewport.zoomTo(zoomLevel, new OpenSeadragon.Point(0.5, 0), true);
  });

  function bindAction(id, action) {
    const btn = document.getElementById(id);
    if (btn) btn.onclick = action;
  }

  bindAction("zoom-in", function () {
    viewer.viewport.zoomBy(1.2);
    viewer.viewport.applyConstraints();
  });

  bindAction("zoom-out", function () {
    viewer.viewport.zoomBy(0.8);
    viewer.viewport.applyConstraints();
  });

  bindAction("home", function () {
    viewer.viewport.goHome();
  });

  bindAction("rotate", function () {
    var currentRotation = viewer.viewport.getRotation();
    viewer.viewport.setRotation(currentRotation + 90);
  });

  bindAction("full-page", function () {
    viewer.setFullScreen(!viewer.isFullScreen());
  });

  bindAction("download", function () {
    const link = document.createElement("a");
    link.href = imageSrc;
    link.download = imageSrc.split("/").pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  const toolbar = document.querySelector(".toolbar");
  const hideBtn = document.getElementById("hide-toolbar");
  const showBtn = document.getElementById("show-toolbar");

  // Function to hide the big menu and show the small button
  function hideMenu() {
    toolbar.classList.add("hidden");
    showBtn.classList.add("visible");
  }

  // Function to show the big menu and hide the small button
  function showMenu() {
    toolbar.classList.remove("hidden");
    showBtn.classList.remove("visible");
  }

  // Bind clicks
  if (hideBtn) hideBtn.onclick = hideMenu;
  if (showBtn) showBtn.onclick = showMenu;
});
