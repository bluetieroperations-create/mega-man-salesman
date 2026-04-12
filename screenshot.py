import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    os.makedirs(r"C:\Users\maste\.openclaw\workspace\images", exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width":1280,"height":800})
        await page.goto("https://www.arianamotorslv.com/inventory/")
        await page.wait_for_timeout(5000)
        cards = await page.query_selector_all(".vehicle-card, .inventory-item, [class*=vehicle], [class*=inventory]")
        print(f"Found {len(cards)} vehicle cards")
        for i, card in enumerate(cards[:9]):
            await card.screenshot(path=rf"C:\Users\maste\.openclaw\workspace\images\car{i+1}.png")
            print(f"Saved car{i+1}.png")
        if not cards:
            await page.screenshot(path=r"C:\Users\maste\.openclaw\workspace\images\inventory-full.png")
            print("Saved full page screenshot")
        await browser.close()

asyncio.run(main())
