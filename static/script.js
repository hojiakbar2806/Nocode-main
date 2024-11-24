const iframe = document.getElementById("playground_inner");
let selectedElementPath = null;

if (iframe !== null) {
  iframe.addEventListener("load", setupIframeInteractions);
}

function setupIframeInteractions() {
  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;

  // Style qo'shish
  addSelectionStyle(iframeDoc);

  // Event listener'larni qo'shish
  iframeDoc.addEventListener("click", handleElementSelection);
  iframeDoc.addEventListener("keydown", handleElementDeletion);
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

  // Root elementni tekshirish
  if (!rootElement) {
    console.error("root element topilmadi!");
    return;
  }

  // Oldingi tanlangan elementni tozalash
  clearPreviousSelection(iframeDoc);

  // Yangi elementni tanlash
  markSelectedElement(target);

  // Element yo'lini hisoblash
  const indexPath = getElementIndexPath(target, rootElement);
  selectedElementPath = indexPath;

  // Element haqida ma'lumot
  const elementInfo = getElementInfo(target);

  // Element ma'lumotini ko'rsatish
  target.setAttribute("data-element-info", elementInfo);

  console.log("Tanlangan element:", {
    type: target.tagName.toLowerCase(),
    class: target.className,
    id: target.id,
    path: indexPath,
    info: elementInfo,
  });
}

function handleElementDeletion(event) {
  if (
    (event.key === "Delete" || event.key === "Backspace") &&
    selectedElementPath
  ) {
    const projectName = window.location.pathname.split("/")[2];

    deleteElement(projectName, selectedElementPath).then((success) => {
      if (success) {
        console.log("Element muvaffaqiyatli o'chirildi:", selectedElementPath);
        selectedElementPath = null;
      }
    });
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

window.onload = function () {
  const modalElement = document.getElementById("myModal");
  const modalBtn = document.getElementById("modal_btn");

  if (!modalElement) {
    return;
  }

  var myModal = new bootstrap.Modal(modalElement, {
    keyboard: false,
  });

  modalBtn.addEventListener("click", function () {
    myModal.show();
  });
};

function addComponent(component, variant) {
  const projectName = window.location.pathname.split("/")[2];

  fetch(`/append-component/${projectName}`, {
    method: "POST",
    body: JSON.stringify({ component: component, variant: variant }),
  }).then(() => {
    window.location.reload();
  });
}
