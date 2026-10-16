import tkinter as tk
import tkinter.font as tkfont
import math
import random

# SETTINGS

WIDTH = 1100
HEIGHT = 850

BACKGROUND = "#08040A"
TEXT_COLOR = "#FF244F"
GLOW_COLOR = "#70001C"
TITLE_COLOR = "#FF5C83"

PHRASES = [
    "I love you", "Te amo", "Je t'aime",
    "Ich liebe dich", "Ti amo", "Eu te amo",
    "Ik hou van jou", "Seni seviyorum",
    "Kocham cię", "Te iubesc", "Volim te",
    "मैं तुमसे प्यार करता हूँ",
    "હું તને પ્રેમ કરું છું",
    "माझं तुझ्यावर प्रेम आहे",
    "愛してる", "大好きです",
    "사랑해", "사랑해요",
    "我爱你", "我喜歡你",
    "Anh yêu em", "Mahal kita",
    "Aku cinta kamu", "ฉันรักคุณ",
    "أحبك", "أحبك كثيرًا",
    "دوستت دارم", "אני אוהב אותך",
    "Nakupenda", "Ngiyakuthanda",
    "Mo nifẹ rẹ", "Mi amas vin",
    "Σε αγαπώ", "Я тебя люблю",
    "Я кохаю тебе", "Aloha wau iā ʻoe"
]

random.seed(12)

# ==========================================
# WINDOW
# ==========================================
root = tk.Tk()
root.title("Multilingual Love Heart ❤️")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.minsize(750, 650)
root.configure(bg=BACKGROUND)

canvas = tk.Canvas(
    root,
    bg=BACKGROUND,
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

font = tkfont.Font(
    family="Nirmala UI",
    size=9,
    weight="bold"
)

title_font = ("Segoe UI", 19, "bold")

animated_text = []
resize_job = None
animation_started = False

# CREATE A MATHEMATICAL HEART OUTLINE
def heart_outline():
    points = []

    # Parametric heart equation
    for i in range(1200):
        t = 2 * math.pi * i / 1200

        x = 16 * math.sin(t) ** 3

        y = (
            13 * math.cos(t)
            - 5 * math.cos(2 * t)
            - 2 * math.cos(3 * t)
            - math.cos(4 * t)
        )

        points.append((x / 17, y / 17))

    return points


HEART = heart_outline()


# FIND HEART BOUNDARIES FOR EACH ROW
def get_intervals(y):
    intersections = []

    for i in range(len(HEART)):
        x1, y1 = HEART[i]
        x2, y2 = HEART[(i + 1) % len(HEART)]

        # Find where this outline edge crosses the row.
        if (y1 <= y < y2) or (y2 <= y < y1):
            x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            intersections.append(x)

    intersections.sort()

    # Pair intersections to preserve the heart's top notch.
    intervals = []

    for i in range(0, len(intersections) - 1, 2):
        intervals.append(
            (intersections[i], intersections[i + 1])
        )

    return intervals


# DRAW THE HEART
def draw_heart():
    global animated_text

    canvas.delete("all")
    animated_text = []

    canvas.update_idletasks()

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    center_x = width / 2
    center_y = height / 2 + 35

    # Make the heart use more of the available window.
    scale = min(width * 0.43, height * 0.43)

    canvas.create_text(
        center_x,
        38,
        text="MULTILINGUAL LOVE",
        font=title_font,
        fill=TITLE_COLOR
    )

    # Determine the top and bottom of the outline.
    max_y = max(y for x, y in HEART)
    min_y = min(y for x, y in HEART)

    # Smaller row spacing gives a denser heart.
    row_step = 0.040
    row = max_y - 0.008

    phrase_index = random.randrange(len(PHRASES))

    while row > min_y:
        intervals = get_intervals(row)

        screen_y = center_y - row * scale

        for left, right in intervals:
            left_px = center_x + left * scale
            right_px = center_x + right * scale

            x = left_px + 2

            # Continue until this section is filled.
            attempts = 0

            while x < right_px - 2 and attempts < len(PHRASES):
                phrase = PHRASES[phrase_index % len(PHRASES)]
                phrase_index += 1
                attempts += 1

                text_width = font.measure(phrase)

                # Try another phrase if this one is too wide.
                if x + text_width > right_px:
                    continue

                text_x = x + text_width / 2
                phase = random.uniform(0, 2 * math.pi)

                shadow_id = canvas.create_text(
                    text_x + 1,
                    screen_y + 1,
                    text=phrase,
                    font=font,
                    fill=GLOW_COLOR
                )

                text_id = canvas.create_text(
                    text_x,
                    screen_y,
                    text=phrase,
                    font=font,
                    fill=TEXT_COLOR
                )

                animated_text.append({
                    "id": text_id,
                    "shadow": shadow_id,
                    "x": text_x,
                    "y": screen_y,
                    "phase": phase
                })

                x += text_width + 4

        row -= row_step


# SHIMMER + FLOATING EFFECT
def animate():
    time_now = root.tk.call("clock", "milliseconds")
    time_now = int(time_now)

    for item in animated_text:
        phase = item["phase"]

        brightness = (
            math.sin(time_now / 650 + phase) + 1
        ) / 2

        red = 205 + int(50 * brightness)
        green = 5 + int(25 * brightness)
        blue = 25 + int(55 * brightness)

        color = f"#{red:02x}{green:02x}{blue:02x}"

        offset = math.sin(
            time_now / 900 + phase
        ) * 1.2

        canvas.itemconfigure(
            item["id"],
            fill=color
        )

        canvas.coords(
            item["id"],
            item["x"],
            item["y"] + offset
        )

        canvas.coords(
            item["shadow"],
            item["x"] + 1,
            item["y"] + offset + 1
        )

    root.after(40, animate)


# HANDLE WINDOW RESIZING
def on_resize(event):
    global resize_job

    if event.widget != canvas:
        return

    if resize_job is not None:
        root.after_cancel(resize_job)

    resize_job = root.after(250, redraw)


def redraw():
    global resize_job
    resize_job = None
    draw_heart()


# START
canvas.bind("<Configure>", on_resize)

draw_heart()
animate()

root.mainloop()
