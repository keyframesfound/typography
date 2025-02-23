import os
from PIL import Image, ImageDraw, ImageFont
import sys

# User inputs
target_word = input("Enter target word: ")
pattern_word = input("Enter pattern word: ")
try:
    target_size = int(input("Enter target word size (200-2000): "))
    pattern_size = int(input("Enter pattern word size (12-50): "))
except ValueError:
    print("Please enter valid numbers")
    sys.exit(1)

# Create an 8K resolution image
img_size = (7680, 4320)  # 8K resolution
final_img = Image.new("RGB", img_size, "white")
mask_img = Image.new("L", img_size, "white")

# Update font paths to tech/computer style fonts
font_paths = [
    "/System/Library/Fonts/Monaco.ttf",  # macOS
    "/System/Library/Fonts/Menlo.ttf",  # macOS alternative
    "/System/Library/Fonts/Courier New.ttf",  # macOS/Windows
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",  # Linux
    "C:/Windows/Fonts/consola.ttf",  # Windows Consolas
    "C:/Windows/Fonts/lucon.ttf",  # Windows Lucida Console
]

# Try to load a font
big_font = None
small_font = None
for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            big_font = ImageFont.truetype(font_path, target_size)
            small_font = ImageFont.truetype(font_path, pattern_size)
            break
        except IOError:
            continue

# Add fallback monospace hint if no fonts found
if big_font is None or small_font is None:
    print("Attempting to load system monospace font...")
    try:
        from PIL.ImageFont import load_default
        big_font = ImageFont.truetype("monospace", target_size)
        small_font = ImageFont.truetype("monospace", pattern_size)
    except:
        print("Using default font as fallback.")
        big_font = small_font = ImageFont.load_default()

# Draw target word on mask
mask_draw = ImageDraw.Draw(mask_img)
bbox = big_font.getbbox(target_word)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
position = ((img_size[0]-text_width)//2, (img_size[1]-text_height)//2)
mask_draw.text(position, target_word, fill="black", font=big_font)

# Fill target shape with pattern word
draw = ImageDraw.Draw(final_img)
bbox_small = small_font.getbbox(pattern_word)
small_w = bbox_small[2] - bbox_small[0]
small_h = bbox_small[3] - bbox_small[1]

# Increase padding for higher resolution
word_padding_x = int(small_w * 0.4)  # Slightly larger padding for higher res
word_padding_y = int(small_h * 0.4)

# Adjust step size with padding
step_x = small_w + word_padding_x
step_y = small_h + word_padding_y

for y in range(0, img_size[1], step_y):
    for x in range(0, img_size[0], step_x):
        px = min(x + small_w//2, img_size[0]-1)
        py = min(y + small_h//2, img_size[1]-1)
        if mask_img.getpixel((px, py)) < 128:
            draw.text((x, y), pattern_word, fill="black", font=small_font)

# Crop the image to remove extra white space
bbox = final_img.getbbox()
if bbox:
    final_img = final_img.crop(bbox)

# Save with ultra-high quality settings
final_img_with_padding = Image.new("RGB", (final_img.width + 200, final_img.height + 200), "white")
final_img_with_padding.paste(final_img, (100, 100))
final_img_with_padding.save("output.png", dpi=(1200, 1200), quality=100)
print("Ultra high resolution PNG image saved as output.png (8K)")
