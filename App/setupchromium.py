import asyncio
from pyppeteer import launch, executablePath

async def setup():
    browser = await launch(headless=True, args=["--no-sandbox"])
    print("Chromium successfully installed at:", executablePath())
    await browser.close()

asyncio.run(setup())