// Iframe bilan ishlash va element tanlash qismi
const iframe = document.getElementById("playground_inner");

if (iframe !== null) {
  iframe.addEventListener("load", () => {
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;

    iframeDoc.addEventListener("dblclick", (event) => {
      event.preventDefault();
      const target = event.target;

      const prevSelected = iframeDoc.querySelector(".selected-element");
      if (prevSelected) {
        prevSelected.classList.remove("selected-element");
      }

      target.classList.add("selected-element");

      const elementInfo = {
        tag: target.tagName.toLowerCase(),
        id: target.id || "ID yo'q",
        classes: target.className || "Class yo'q",
        content: target.textContent.trim() || "Kontent yo'q",
      };
      window.parent.postMessage(
        { type: "element-selected", data: elementInfo },
        "*"
      );
    });

    const style = iframeDoc.createElement("style");
    style.textContent = `
        .selected-element {
            border: 1px solid red !important;
        }
    `;
    iframeDoc.head.appendChild(style);
  });
}

window.addEventListener("message", (event) => {
  if (event.data.type === "element-selected") {
    const elementInfo = event.data.data;
    console.log(`
            <strong>Element haqida ma'lumot:</strong><br>
            Teg: ${elementInfo.tag} <br>
            ID: ${elementInfo.id} <br>
            Classlar: ${elementInfo.classes} <br>
            Kontent: ${elementInfo.content}
        `);
  }
});

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
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        window.location.reload();
        print("success");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}



(function () {
  "use strict";
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl);
  });
})();
