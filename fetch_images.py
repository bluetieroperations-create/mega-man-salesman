import json
import re
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print('[Mega-Byte] Parsing vehicle list...')

vehicles = []
with open(r'C:\Users\maste\.openclaw\workspace\ariana_vehicles_clean.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or '|' not in line:
            continue
        parts = line.split('|')
        if len(parts) < 4:
            continue
        year_make = parts[1].strip()
        price = parts[2].strip()
        stock = ''
        miles = ''
        for p in parts[2:]:
            p = p.strip()
            if p.startswith('Stock #:'):
                stock = p.replace('Stock #:', '').strip()
            if p.startswith('Miles:'):
                miles = p.replace('Miles:', '').strip()
        
        year_match = re.match(r'^(\d{4})\s+(.+)$', year_make)
        if year_match and stock:
            year = year_match.group(1)
            make_model = year_match.group(2)
            vehicles.append({'year': year, 'make_model': make_model, 'price': price, 'stock': stock, 'miles': miles})

print(f'[Mega-Byte] Parsed {len(vehicles)} vehicles')

# Set up Selenium
options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(20)

def get_image_url(stock_num):
    try:
        url = f'https://www.arianamotorslv.com/inventory/{stock_num}/'
        driver.get(url)
        time.sleep(3)
        imgs = driver.find_elements(By.CSS_SELECTOR, 'img[src*="dealercenter"], img[src*=" dealercenter"]')
        for img in imgs[:1]:
            src = img.get_attribute('src')
            if src and ('dealercenter' in src or 'cdn' in src):
                return src
        return ''
    except Exception as e:
        return ''

# Fetch images for all vehicles
print('[Mega-Byte] Fetching images for all 169 vehicles...')
image_map = {}
for i, v in enumerate(vehicles):
    print(f'  [{i+1}/{len(vehicles)}] Stock {v["stock"]}...', end='')
    img = get_image_url(v['stock'])
    image_map[v['stock']] = img
    if img:
        print(f' GOT IMAGE')
    else:
        print(f' no image')
    time.sleep(1)

driver.quit()

# Save image map
with open(r'C:\Users\maste\.openclaw\workspace\image_map.json', 'w', encoding='utf-8') as f:
    json.dump(image_map, f, ensure_ascii=False, indent=2)

print(f'[Mega-Byte] Image fetch complete. Saved to image_map.json')
print(f'  Vehicles with images: {sum(1 for v in image_map.values() if v)}')
