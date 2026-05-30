document.addEventListener("DOMContentLoaded", () => {
    const ingredientsList = document.getElementById("ingredients-list");
    const addIngredientBtn = document.getElementById("add-ingredient-btn");

    const instructionsList = document.getElementById("instructions-list");
    const addStepBtn = document.getElementById("add-step-btn");

    function createIngredientRow() {
        const row = document.createElement("div");
        row.className = "input-group mb-3 ingredient-row";

        row.innerHTML = `
            <input
                type="text"
                class="form-control"
                name="ingredients"
                placeholder="Ex: 2 chicken breasts"
            >

            <button
                class="btn btn-outline-danger remove-ingredient-btn"
                type="button">
                Remove
            </button>
        `;

        return row;
    }

    function createInstructionRow(stepNumber) {
        const row = document.createElement("div");
        row.className = "input-group mb-3 instruction-row";

        row.innerHTML = `
            <span class="input-group-text step-number">${stepNumber}</span>

            <textarea
                class="form-control"
                name="instructions"
                rows="2"
                placeholder="Describe the cooking step"></textarea>

            <button
                class="btn btn-outline-danger remove-step-btn"
                type="button">
                Remove
            </button>
        `;

        return row;
    }

    function renumberSteps() {
        const stepNumbers = instructionsList.querySelectorAll(".step-number");

        stepNumbers.forEach((stepNumber, index) => {
            stepNumber.textContent = index + 1;
        });
    }

    addIngredientBtn.addEventListener("click", () => {
        ingredientsList.appendChild(createIngredientRow());
    });

    addStepBtn.addEventListener("click", () => {
        const nextStepNumber = instructionsList.querySelectorAll(".instruction-row").length + 1;
        instructionsList.appendChild(createInstructionRow(nextStepNumber));
    });

    ingredientsList.addEventListener("click", (event) => {
        if (event.target.classList.contains("remove-ingredient-btn")) {
            event.target.closest(".ingredient-row").remove();
        }
    });

    instructionsList.addEventListener("click", (event) => {
        if (event.target.classList.contains("remove-step-btn")) {
            event.target.closest(".instruction-row").remove();
            renumberSteps();
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const imageInput = document.getElementById("recipe-image-input");
    const imagePreview = document.getElementById("recipe-image-preview");
    const imagePlaceholder = document.getElementById("recipe-image-placeholder");

    if (!imageInput || !imagePreview) {
        return;
    }

    imageInput.addEventListener("change", () => {
        const file = imageInput.files?.[0];

        if (!file) {
            return;
        }

        if (!file.type.startsWith("image/")) {
            imageInput.value = "";
            return;
        }

        imagePreview.src = URL.createObjectURL(file);
        imagePreview.classList.remove("d-none");

        if (imagePlaceholder) {
            imagePlaceholder.classList.add("d-none");
        }
    });
});