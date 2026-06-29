function scrapeAmazon() {
  const title = document.querySelector("#productTitle")?.innerText?.trim();
  if (!title) return null;                       // not a product page

  const price = document
    .querySelector(".a-price .a-offscreen")
    ?.innerText?.replace(/[^\d.]/g, "");
  const brand = document.querySelector("#bylineInfo")?.innerText?.trim();
  const image = document.querySelector("#landingImage")?.src;
  const description = document.querySelector("#feature-bullets")?.innerText?.trim();

  return {
    external_id: location.pathname,              // simple unique-ish id
    title,
    brand,
    price: price ? parseFloat(price) : null,
    image,
    description,
    source_url: location.href,
  };
}

const product = scrapeAmazon();
if (product) {
  // hand the scraped data to the background worker
  chrome.runtime.sendMessage({ type: "PRODUCT_FOUND", product });
}