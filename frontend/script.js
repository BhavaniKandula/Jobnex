
const form = document.getElementById("analyze-Form");
const resumeInput = document.getElementById("resume_text");
const jobDescriptionInput = document.getElementById("jd_text");
const button = document.getElementById("analyze-button");
const status = document.getElementById("status");
const results = document.getElementById("results");
const resultData = document.getElementById("result-data");

const isLocalStandalone = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || !window.location.origin.startsWith("http");
const API_BASE = (isLocalStandalone && window.location.port !== "8000") 
    ? "http://127.0.0.1:8000" 
    : "";

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    button.disabled = true;
    status.textContent = "Analyzing resume...";
    results.hidden = true;

    try {
        const response = await fetch(
            `${API_BASE}/api/analyse`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    resume_text: resumeInput.value,
                    jd_text: jobDescriptionInput.value
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        resultData.textContent = JSON.stringify(data, null, 2);
        results.hidden = false;
        status.textContent = "Analysis completed successfully!";

    } catch (error) {
        status.textContent =
            "Could not analyze resume: " + error.message;

    } finally {
        button.disabled = false;
    }
});