import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

print('[Mega-Byte Scraper] Starting...')

options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = uc.Chrome(options=options, version_main=None)
driver.set_page_load_timeout(30)

all_vehicles = []

for page in range(1, 9):
    url = f'https://www.arianamotorslv.com/inventory/?pager=24&page_no={page}'
    print(f'[Mega-Byte] Loading page {page}/8...')
    try:
        driver.get(url)
        time.sleep(5)
        
        cars = driver.find_elements(By.CSS_SELECTOR, '.vehicle-card, .vehicle-item, .inv-card, article, [class*="vehicle"]')
        print(f'  Found {len(cars)} elements')
        
        page_vehicles = []
        for car in cars:
            try:
                text = car.text.strip()
                if len(text) > 20:
                    page_vehicles.append(text)
            except:
                pass
        
        all_vehicles.append({'page': page, 'vehicles': page_vehicles})
        print(f'  Extracted {len(page_vehicles)} vehicle entries')
        
    except Exception as e:
        print(f'  Error on page {page}: {e}')
        all_vehicles.append({'page': page, 'error': str(e)})

driver.quit()

with open(r'C:\Users\maste\.openclaw\workspace\ariana_inventory.json', 'w', encoding='utf-8') as f:
    json.dump(all_vehicles, f, ensure_ascii=False, indent=2)

print(f'[Mega-Byte] Done. Saved {sum(len(p.get("vehicles", [])) for p in all_vehicles)} total vehicles.')
print('Output saved to ariana_inventory.json')