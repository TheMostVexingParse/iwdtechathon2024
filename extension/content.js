// contentScript.js

// Function to report current URL
async function reportBack(currentUrl) {
  const formData = new FormData();
  formData.append("curr_url", currentUrl);

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

// Function to track URL changes
function trackUrlChanges() {
  let currentUrl = window.location.href;

  // Report initial URL
  reportBack(currentUrl);

  // Listen for URL changes
  window.addEventListener("hashchange", () => {
    const newUrl = window.location.href;
    if (newUrl !== currentUrl) {
      currentUrl = newUrl;
      reportBack(currentUrl);
    }
  });

  // Listen for history state changes (like navigating within the same page)
  window.addEventListener("popstate", () => {
    const newUrl = window.location.href;
    if (newUrl !== currentUrl) {
      currentUrl = newUrl;
      reportBack(currentUrl);
    }
  });
}

// Start tracking URL changes when the content script is injected
trackUrlChanges();
