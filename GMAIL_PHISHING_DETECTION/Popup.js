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
              email: response.text || "test email",
            }),
          })
            .then((res) => {
              if (!res.ok) throw new Error("Server not responding");
              return res.json();
            })
            .then((data) => {
              console.log(data);
            })
            .catch((err) => {
              console.error(err);

              document.getElementById("result").innerHTML =
                "<p class='error'>Server is waking up... try again in 10 seconds</p>";
            });
        });
      },
    );
  });
});
