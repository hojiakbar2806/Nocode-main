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
  const projectName = window.location.pathname.split("/")[3];

  console.log("sa");

  fetch(`/nocode/append-component/${projectName}`, {
    method: "POST",
    body: JSON.stringify({ component: component, variant: variant }),
  }).then(() => {
    window.location.reload();
  });
}

function handleElementDeletion(event) {
  if (
    (event.key === "Delete" || event.key === "Backspace") &&
    selectedElementPath
  ) {
    const projectName = window.location.pathname.split("/")[2];

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


