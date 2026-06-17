import qrcode
from PIL import Image, ImageDraw

# ===============================
# CONFIGURATION
# ===============================
# ===============================
# WhatsApp CONFIGURATION
# Format: Use country code + phone number without any spaces, '+', or dashes.
# Example for South Africa (+27): "https://wa.me/27XXXXXXXXX"
#Prefil message 
#Example data = "https://wa.me/27XXXXXXXXX?text=Hey!%20Just%20scanning%20in%20from%20the%20shop,%20ready%20to%20send%20through%20my%20feedback."
data = "https://wa.me/27XXXXXXXXX?text=Hey!%20Just%20scanning%20in%20from%20the%20shop,%20ready%20to%20send%20through%20my%20feedback."
logo_path = "barblogo_400x400.jpg"
output_file = "styled_qr_black_gold.png"

# ===============================
# GENERATE QR MATRIX
# ===============================
qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)
matrix = qr.get_matrix()
size = len(matrix)
box = 10
img_size = (size + qr.border*2) * box

# White background
img = Image.new("RGB", (img_size, img_size), "white")
draw = ImageDraw.Draw(img)

# ===============================
# COLOR DEFINITIONS
# ===============================
black = (0, 0, 0)
gold = (212, 175, 55)

""" # ===============================
# DRAW QR MODULES (BLACK GOLD GRADIENT)
# ===============================
for y, row in enumerate(matrix):
    for x, cell in enumerate(row):
        if cell:
            # Gradient ratio (top: black, bottom: gold)
            ratio = y / size
            r = int(black[0] * (1 - ratio) + gold[0] * ratio)
            g = int(black[1] * (1 - ratio) + gold[1] * ratio)
            b = int(black[2] * (1 - ratio) + gold[2] * ratio)
            color = (r, g, b)

            # Draw rounded dots
            x1 = (x + qr.border) * box
            y1 = (y + qr.border) * box
            draw.ellipse([x1, y1, x1+box, y1+box], fill=color)

# ===============================
# STYLE QR "EYES" (POSITION MARKERS)
# ===============================
eye_size = 7  # Eye modules are 7x7 in QR spec
eye_positions = [(0, 0), (size-eye_size, 0), (0, size-eye_size)]

for ex, ey in eye_positions:
    x0 = (ex + qr.border)*box
    y0 = (ey + qr.border)*box
    w = eye_size * box

    # Outer eye (gold)
    draw.rectangle([x0, y0, x0+w, y0+w], fill=gold)

    # Inner eye (white space for contrast)
    inner = box * 3
    offset = (w - inner) // 2
    draw.rectangle([x0+offset, y0+offset, x0+offset+inner, y0+offset+inner], fill="white")

    # Central dot (black)
    dot = box * 1.5
    dot_offset = (w - dot) // 2
    draw.ellipse([x0+dot_offset, y0+dot_offset, x0+dot_offset+dot, y0+dot_offset+dot], fill=black)
 """

# ===============================
# DRAW QR MODULES (SOLID BLACK)
# ===============================
for y, row in enumerate(matrix):
    for x, cell in enumerate(row):
        if cell:
            # Solid black for all dots
            color = black

            # Draw rounded dots
            x1 = (x + qr.border) * box
            y1 = (y + qr.border) * box
            draw.ellipse([x1, y1, x1+box, y1+box], fill=color)

# ===============================
# STYLE QR "EYES" (POSITION MARKERS)
# ===============================
eye_size = 7  
eye_positions = [(0, 0), (size-eye_size, 0), (0, size-eye_size)]

for ex, ey in eye_positions:
    x0 = (ex + qr.border)*box
    y0 = (ey + qr.border)*box
    w = eye_size * box

    # Outer eye (Solid Black)
    draw.rectangle([x0, y0, x0+w, y0+w], fill=black)

    # Inner eye (white space for contrast)
    inner = box * 3
    offset = (w - inner) // 2
    draw.rectangle([x0+offset, y0+offset, x0+offset+inner, y0+offset+inner], fill="white")

    # Central dot (Solid Black)
    dot = box * 1.5
    dot_offset = (w - dot) // 2
    draw.ellipse([x0+dot_offset, y0+dot_offset, x0+dot_offset+dot, y0+dot_offset+dot], fill=black)

# ===============================
# ADD CENTER LOGO
# ===============================
if logo_path:
    logo = Image.open(logo_path).convert("RGBA")
    max_logo_size = img_size // 5  # Made slightly larger so it looks crisp
    logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

    # Changed mask to a solid black square to match your barber logo background perfectly
    mask_size = (logo.width + 10, logo.height + 10)
    mask_img = Image.new("RGBA", mask_size, (0, 0, 0, 255)) 

    # Paste black mask, then logo
    pos = ((img_size - mask_size[0]) // 2, (img_size - mask_size[1]) // 2)
    img.paste(mask_img, pos)

    logo_pos = ((img_size - logo.width) // 2, (img_size - logo.height) // 2)
    img.paste(logo, logo_pos, mask=logo)

# ===============================
# ADD CENTER LOGO
# ===============================
if logo_path:
    logo = Image.open(logo_path).convert("RGBA")
    max_logo_size = img_size // 6  # Keep small for scannability
    logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

    # Add a white circle mask behind logo for clarity
    mask_size = (logo.width + 20, logo.height + 20)
    mask_img = Image.new("RGBA", mask_size, (255, 255, 255, 255))
    mask_draw = ImageDraw.Draw(mask_img)
    mask_draw.ellipse([0, 0, mask_size[0], mask_size[1]], fill=(255, 255, 255, 255))

    # Paste white circle mask, then logo
    pos = ((img_size - mask_size[0]) // 2, (img_size - mask_size[1]) // 2)
    img.paste(mask_img, pos, mask=mask_img)

    logo_pos = ((img_size - logo.width) // 2, (img_size - logo.height) // 2)
    img.paste(logo, logo_pos, mask=logo)

# ===============================
# SAVE FINAL QR
# ===============================
img.save(output_file)
print(f"✅ Black-to-gold QR with logo saved as: {output_file}")
