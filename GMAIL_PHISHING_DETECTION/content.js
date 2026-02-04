function getEmailText() {
  const emailBody = document.querySelector("div.a3s");

  if (!emailBody) return null;

  return emailBody.innerText;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "GET_EMAIL") {
    sendResponse({ text: getEmailText() });
  }
});
