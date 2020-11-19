import sys
from PIL import Image, ImageDraw, ImageFont

img_name = "" # Image name

scale = 4 # Image scale
probe = 8 # Skip pixels
shift = 4 # Move line to right
font_size = 12 # Font size

colored = True # Colored or Mono
extended_range = False # User non typicall letters

# Read args
for x in range(len(sys.argv)):
    if sys.argv[x] == "-help":
        print("Usage: <scale> <probe> <font size> <shift> <colored> <extended range>")
        exit()

    if x == 1:
        img_name = sys.argv[x]
    elif x == 2:
        scale = float(sys.argv[x])
    elif x == 3:
        probe = int(sys.argv[x])
    elif x == 4:
        font_size = int(sys.argv[x])
    elif x == 5:
        shift = int(sys.argv[x])
    elif x == 6:
        if sys.argv[x] == "true":
            colored = True
        elif sys.argv[x] == "false":
            colored = False
    elif x == 7:
        if sys.argv[x] == "true":
            extended_range = True
        elif sys.argv[x] == "false":
            extended_range = False


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
        if move_right == probe:
            color = img.getpixel((x,y))
            data.append(((x, y), color))
            move_right = 0

        move_right+=1

    if move_right == 0:
        move_right += shift
    else:
        move_right -= shift

# Create new img
new_img = Image.new('RGB', (int(size[0]*scale), int(size[1]*scale)), (0,0,0,0))
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
        d.text((x*scale,y*scale), chr(color_avg), font=fnt, fill=(colors[0], colors[1], colors[2],255))
    else:
        d.text((x*scale,y*scale), chr(color_avg), font=fnt, fill=(255, 255, 255, 255))

# Save new img
new_img.save("output.png")