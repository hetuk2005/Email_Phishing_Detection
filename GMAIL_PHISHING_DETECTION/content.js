function getEmailText() {
  const emailBody = document.querySelector("div.a3s");
  if (!emailBody) return null;
  return emailBody.innerText;
}

function getSenderEmail() {
  return document.querySelector(".gD")?.getAttribute("email") || "";
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "GET_EMAIL") {
    sendResponse({
      text: getEmailText(),
      sender: getSenderEmail(),
    });
  }
});
