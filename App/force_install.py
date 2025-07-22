from playwright.sync_api import sync_playwright

def install_chromium():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        print("✅ Chromium launched successfully.")
        browser.close()

if __name__ == "__main__":
    install_chromium()
    