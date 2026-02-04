document.getElementById("scan").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tabId = tabs[0].id;

    // Inject content.js manually (IMPORTANT)
    chrome.scripting.executeScript(
      {
        target: { tabId: tabId },
        files: ["content.js"],
      },
      () => {
        // Now send message AFTER injection
        chrome.tabs.sendMessage(tabId, { action: "GET_EMAIL" }, (response) => {
          const resultDiv = document.getElementById("result");

          if (chrome.runtime.lastError) {
            resultDiv.innerHTML = `<p class="error">❌ Open an email first</p>`;
            return;
          }

          if (!response || !response.text) {
            resultDiv.innerHTML = `<p class="error">❌ Open an email first</p>`;
            return;
          }

          fetch("http://127.0.0.1:5000/scan", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: response.text }),
          })
            .then((res) => res.json())
            .then((data) => {
              let riskClass = "low";
              if (data.level === "HIGH") riskClass = "high";
              else if (data.level === "MEDIUM") riskClass = "medium";

              resultDiv.innerHTML = `
                <p class="${riskClass}">Risk: ${data.risk}%</p>
                <p class="${riskClass}">Threat Level: ${data.level}</p>

                <p><b>Reasons:</b></p>
                <ul>
                  ${data.reasons.map((r) => `<li>${r}</li>`).join("")}
                </ul>

                <p><b>Safety Tip:</b> ${data.tip}</p>
              `;
            });
        });
      },
    );
  });
});
