import sys
from PIL import Image, ImageDraw, ImageFont

img_name = "" # Image name

scale = 1 # Image scale
sample = 64 # Skip pixels
font_size = 40 # Font size
shift = 2 # Move characters to right

colored = False # Colored or Mono
extended_range = False # Extended ASCII characters
reverce_basic_colors = False # Set background black and characters white (useful with mono images)

# Read args
for x in range(len(sys.argv)):
    arg = sys.argv[x]
    if arg == "-help":
        print("Usage: <scale> <sample> <font size> <shift>")
        print("-c   Colored version\n")
        print("-e   Extended ASCII characters\n")
        print("-r   Set background white and characters white (useful with mono images)\n")
        print("More info: https://github.com/Sekyzio/Photo-Ascii/README.md\n")
        exit()

    elif arg == "-c":
        colored = True
    elif arg == "-e":
        extended_range = True
    elif arg == "-r":
        reverce_basic_colors = True

    if x == 1:
        img_name = sys.argv[x]
    elif x == 2:
        scale = float(sys.argv[x])
    elif x == 3:
        sample = int(sys.argv[x])
    elif x == 4:
        font_size = int(sys.argv[x])
    elif x == 5:
        shift = int(sys.argv[x])

if len(sys.argv) < 5:
    print("Too few arguments")
    exit()

fnt = ImageFont.truetype("/usr/share/fonts/truetype/malayalam/AnjaliOldLipi-Regular.ttf", font_size) # Font type
img = Image.open(img_name) #Load img

size = img.size # Image size
data = [] # Pixel position and color
move_right = 0 # Shift value

# Get values for every pixel
for y in range(size[1]):
    for x in range(size[0]):
        if move_right == sample:
            color = img.getpixel((x,y))
            data.append(((x, y), color))
            move_right = 0

        move_right+=1

    if move_right == 0:
        move_right += shift
    else:
        move_right -= shift


if reverce_basic_colors:
    bg_color = (255, 255, 255, 0) # Background color
    ch_color = (0, 0, 0, 0) # Character color
else:
    bg_color = (0, 0, 0, 0)
    ch_color = (255, 255, 255, 255)

# Create new img
new_img = Image.new('RGB', (int(size[0]*scale), int(size[1]*scale)), bg_color)
d = ImageDraw.Draw(new_img)
for i in range(len(data)):
    values = data[i]
    x, y = values[0]
    colors = values[1]
    color_avg = (colors[0] + colors[1] + colors[2])//3


    if color_avg <= 33: # Values lower than 33 are not printable
        color_avg = 33

    if extended_range:
        if color_avg >= 255:
            color_avg = 254
    else:
        if color_avg >= 126:
            color_avg = 126

    if colored: # Colored or Mono
        d.text((x*scale,y*scale), chr(color_avg), font=fnt, fill=(colors[0], colors[1], colors[2], 255))
    else:
        d.text((x*scale,y*scale), chr(color_avg), font=fnt, fill=(ch_color))

# Save new img
new_img.save("output.png")