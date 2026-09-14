from PIL import Image, ImageChops

width = 1366
height = 768

def mostCommonUsedColour(imageInv):
    imageWidth, imageHeight = imageInv.size

    redTotal = 0
    greenTotal = 0
    blueTotal = 0
    alphaTotal = 0

    count = 0

    for x in range(0, imageWidth):
        for y in range(0, imageHeight):
            red, green, blue, alpha = imageInv.getpixel((x, y))

            if alpha == 0:
                continue
            else:

                redTotal += red
                greenTotal += green
                blueTotal += blue
                alphaTotal += alpha
                count += 1

    return (redTotal/count, greenTotal/count, blueTotal/count, alphaTotal/count)

image = Image.open('/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/0655_Delphox-Mega.png')
# image = Image.open('/home/mark/Adams_Dev_Test/test.png')
# image = Image.open(r'/home/adam/Pokemon_Images/Adams_Tests/HQ_Spare_Images/0655_Delphox.png')

image = image.convert('RGBA')

# imageInv = ImageChops.invert(image)

commonColour = mostCommonUsedColour(image)

redCommon = commonColour[0]
greenCommon = commonColour[1]
blueCommon = commonColour[2]
alphaCommon = commonColour[3]

print(hex(int(redCommon)))
print(hex(int(greenCommon)))
print(hex(int(blueCommon)))
print(hex(int(alphaCommon)))

img = Image.new(mode = "RGB", size = (width, height), color = (int(redCommon), int(greenCommon), int(blueCommon)))
img.show()
