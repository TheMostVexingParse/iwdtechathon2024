chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.checkIfUrlExists) {
      fetch(request.checkIfUrlExists, { method: "HEAD" })
        .then(response => sendResponse({ status: response.ok }))
        .catch(error => sendResponse({ status: false, error: JSON.stringify(error) }))
    }
    return true
  })