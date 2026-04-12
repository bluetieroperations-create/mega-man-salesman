import re

vehicles = []
with open(r'C:\Users\maste\.openclaw\workspace\ariana_vehicles_clean.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # format: "1. YEAR MAKE MODEL | Price | Stock #: XXX | Miles: YYY"
        parts = [p.strip() for p in line.split('|')]
        # parts[0] = "1. YEAR MAKE MODEL", parts[1] = price, parts[2] = Stock #, parts[3] = Miles
        if len(parts) < 4:
            continue
        
        # Extract year and make from parts[0] - starts with number
        first_part = parts[0]
        year_make_match = re.match(r'^\d+\.\s*(\d{4})\s+(.+)$', first_part)
        if not year_make_match:
            continue
        
        year = year_make_match.group(1)
        make_model = year_make_match.group(2).strip()
        price = parts[1].strip()
        stock = ''
        miles = ''
        for p in parts[2:]:
            p = p.strip()
            if p.startswith('Stock #:'):
                stock = p.replace('Stock #:', '').strip()
            if p.startswith('Miles:'):
                miles = p.replace('Miles:', '').strip()
        
        if stock:
            vehicles.append({'year': year, 'make_model': make_model, 'price': price, 'stock': stock, 'miles': miles})

print(f'Parsed {len(vehicles)} vehicles')

image_map = {}
try:
    import json
    with open(r'C:\Users\maste\.openclaw\workspace\image_map.json', 'r', encoding='utf-8') as f2:
        image_map = json.load(f2)
    print(f'Loaded {len(image_map)} image URLs')
except:
    print('No image map found')

cards_html = ''
for v in vehicles:
    stock = v['stock']
    img_url = image_map.get(stock, '')
    if not img_url:
        img_url = f'https://imagescf.dealercenter.net/640/480/{stock}.jpg'
    
    price_display = v['price'] if v['price'] else 'Call For Price'
    
    try:
        pval = int(v['price'].replace('$','').replace(',',''))
        if pval < 15000:
            badge_text = 'Under 15K'
        elif pval < 25000:
            badge_text = 'Hot Deal'
        else:
            badge_text = 'Premium'
    except:
        badge_text = 'In Stock'
    
    mm = v['make_model'].replace('"', "'")
    placeholder_url = 'https://via.placeholder.com/640x480/cc0000/ffffff?text={}+{}'.format(v['year'], mm.replace(' ', '+'))
    
    card = '<div class="vehicle-card"><div class="vehicle-img"><img src="{img}" alt="{yr} {mm}" loading="lazy" onerror="this.src=\'{pu}\'"><span class="vehicle-badge">{bt}</span></div><div class="vehicle-body"><div class="vehicle-year">{yr}</div><div class="vehicle-name">{mm}</div><div class="vehicle-type">Stock #{st} | {mi} mi</div><div class="vehicle-price">{pd}</div><a href="#contact" class="vehicle-cta">Inquire Now</a></div></div>'.format(
        img=img_url, yr=v['year'], mm=mm, pu=placeholder_url, bt=badge_text, st=v['stock'], mi=v['miles'], pd=price_display)
    cards_html += card + '\n'

form_options = ''
for v in vehicles:
    mm = v['make_model'].replace('"', "'")
    form_options += '<option value="{}">{} {}</option>\n'.format(mm, v['year'], mm)

print(f'Built {len(vehicles)} cards')

with open(r'C:\Users\maste\.openclaw\workspace\vehicle_cards.html', 'w', encoding='utf-8') as f:
    f.write(cards_html)

with open(r'C:\Users\maste\.openclaw\workspace\form_options.txt', 'w', encoding='utf-8') as f:
    f.write(form_options)

print('Done')
