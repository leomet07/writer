import cv2
import os
import numpy as np
from PIL import Image

print("Writing...")

height = 2480
width = 3508
# canvas = np.zeros((height, width, 3), np.uint8)
# canvas.fill(255)
canvas = cv2.imread("paper.jpg")
canvas = cv2.resize(canvas, (630, 800))

canvas_h, canvas_w, _ = canvas.shape


def get_raw_file_name(file):
    before_the_ext = file.index(".")

    name = file[:before_the_ext]

    return name


def generate_char_map(dir):
    print("Char map of dir " + str(dir) + ": ")

    char_map = {}
    if os.path.exists(dir):
        for r, d, f in os.walk(dir):
            for file in f:

                file_path = os.path.join(dir, file)
                print("file path: " + str(file_path))

                file_name = get_raw_file_name(file)
                print("file name: " + str(file_name))

                print("")

                texture = cv2.imread(file_path)
                w = round(30)
                h = round(1.27 * w)
                texture = cv2.resize(texture, (h, w))

                # make sure it has alpha channel

                char_map[file_name] = texture
    print("\n-------------------")
    return char_map


"""
a_img = cv2.imread("a.jpg")
a_img = cv2.resize(a_img, (500, 150))

b_img = cv2.imread("b.png")
b_img = cv2.resize(b_img, (500, 150))
"""
characters = generate_char_map("letters")

string = "bacbabbbbbbbb"


collumn = 0
row = 0


for index in range(len(string)):
    char = string[index]

    try:
        texture = characters[char]
        texture_h, texture_w, _ = texture.shape

        image_h, image_w, image_c = texture.shape

        x_starting = 110
        x_spacing = 10
        x_indent = 50

        y_starting = 120
        y_spacing = 10

        print((image_w + x_spacing) * (collumn + 1) + x_starting)
        if (image_w + x_spacing) * (collumn + 1) + x_starting >= canvas_w:
            print("Goes over")
            collumn = 0
            row += 1

        x_offset = (image_w + x_spacing) * (collumn) + x_starting
        y_offset = (row) * (y_spacing + image_h) + y_starting

        if (index == 0):
            x_offset += x_indent

        canvas[
            y_offset : y_offset + texture.shape[0],
            x_offset : x_offset + texture.shape[1],
        ] = texture

        collumn += 1
    except KeyError:
        print("Letter " + char + " doesn't exist")


def display_paper(canvas, dim):
    # resize img to display
    resized_img = cv2.resize(canvas, dim, interpolation=cv2.INTER_AREA)
    # make canvas white

    cv2.imshow("window", resized_img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


display_paper(canvas, (620, 877))

print(canvas.shape)

# convert to pdf
img = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
canvas_pil = Image.fromarray(img)


print(canvas_pil.size[::-1])
canvas_pil.save("print.pdf")
