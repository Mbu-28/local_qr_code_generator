import sys
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

whatsapp_url = "https://wa.me/27XXXXXXXXX?text=Hey!%20Just%20scanning%20in%20from%20the%20shop,%20ready%20to%20send%20through%20my%20feedback."
instagram_url = "https://instagram.com/your_handle"
logo_path = "barblogo_400x400.jpg"

# Read platform from command line argument (Defaults to 'whatsapp' if empty)
platform = sys.argv[1].lower() if len(sys.argv) > 1 else "whatsapp"

if platform == "whatsapp":
    data = whatsapp_url
    output_file = "qr_whatsapp_black.png"
    print("🖤 Selected: WhatsApp (Solid Black Style)")
elif platform == "instagram":
    data = instagram_url
    output_file = "qr_instagram_gradient.png"
    print("🎨 Selected: Instagram (Black & Gold Gradient Style)")
else:
    print(f"❌ Unknown platform '{platform}'. Please use 'whatsapp' or 'instagram'.")
    sys.exit(1)

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

# White canvas
img = Image.new("RGB", (img_size, img_size), "white")
draw = ImageDraw.Draw(img)

# Color palettes
black = (0, 0, 0)
gold = (212, 175, 55)

# ===============================
# DRAW QR MODULES
# ===============================
for y, row in enumerate(matrix):
    for x, cell in enumerate(row):
        if cell:
            if platform == "instagram":
                # Elegant curved gradient for Instagram (Fades smoothly to gold at the bottom)
                linear_ratio = y / size
                ratio = linear_ratio ** 2 
                r = int(black[0] * (1 - ratio) + gold[0] * ratio)
                g = int(black[1] * (1 - ratio) + gold[1] * ratio)
                b = int(black[2] * (1 - ratio) + gold[2] * ratio)
                color = (r, g, b)
            else:
                # Timeless solid black for WhatsApp
                color = black

            # Draw modules as rounded dots
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

    # Outer Frame (Always solid black to keep it looking clean and premium)
    draw.rectangle([x0, y0, x0+w, y0+w], fill=black)

    # Inner Frame Spacer (White gap)
    inner = box * 3
    offset = (w - inner) // 2
    draw.rectangle([x0+offset, y0+offset, x0+offset+inner, y0+offset+inner], fill="white")

    # Center Target Dot (Gold accent for Instagram, solid Black for WhatsApp)
    center_color = gold if platform == "instagram" else black
    dot = box * 1.5
    dot_offset = (w - dot) // 2
    draw.ellipse([x0+dot_offset, y0+dot_offset, x0+dot_offset+dot, y0+dot_offset+dot], fill=center_color)

# ===============================
# ADD CENTER LOGO WITH TARGET BORDER
# ===============================
if logo_path:
    logo = Image.open(logo_path).convert("RGBA")
    
    # Scale down logo to perfectly clear space inside the QR code
    max_logo_size = img_size // 5  
    logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

    # Calculate multi-layered borders to replicate your reference image frame
    black_border_thickness = 4
    white_border_thickness = 12
    
    # Outer frame layer dimensions
    outer_frame_size = (
        logo.width + (white_border_thickness * 2) + (black_border_thickness * 2),
        logo.height + (white_border_thickness * 2) + (black_border_thickness * 2)
    )
    
    # Inner white backdrop layer dimensions
    white_bg_size = (
        logo.width + (white_border_thickness * 2),
        logo.height + (white_border_thickness * 2)
    )

    # 1. Draw the absolute outermost black framing outline square
    outer_mask = Image.new("RGBA", outer_frame_size, (0, 0, 0, 255))
    outer_pos = ((img_size - outer_frame_size[0]) // 2, (img_size - outer_frame_size[1]) // 2)
    img.paste(outer_mask, outer_pos)

    # 2. Draw the clean white inner padding border over it
    white_mask = Image.new("RGBA", white_bg_size, (255, 255, 255, 255))
    white_pos = ((img_size - white_bg_size[0]) // 2, (img_size - white_bg_size[1]) // 2)
    img.paste(white_mask, white_pos)

    # 3. Draw the center black block that matches your barber logo image background
    logo_bg_mask = Image.new("RGBA", (logo.width, logo.height), (0, 0, 0, 255))
    logo_bg_pos = ((img_size - logo.width) // 2, (img_size - logo.height) // 2)
    img.paste(logo_bg_mask, logo_bg_pos)

    # 4. Paste the actual barber shop branding image dead center
    img.paste(logo, logo_bg_pos, mask=logo)

# ===============================
# SAVE FINAL QR
# ===============================
img.save(output_file)
print(f"✅ Production asset created successfully: {output_file}\n")