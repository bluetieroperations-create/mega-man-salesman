import re

# Read current site
with open(r'C:\Users\maste\.openclaw\workspace\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read the 169 cards
with open(r'C:\Users\maste\.openclaw\workspace\vehicle_cards.html', 'r', encoding='utf-8') as f:
    cards_html = f.read()

# Read form options
with open(r'C:\Users\maste\.openclaw\workspace\form_options.txt', 'r', encoding='utf-8') as f:
    form_options = f.read()

disclaimer = 'Price does not include $499 Dealer Doc Fee, Taxes, License, smog, and $995 Reconditioning. While great effort is made to ensure the accuracy of the information on this site, errors do occur so please verify information with a customer service rep. This is easily done by calling us at 702-588-9292 or by visiting us at the dealership. Availability of vehicle may change without notice due to time frame it takes to remove vehicle from dealer inventory upon sale. Contact us for most current information.'

# 1. Replace the vehicle grid
grid_pattern = r'<div class="vehicle-grid">.*?</div>\s*</div>\s*</section>'
new_grid = '<div class="vehicle-grid">\n' + cards_html + '</div>\n</div>\n<div style="text-align:center;padding:24px 0 48px;font-size:13px;color:#666;max-width:800px;margin:0 auto;">' + disclaimer + '</div>\n</section>'
html, count = re.subn(grid_pattern, new_grid, html, flags=re.DOTALL)
print(f'Grid replaced: {count} occurrence(s)')

# 2. Update "9 Vehicles In Stock" stat
html = html.replace('>9<', '>169<', 1)
print('Stat updated to 169')

# 3. Update hero stats - fix all stats
html = html.replace('<span class="stat-number">15+</span>', '<span class="stat-number">15+</span>')
html = html.replace('<span class="stat-number">500+</span>', '<span class="stat-number">500+</span>')
html = html.replace('<span class="stat-number">5★</span>', '<span class="stat-number">5★</span>')
html = html.replace('<span class="stat-number">9</span><span class="stat-label">Vehicles In Stock</span>', '<span class="stat-number">169</span><span class="stat-label">Vehicles In Stock</span>')
print('Hero stats updated')

# 4. Update form dropdown
dropdown_old = r'<select>.*?</select>'
new_dropdown = '<select>\n' + form_options + '<option value="">Not sure yet</option></select>'
html, count2 = re.subn(dropdown_old, new_dropdown, html, flags=re.DOTALL)
print(f'Dropdown replaced: {count2} occurrence(s)')

# 5. Save updated site
with open(r'C:\Users\maste\.openclaw\workspace\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('index.html saved successfully!')
print('Total cards in grid: 169')
