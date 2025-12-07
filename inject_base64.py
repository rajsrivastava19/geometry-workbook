import base64
import os

# Paths
html_path = 'index.html'
icon_path = 'icon.png'
header_img_path = 'ishaan.png'

# Read HTML
with open(html_path, 'r') as f:
    html_content = f.read()

# Read and encode Icon
with open(icon_path, 'rb') as f:
    icon_b64 = base64.b64encode(f.read()).decode('utf-8')
    icon_data_uri = f"data:image/png;base64,{icon_b64}"

# Read and encode Header Image
with open(header_img_path, 'rb') as f:
    header_b64 = base64.b64encode(f.read()).decode('utf-8')
    header_data_uri = f"data:image/png;base64,{header_b64}"

# Replace placeholders
html_content = html_content.replace('__ICON_BASE64__', icon_data_uri)
html_content = html_content.replace('__HEADER_IMG_BASE64__', header_data_uri)

# Write back to HTML
with open(html_path, 'w') as f:
    f.write(html_content)

print("Successfully injected Base64 images into index.html")
