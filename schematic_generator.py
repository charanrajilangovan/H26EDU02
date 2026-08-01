import cv2
import json
import os
import numpy as np


def generate_schematic(layout):
    """
    Generate a clean digital schematic from layout.
    """

    WIDTH = 1400
    HEIGHT = 900

    canvas = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

    positions = []

    # -----------------------------
    # Draw Components
    # -----------------------------
    for comp in layout:

        x = int(comp["layout_x"])
        y = int(comp["layout_y"])

        name = comp["name"]

        symbol_path = os.path.join(
            "symbols",
            name + ".png"
        )

        if os.path.exists(symbol_path):

            symbol = cv2.imread(symbol_path)

            symbol = cv2.resize(symbol, (80,80))

            h, w = symbol.shape[:2]

            x1 = max(0, x - w // 2)
            y1 = max(0, y - h // 2)

            canvas[y1:y1+h, x1:x1+w] = symbol

        else:

            cv2.circle(
                canvas,
                (x,y),
                10,
                (0,0,255),
                -1
            )

            cv2.putText(
                canvas,
                name,
                (x+20,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,0,0),
                2
            )

        positions.append((x,y))

    # -----------------------------
    # Draw Wires
    # -----------------------------
    for i in range(len(positions)-1):

        x1,y1 = positions[i]
        x2,y2 = positions[i+1]

        cv2.line(
            canvas,
            (x1,y1),
            (x2,y2),
            (0,0,0),
            2
        )

    # -----------------------------
    # Save
    # -----------------------------
    os.makedirs("output", exist_ok=True)

    cv2.imwrite(
        "output/final_schematic.png",
        canvas
    )

    return canvas


# ---------------------------------
# Test
# ---------------------------------

if __name__ == "__main__":

    with open("output/layout.json") as f:

        layout = json.load(f)

    generate_schematic(layout)

    print("Schematic Generated Successfully!")
