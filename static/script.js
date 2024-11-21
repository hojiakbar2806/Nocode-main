let zoomLevel = 1;

function zoomIn() {
  zoomLevel += 0.1;
  document.getElementById("playground").style.transform =
    "scale(" + zoomLevel + ")";
}

function zoomOut() {
  zoomLevel -= 0.1;
  document.getElementById("playground").style.transform =
    "scale(" + zoomLevel + ")";
}
