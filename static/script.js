const optionDrawer = document.querySelector(".options-drawer");
const closeOptionBtn = document.querySelector(".close-option-button");

closeOptionBtn.addEventListener("click", () => {
  optionDrawer.classList.remove("show");
});

const iframe = document.getElementById("playground_inner");
let selectedElementPath = null;

if (iframe !== null) {
  iframe.addEventListener("load", () => {
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    addSelectionStyle(iframeDoc);

    iframeDoc.addEventListener("dblclick", handleElementSelection);
    iframeDoc.addEventListener("keydown", handleElementDeletion);
  });
}

function addSelectionStyle(doc) {
  const style = doc.createElement("style");
  style.textContent = `
    .selected-element {
      border: 2px solid red !important;
    }
  `;
  doc.head.appendChild(style);
}

function handleElementSelection(event) {
  event.preventDefault();
  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
  const target = event.target;
  const rootElement = iframeDoc.getElementById("root");

  if (optionDrawer) {
    optionDrawer.classList.add("show");
  }

  console.log(optionDrawer);
  if (!rootElement) {
    console.error("root element topilmadi!");
    return;
  }

  clearPreviousSelection(iframeDoc);
  markSelectedElement(target);

  const indexPath = getElementIndexPath(target, rootElement);
  selectedElementPath = indexPath;
  target.setAttribute("data-element-info", getElementInfo(target));
}

function handleElementDeletion(event) {
  if (
    (event.key === "Delete" || event.key === "Backspace") &&
    selectedElementPath
  ) {
    const projectName = window.location.pathname.split("/")[2];
    deleteElement(projectName, selectedElementPath);
  }
}

function getElementIndexPath(element, rootElement) {
  const path = [];
  let currentElement = element;

  while (
    currentElement &&
    currentElement !== rootElement &&
    currentElement.parentNode
  ) {
    const parent = currentElement.parentNode;
    const children = Array.from(parent.children);
    const index = children.indexOf(currentElement);
    path.unshift(index); // Indeksni boshiga qo'shamiz
    currentElement = parent;
  }

  return path;
}

function clearPreviousSelection(doc) {
  const prevSelected = doc.querySelector(".selected-element");
  if (prevSelected) {
    prevSelected.classList.remove("selected-element");
    prevSelected.removeAttribute("data-element-info");
  }
}

function markSelectedElement(element) {
  element.classList.add("selected-element");
}

function getElementInfo(element) {
  const tag = element.tagName.toLowerCase();
  const id = element.id ? `#${element.id}` : "";
  const classes = element.className
    ? `.${element.className.split(" ").join(".")}`
    : "";
  return `${tag}${id}${classes}`;
}

function deleteElement(projectName, elementPath) {
  fetch(`/update-element/delete/${projectName}`, {
    method: "POST",
    body: JSON.stringify({ elementPath }),
  }).then(() => window.location.reload());
}

function addComponent(component, variant) {
  const projectName = window.location.pathname.split("/")[2];

  fetch(`/append-component/${projectName}`, {
    method: "POST",
    body: JSON.stringify({ component: component, variant: variant }),
  }).then(() => {
    window.location.reload();
  });
}
