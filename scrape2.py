import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print('[Mega-Byte] Starting Chrome...')

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(30)

all_vehicles = []

for page in range(1, 9):
    url = f'https://www.arianamotorslv.com/inventory/?pager=24&page_no={page}'
    print(f'[Mega-Byte] Loading page {page}/8...')
    try:
        driver.get(url)
        time.sleep(6)
        cars = driver.find_elements(By.CSS_SELECTOR, '.vehicle-card, .vehicle-item, .inv-card, article, [class*="vehicle"], [class*="car"]')
        print(f'  Found {len(cars)} elements')
        page_vehicles = []
        for car in cars:
            try:
                text = car.text.strip()
                if len(text) > 30:
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

total = sum(len(p.get("vehicles", [])) for p in all_vehicles)
print(f'[Mega-Byte] Done. Extracted {total} total vehicle entries.')