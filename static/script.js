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
    modify: "Modify",
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
          placeholder: "e.g., img-fluid rounded",
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
          placeholder: "e.g., form-control",
        },
      ],
    },
    text: {
      label: "Text",
      options: [
        { id: "textContent", label: "Text Content", type: "text" },
        {
          id: "textTag",
          label: "HTML Tag",
          type: "select",
          choices: ["p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "div"],
        },
        {
          id: "textClass",
          label: "CSS Classes",
          type: "text",
          placeholder: "e.g., text-muted",
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
          placeholder: "e.g., btn btn-primary",
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
          placeholder: "e.g., btn btn-link",
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
    renderMainOptions();
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

  function renderMainOptions() {
    switch (editMode) {
      case "insert":
        renderInsertOptions();
        break;
      case "replace":
        renderReplaceOptions();
        break;
      case "modify":
        renderModifyOptions();
        break;
      default:
        renderDefaultOptions();
    }
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

  function renderReplaceOptions() {
    renderInsertOptions();
  }

  function renderModifyOptions() {
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    const selectedElement = iframeDoc.querySelector(".selected-element");

    const componentType = detectComponentType(selectedElement);

    options.innerHTML = `
      <div class="mb-3">
        <h5>Modify: ${COMPONENT_TYPES[componentType]?.label || "Component"}</h5>
      </div>
      ${renderComponentOptions(componentType, selectedElement)}
      <button class="btn btn-primary w-100" onclick="window.saveComponent('modify')">Update Component</button>
    `;
  }

  function detectComponentType(element) {
    if (element.tagName === "IMG") return "image";
    if (element.tagName === "INPUT") return "input";
    if (
      ["P", "H1", "H2", "H3", "H4", "H5", "H6", "SPAN", "DIV"].includes(
        element.tagName
      )
    )
      return "text";
    if (element.tagName === "BUTTON") return "button";
    if (element.tagName === "A") return "link";
    return null;
  }

  function renderComponentOptions(type, element) {
    if (!type || !COMPONENT_TYPES[type]) return "";

    return COMPONENT_TYPES[type].options
      .map((option) => {
        let input = "";
        switch (option.type) {
          case "select":
            input = `
            <select id="${option.id}" class="form-select">
              ${option.choices
                .map(
                  (choice) => `
                <option value="${choice}" ${
                    element[option.id] === choice ? "selected" : ""
                  }>
                  ${choice}
                </option>
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
              value="${element[option.id] || ""}"
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
    const projectName = window.location.pathname.split("/")[2];

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
        content = `
          <${textTag} class="${textClass}">${textContent}</${textTag}>
        `;
        break;
      case "button":
        const buttonContent = document.getElementById("buttonContent").value;
        const buttonType = document.getElementById("buttonType").value;
        const buttonClass = document.getElementById("buttonClass").value;
        content = `
          <button 
            type="${buttonType}" 
            class="${buttonClass}"
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
            class="${linkClass}"
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

    const endpoint =
      mode === "insert"
        ? `/update-element/append/${projectName}`
        : `/update-element/replace/${projectName}`;

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
      const projectName = window.location.pathname.split("/")[2];

      fetch(`/update-element/delete/${projectName}`, {
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
    renderMainOptions();
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
