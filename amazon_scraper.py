from playwright.sync_api import sync_playwright

def scrape_amazon_product(url):
    with sync_playwright() as p:
        # Launch browser visibly so we can solve CAPTCHA if needed
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

        page.goto(url, timeout=90000)  # 90 seconds

        # Try different price locators
        price = None
        for selector in ["span.a-price-whole", "span.a-offscreen"]:
            try:
                price = page.locator(selector).first.text_content(timeout=5000)
                if price:
                    break
            except:
                pass

        # Bank offers
        try:
            bank_offers_section = page.locator("div#bankPromotions_feature_div")
            bank_offers = bank_offers_section.all_inner_texts()
        except:
            bank_offers = []

        # Shipping info
        try:
            shipping = page.locator("#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE").text_content(timeout=5000)
        except:
            shipping = None

        browser.close()

        return {
            "price": price.strip() if price else None,
            "bank_offers": [offer.strip() for offer in bank_offers if offer.strip()],
            "shipping": shipping.strip() if shipping else None
        }

if __name__ == "__main__":
    product_url = input("Enter Amazon.in product URL: ")
    result = scrape_amazon_product(product_url)
    print(result)
