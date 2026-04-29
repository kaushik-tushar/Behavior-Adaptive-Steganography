/* -------------------------------------------------
   Behavior-Adaptive Steganography – Frontend Logic
-------------------------------------------------- */

/* ---------- UPDATE BEHAVIOR PROFILE ---------- */
async function updateBehavior() {
    const riskLevel = document.getElementById("riskLevel").value;
    const fileSize = document.getElementById("fileSize").value;

    const response = await fetch("/update_behavior", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            risk_level: riskLevel,
            avg_file_size_kb: parseInt(fileSize)
        })
    });

    const result = await response.json();

    const status = document.getElementById("behaviorStatus");
    status.textContent = "✔ Behavior profile updated successfully";
    status.style.color = "#22c55e";

    console.log("Updated Behavior:", result.behavior);
}

/* ---------- EXTRACT MESSAGE ---------- */
async function extractMessage() {
    const fileInput = document.getElementById("extractImage");
    const output = document.getElementById("extractOutput");

    if (!fileInput.files.length) {
        output.textContent = "❌ Please select a stego image first";
        return;
    }

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    output.textContent = "⏳ Extracting message...";

    try {
        const response = await fetch("/extract", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        output.textContent = result.extracted_message;
    } catch (err) {
        output.textContent = "❌ Extraction failed";
    }
}

/* ---------- UI ENHANCEMENTS ---------- */
document.addEventListener("DOMContentLoaded", () => {
    console.log("Behavior-Adaptive Steganography UI Loaded");
});
