from PIL import Image
import os

# Create white canvas
canvas = Image.new("RGB", (1200, 800), "white")

# Symbol positions
components = [
    ("battery.png", (100,100)),
    ("capacitor.png", (300,100)),
    ("diode.png", (500,100)),
    ("ground.png", (700,100)),
    ("inductor.png", (100,300)),
    ("led.png", (300,300)),
    ("resistor.png", (500,300))
]

for filename, position in components:

    img = Image.open("symbols/" + filename)

    img = img.resize((100,100))

    canvas.paste(img, position)

os.makedirs("output", exist_ok=True)

canvas.save("output/generated_schematic.png")

print("Generated Successfully!")
