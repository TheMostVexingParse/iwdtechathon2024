// background.js

// Initialize current URL
let currentURL = "";

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "updateURL") {
    currentURL = message.url;
    reportBack();
  }
});

// Function to send data to the server
async function reportBack() {
  const formData = new FormData();
  formData.append("curr_url", currentURL);

  try {
    const response = await fetch("http://172.16.10.44:5000", {
      method: "POST",
      body: formData,
    });
    console.log(await response.json());
  } catch (e) {
    console.error(e);
  }
}
