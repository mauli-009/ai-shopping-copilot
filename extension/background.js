const API = "http://localhost:8000";

// Allow opening the side panel by clicking the toolbar icon
chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch(() => {});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "PRODUCT_FOUND") {
    chrome.storage.local.set({ lastProduct: msg.product });
    // Phase 2: send to backend with JWT and store the AI result
  }
});