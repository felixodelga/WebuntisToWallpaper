from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

color_bg_standart = (60, 42, 120)
color_bg_cancelled = (50, 50, 50)
color_bg_irregular = (230, 10, 10)

color_text_standart = (255, 255, 255)
color_text_cancelled = (255, 255, 255)
color_text_irregular = (20, 20, 20)


# Format *original* : *replacement*
replace = {
    "E1": "E",
    "LUK": "BSP",
}

# highlight bg
hf = ["F", "D", "M", "DG", "E"]
hf_col = (100, 20, 130)

pk_col = (54, 80, 112)

# highlight fg
colors = {
    "D": (11, 200,  53),
    "M": (214,  10,  48),
    "F": (220,  37, 221),
    "E": (24,  63, 221),
    "DG": (239, 211,  26),
}


# exclude these
blacklist = ["RK", "LAT6", "RU", "BE", "LUM",
             "DELF", "SPA+", "LAT+", "MU+", "CC"]


def pasteBoxWithText(imTo, position, text, imFrom, color, textsize):
    font = ImageFont.truetype("Roboto-Regular.ttf", textsize)

    draw = ImageDraw.Draw(imFrom)

    W, H = imFrom.size
    w, h = draw.textsize(text, font=font)

    draw.text(((W-w)/2, (H-h)/2), text, color, font=font)
    del draw
    imTo.paste(imFrom, position)

    return imTo


def drawTimetable(timetable, img, box):  # box: top/left/bottom/right

    # loop over all lessons and apply filters
    for i in range(2):
        for lessons in timetable:
            for lesson in lessons:
                if lesson in blacklist:
                    lessons.remove(lesson)

                if lesson in replace:
                    lessons.remove(lesson)
                    lessons.append(replace[lesson])

                if lesson.startswith("++") or lesson.startswith("--"):
                    if lesson[2:] in blacklist:
                        lessons.remove(lesson)

    w = box[3]-box[1]
    h = box[2]-box[0]

    for i in range(len(timetable)):
        l = len(timetable[i])

        if l == 0:
            continue

        for j in range(len(timetable[i])):

            color = color_text_standart if timetable[i][j] not in colors else colors[timetable[i][j]]

            bg_color = color_bg_standart

            # Highlight 1
            if timetable[i][j] in hf:
                bg_color = hf_col

            # Highlight 2
            if timetable[i][j].endswith("+"):
                bg_color = pk_col

            # cancelled
            if (timetable[i][j].startswith("--")):
                timetable[i][j] = timetable[i][j][2:]
                color = color_text_cancelled
                bg_color = color_bg_cancelled

            # irregular
            if (timetable[i][j].startswith("++")):
                timetable[i][j] = timetable[i][j][2:]
                color = color_text_irregular
                bg_color = color_bg_irregular
                
            pasteBoxWithText(img,
                             (box[1] + int(w/l) * j, box[0]+i*int(h/10)),
                             timetable[i][j],
                             Image.new("RGB", (int(w/l), int(h/10)), bg_color),
                             color,
                             abs(int(h/12)))


#(1920-450*(2-col) + int(450/l) * j, 20+i*100)

#Image.new("RGB", (int(450/l), 100), bg_color)
