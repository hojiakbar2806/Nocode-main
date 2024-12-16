document.addEventListener("DOMContentLoaded", () => {
  const iframe = document.getElementById("playground_inner");
  const optionDrawer = document.querySelector(".options-drawer");
  const options = document.querySelector(".options");
  const optionsHead = document.querySelector(".options-head");

  let selectedElementPath = null;
  let editMode = null;

  const EDIT_MODES = {
    insert: "Insert",
    replace: "Replace",
    append: "Append",
  };

  const COMPONENT_TYPES = {
    image: {
      label: "Image",
      options: [
        { id: "imageUrl", label: "Image URL", type: "text" },
        { id: "imageAlt", label: "Alt Text", type: "text" },
        {
          id: "imageClass",
          label: "CSS Classes",
          type: "text",
          placeholder: "bootstrap class",
        },
      ],
    },
    input: {
      label: "Input",
      options: [
        {
          id: "inputType",
          label: "Input Type",
          type: "select",
          choices: [
            "text",
            "number",
            "email",
            "password",
            "tel",
            "url",
            "date",
          ],
        },
        { id: "inputPlaceholder", label: "Placeholder", type: "text" },
        {
          id: "inputClass",
          label: "CSS Classes",
          type: "text",
          placeholder: "bootstrap class",
        },
      ],
    },
    text: {
      label: "Text",
      options: [
        { id: "textContent", label: "Text Content", type: "text" },
        {
          id: "textTag",
          label: "Type",
          type: "select",
          choices: [
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "span",
            "div",
            "text",
          ],
        },
        {
          id: "textClass",
          label: "CSS Classes",
          type: "text",
          placeholder: "bootstrap class",
        },
      ],
    },
    button: {
      label: "Button",
      options: [
        { id: "buttonContent", label: "Button Text", type: "text" },
        {
          id: "buttonType",
          label: "Button Type",
          type: "select",
          choices: ["button", "submit", "reset"],
        },
        {
          id: "buttonClass",
          label: "CSS Classes",
          type: "text",
          placeholder: "bootstrap class",
        },
      ],
    },
    link: {
      label: "Link",
      options: [
        { id: "linkHref", label: "Link URL", type: "text" },
        { id: "linkContent", label: "Link Text", type: "text" },
        {
          id: "linkClass",
          label: "CSS Classes",
          type: "text",
          placeholder: "bootstrap class",
        },
      ],
    },
  };

  function initEditor() {
    if (iframe !== null) {
      iframe.addEventListener("load", () => {
        const iframeDoc =
          iframe.contentDocument || iframe.contentWindow.document;
        addSelectionStyle(iframeDoc);
        iframeDoc.addEventListener("click", handleElementSelection);
        iframeDoc.addEventListener("keydown", handleElementDeletion);
      });
    }
  }

  function addSelectionStyle(doc) {
    const style = doc.createElement("style");
    style.textContent = `
    .selected-element {
      border: 2px dashed blue !important;
      transition: all 0.3s ease;
    }
    .selected-element:hover {
      box-shadow: 0 0 10px rgba(0,0,255,0.5);
    }
  `;
    doc.head.appendChild(style);
  }

  function handleElementSelection(event) {
    event.preventDefault();
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    const target = event.target;
    const rootElement = iframeDoc.getElementById("root");

    clearPreviousSelection(iframeDoc);
    markSelectedElement(target);

    const indexPath = getElementIndexPath(target, rootElement);
    selectedElementPath = indexPath;

    optionDrawer.classList.add("show");
    renderOptionsHead();
    if (mode) renderInsertOptions();
  }

  function renderOptionsHead() {
    optionsHead.innerHTML = `
      <div class="btn-group mb-2" role="group" aria-label="Edit Mode">
        ${Object.entries(EDIT_MODES)
          .map(
            ([mode, label]) => `
          <button 
            class="btn btn-sm ${
              editMode === mode ? "btn-primary" : "btn-outline-primary"
            }" 
            onclick="window.setEditMode('${mode}')"
          >
            ${label}
          </button>
        `
          )
          .join("")}
      </div>
      <button class="btn btn-sm btn-secondary" onclick="window.closeDrawer()">Close</button>
    `;
  }

  function renderInsertOptions() {
    options.innerHTML = `
      <div class="mb-3">
        <label for="componentType" class="form-label">Choose Component</label>
        <select id="componentType" class="form-select" onchange="window.showComponentOptions()">
          <option value="">Select...</option>
          ${Object.entries(COMPONENT_TYPES)
            .map(
              ([type, config]) =>
                `<option value="${type}">${config.label}</option>`
            )
            .join("")}
        </select>
      </div>
      <div id="componentOptions" class="mb-3"></div>
      <button class="btn btn-primary w-100" onclick="window.saveComponent('insert')">Insert Component</button>
    `;
  }

  window.showComponentOptions = function () {
    const componentType = document.getElementById("componentType").value;
    const componentOptions = document.getElementById("componentOptions");

    if (!componentType) {
      componentOptions.innerHTML = "";
      return;
    }

    const componentConfig = COMPONENT_TYPES[componentType];
    if (!componentConfig) return;

    componentOptions.innerHTML = componentConfig.options
      .map((option) => {
        let input = "";
        switch (option.type) {
          case "select":
            input = `
            <select id="${option.id}" class="form-select">
              ${option.choices
                .map(
                  (choice) => `
                <option value="${choice}">${choice}</option>
              `
                )
                .join("")}
            </select>
          `;
            break;
          case "text":
          default:
            input = `
            <input 
              type="text" 
              id="${option.id}" 
              class="form-control" 
              placeholder="${option.placeholder || ""}"
            >
          `;
        }

        return `
        <div class="mb-3">
          <label for="${option.id}" class="form-label">${option.label}</label>
          ${input}
        </div>
      `;
      })
      .join("");
  };

  window.saveComponent = function (mode) {
    const componentType = document.getElementById("componentType").value;
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    const rootElement = iframeDoc.getElementById("root");

    if (!rootElement) {
      alert("Root element not found!");
      return;
    }

    let content = "";
    const projectName = window.location.pathname.split("/")[3];

    switch (componentType) {
      case "image":
        const imageUrl = document.getElementById("imageUrl").value;
        const imageAlt = document.getElementById("imageAlt").value;
        const imageClass = document.getElementById("imageClass").value;
        content = `
          <img 
            src="${imageUrl}" 
            alt="${imageAlt}" 
            class="img-fluid ${imageClass}"
          >
        `;
        break;
      case "input":
        const inputType = document.getElementById("inputType").value;
        const inputPlaceholder =
          document.getElementById("inputPlaceholder").value;
        const inputClass = document.getElementById("inputClass").value;
        content = `
          <input 
            type="${inputType}" 
            class="form-control ${inputClass}"
            placeholder="${inputPlaceholder}"
          >
        `;
        break;
      case "text":
        const textContent = document.getElementById("textContent").value;
        const textTag = document.getElementById("textTag").value;
        const textClass = document.getElementById("textClass").value;
        if (textTag == "text") {
          content = `${textContent}`;
        } else {
          content = `
          <${textTag} class="${textClass}">${textContent}</${textTag}>
        `;
        }
        break;
      case "button":
        const buttonContent = document.getElementById("buttonContent").value;
        const buttonType = document.getElementById("buttonType").value;
        const buttonClass = document.getElementById("buttonClass").value;
        content = `
          <button 
            type="${buttonType}" 
            class="${buttonClass} btn btn-primary"
          >
            ${buttonContent}
          </button>
        `;
        break;
      case "link":
        const linkHref = document.getElementById("linkHref").value;
        const linkContent = document.getElementById("linkContent").value;
        const linkClass = document.getElementById("linkClass").value;
        content = `
          <a 
            href="${linkHref}" 
            class="${linkClass} nav-link"
          >
            ${linkContent}
          </a>
        `;
        break;
    }

    const payload = {
      content: content,
      elementIndex: selectedElementPath,
    };

    const endpoint = `/nocode/update-element/${editMode}/${projectName}`;

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then(() => window.location.reload())
      .catch((error) => {
        console.error("Error saving component:", error);
        alert("Failed to save component. Please try again.");
      });
  };

  function handleElementDeletion(event) {
    if (
      (event.key === "Delete" || event.key === "Backspace") &&
      selectedElementPath
    ) {
      const projectName = window.location.pathname.split("/")[3];

      fetch(`/nocode/update-element/delete/${projectName}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          elementIndex: selectedElementPath,
        }),
      })
        .then(() => window.location.reload())
        .catch((error) => {
          console.error("Error deleting element:", error);
          alert("Failed to delete element. Please try again.");
        });
    }
  }

  window.closeDrawer = function () {
    optionDrawer.classList.remove("show");
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    clearPreviousSelection(iframeDoc);
  };

  window.setEditMode = function (mode) {
    editMode = mode;
    renderOptionsHead();
    renderInsertOptions();
  };

  function getElementIndexPath(element, rootElement) {
    const path = [];
    let currentElement = element;

    while (currentElement !== rootElement) {
      const children = Array.from(currentElement.parentNode.children);
      const index = children.indexOf(currentElement);
      path.unshift(index);
      currentElement = currentElement.parentNode;
    }

    return path;
  }

  function clearPreviousSelection(doc) {
    const previousSelection = doc.querySelector(".selected-element");
    if (previousSelection) {
      previousSelection.classList.remove("selected-element");
    }
  }

  function markSelectedElement(element) {
    element.classList.add("selected-element");
  }

  initEditor();
});
