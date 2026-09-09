from PIL import Image

def mostCommonUsedColour(image):
    imageWidth, imageHeight = image.size

    redTotal = 0
    greenTotal = 0
    blueTotal = 0
    alphaTotal = 0

    count = 0

    for x in range(0, imageWidth):
        for y in range(0, imageHeight):
            red, green, blue, alpha = image.getpixel((x, y))

            if alpha == 0:
                continue
            else:

                redTotal += red
                greenTotal += green
                blueTotal += blue
                alphaTotal += alpha
                count += 1

    return (redTotal/count, greenTotal/count, blueTotal/count, alphaTotal/count)

image = Image.open(r'/home/adam/Pokemon_Images/Adams_Tests/HQ_Spare_Images/0655_Delphox.png')

image = image.convert('RGBA')

commonColour = mostCommonUsedColour(image)

redCommon = commonColour[0]
greenCommon = commonColour[1]
blueCommon = commonColour[2]
alphaCommon = commonColour[3]

print(hex(int(redCommon)))
print(hex(int(greenCommon)))
print(hex(int(blueCommon)))
print(hex(int(alphaCommon)))
