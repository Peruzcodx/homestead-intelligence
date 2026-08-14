from playwright.sync_api import sync_playwright
from database.save_data import save_property
from analysis.change_detector import detect_changes
from database.change_events import save_change_events
from datetime import datetime
BASE_URL = "https://homestead-insights-hub.lovable.app"
LISTINGS_URL = f"{BASE_URL}/buy"

scrape_run_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# ============================================================
# HELPER
# ============================================================

def get_text(page, selector):
    element = page.locator(selector)

    if element.count() == 0:
        return None

    return element.first.inner_text().strip()


# ============================================================
# STEP 1 — DISCOVER ALL PROPERTY URLS
# ============================================================

def get_property_urls(page):

    property_urls = []
    page_number = 1

    while True:

        url = f"{LISTINGS_URL}?page={page_number}"

        print(f"\nChecking listing page {page_number}")
        print(url)

        page.goto(url, wait_until="networkidle")

        page.wait_for_timeout(1000)

        links = page.locator('a[href*="/property/"]')

        count = links.count()

        print(f"Property links found on page: {count}")

        # Stop if this page has no properties
        if count == 0:
            break

        new_urls = 0

        for i in range(count):

            href = links.nth(i).get_attribute("href")

            if not href:
                continue

            # Convert relative URL to absolute URL
            if href.startswith("/"):
                href = BASE_URL + href

            # Avoid duplicates
            if href not in property_urls:
                property_urls.append(href)
                new_urls += 1

        print(f"New URLs added: {new_urls}")
        print(f"Total URLs collected: {len(property_urls)}")

        # If this page produced no new URLs,
        # we have probably reached the end.
        if new_urls == 0:
            break

        page_number += 1

    return property_urls

# ============================================================
# STEP 2 — SCRAPE ONE PROPERTY
# ============================================================

def scrape_property(page, url):

    page.goto(url, wait_until="networkidle")

    page.wait_for_timeout(500)

    property_data = {

        "url": url,

        "title":
            get_text(page, '[data-field="title"]'),

        "price":
            get_text(page, '[data-field="price"]'),

        "street":
            get_text(page, '[data-field="street"]'),

        "city":
            get_text(page, '[data-field="city"]'),

        "state":
            get_text(page, '[data-field="state"]'),

        "zip":
            get_text(page, '[data-field="zip"]'),

        "neighborhood":
            get_text(page, '[data-field="neighborhood"]'),

        "bedrooms":
            get_text(page, '[data-field="bedrooms"]'),

        "bathrooms":
            get_text(page, '[data-field="bathrooms"]'),

        # IMPORTANT:
        # The actual HTML uses data-field="square-feet"
        "sqft":
            get_text(page, '[data-field="square-feet"]'),

        "property_type":
            get_text(page, '[data-field="property-type"]'),

        "availability":
            get_text(page, '[data-field="availability"]'),
    }

    return property_data


# ============================================================
# MAIN SCRAPER
# ============================================================

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # ========================================================
    # STAGE 1 — GET ALL PROPERTY URLS
    # ========================================================

    property_urls = get_property_urls(page)

    print("\n")
    print("=" * 60)
    print("URL DISCOVERY COMPLETE")
    print("=" * 60)

    print(f"Total property URLs found: {len(property_urls)}")


    # ========================================================
    # STAGE 2 — SCRAPE EVERY PROPERTY URL
    # ========================================================

    properties = []

    print("\n")
    print("=" * 60)
    print("STARTING PROPERTY SCRAPING")
    print("=" * 60)

    for index, url in enumerate(property_urls, start=1):

        print("\n")
        print(f"Scraping property {index}/{len(property_urls)}")
        print(url)

        try:

            property_data = scrape_property(page, url)

            properties.append(property_data)

            print("-" * 40)

            for field, value in property_data.items():

                print(f"{field}: {value}")

        except Exception as e:

            print(f"ERROR scraping property:")
            print(url)
            print(e)


    browser.close()
    # ============================================================
# VALIDATE SCRAPE RUN BEFORE SAVING
# ============================================================

if len(properties) != len(property_urls):

    print("\n")
    print("=" * 60)
    print("SCRAPE RUN REJECTED")
    print("=" * 60)

    print(
        f"Expected properties: {len(property_urls)}"
    )

    print(
        f"Successfully scraped: {len(properties)}"
    )

    print(
        "Incomplete scrape detected."
    )

    print(
        "No data was saved for this scrape run."
    )

else:

    print("\n")
    print("=" * 60)
    print("VALID SCRAPE RUN")
    print("=" * 60)

    print(
        f"Saving {len(properties)} properties..."
    )

    for property_data in properties:

        save_property(
            property_data,
            scrape_run_id
        )

    print(
        "Scrape run saved successfully."
    )
    print("\n")
    print("=" * 60)
    print("DETECTING MARKET CHANGES")
    print("=" * 60)

    changes = detect_changes()

    save_change_events(changes)

    print("Change events saved successfully.")

# ============================================================
# FINAL RESULTS
# ============================================================

print("\n")
print("=" * 60)
print("SCRAPING COMPLETE")
print("=" * 60)

print(f"Property URLs found: {len(property_urls)}")
print(f"Properties successfully scraped: {len(properties)}")