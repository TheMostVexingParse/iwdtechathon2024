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
    const response = await fetch("http://127.0.0.1:5000", {
      method: "POST",
      body: formData,
      mode: 'no-cors',
    });
    console.log(await response.json());
  } catch (e) {
    console.error(e);
  }
}




// function launchPopup(content) {
//   const popupWindow = window.open("", "Popup", "width=400,height=300");
  
//   popupWindow.document.body.innerHTML = null;

//   const popupContent = `
//     <!DOCTYPE html>
//     <html>
//       <head>
//         <title>İstatistikler</title>
//         <link href="popup.css" rel="stylesheet">
//         <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
//       </head>
//       <body>
//         <h1>İstatistikler</h1>
//         <div role="main">
//           <span><h4>Son İzlenenler: </h4>${content}</span>
//         </div>
//       </body>
//     </html>
//   `;

//   popupWindow.document.write(popupContent);
// }

// setInterval(async () => {
  
//   chrome.runtime.sendMessage( 
//       "http://192.168.1.64:5000/statistics/",
//       data => launchPopup(data)
//   );
  
// }, 100);

    

