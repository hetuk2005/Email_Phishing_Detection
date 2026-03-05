document.getElementById("scan").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tabId = tabs[0].id;

    chrome.scripting.executeScript(
      {
        target: { tabId: tabId },
        files: ["content.js"],
      },
      () => {
        chrome.tabs.sendMessage(tabId, { action: "GET_EMAIL" }, (response) => {
          const resultDiv = document.getElementById("result");

          if (chrome.runtime.lastError || !response || !response.text) {
            resultDiv.innerHTML = `<p class="error">Open an email first</p>`;
            return;
          }

          document.getElementById("loading").style.display = "block";

          fetch("https://email-phishing-detection-q3om.onrender.com/scan", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: response.text,
              sender: response.sender,
            }),
          })
            .then((res) => res.json())
            .then((data) => {
              // Badge color update
              if (data.level === "HIGH") {
                chrome.action.setBadgeText({ text: "!" });
                chrome.action.setBackgroundColor({ color: "red" });
              } else if (data.level === "MEDIUM") {
                chrome.action.setBadgeText({ text: "!" });
                chrome.action.setBackgroundColor({ color: "orange" });
              } else {
                chrome.action.setBadgeText({ text: "✓" });
                chrome.action.setBackgroundColor({ color: "green" });
              }

              let riskClass = "low";
              if (data.level === "HIGH") riskClass = "high";
              else if (data.level === "MEDIUM") riskClass = "medium";

              document.getElementById("loading").style.display = "none";

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
