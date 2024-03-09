var current_url = "";

chrome.tabs.query({'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT},
   function(tabs){
      current_url = tabs[0].url;
      document.getElementById("url").innerHTML = tabs[0].url;
      reportBack();
   }
);


chrome.tabs.onUpdated.addListener(
  function(tabId, changeInfo, tab) {
    if (changeInfo.url) {
      current_url = tabs[0].url;
      document.getElementById("url").innerHTML = tabs[0].url;
      reportBack();
    }
  }
);

chrome.tabs.onActivated.addListener(
  function(tabId, changeInfo, tab) {
    if (changeInfo.url) {
      current_url = tabs[0].url;
      document.getElementById("url").innerHTML = tabs[0].url;
      reportBack();
    }
  }
);


async function reportBack() {
  const formData = new FormData();
  formData.append("curr_url", current_url);

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
