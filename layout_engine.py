import json
import os
import cv2
import numpy as np


def generate_layout(components):
    """
    Generate a clean layout for detected components.

    Parameters:
        components (list)

    Returns:
        layout (list)
    """

    WIDTH = 1400
    HEIGHT = 900

    canvas = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

    battery_x = 150
    battery_y = 450

    resistor_x = 500
    resistor_gap = 220

    meter_x = 1150
    meter_y = 300

    ground_x = 700
    ground_y = 720

    resistor_count = 0

    layout = []

    for comp in components:

        name = comp["name"].lower()

        new_comp = comp.copy()

        # -------------------------
        # Battery
        # -------------------------
        if "battery" in name:

            new_comp["layout_x"] = battery_x
            new_comp["layout_y"] = battery_y

        # -------------------------
        # Resistor
        # -------------------------
        elif "resistor" in name:

            new_comp["layout_x"] = resistor_x + resistor_count * resistor_gap
            new_comp["layout_y"] = 450

            resistor_count += 1

        # -------------------------
        # Capacitor
        # -------------------------
        elif "capacitor" in name:

            new_comp["layout_x"] = resistor_x + resistor_count * resistor_gap
            new_comp["layout_y"] = 250

        # -------------------------
        # Inductor
        # -------------------------
        elif "inductor" in name:

            new_comp["layout_x"] = resistor_x + resistor_count * resistor_gap
            new_comp["layout_y"] = 650

        # -------------------------
        # Ground
        # -------------------------
        elif "ground" in name:

            new_comp["layout_x"] = ground_x
            new_comp["layout_y"] = ground_y

        # -------------------------
        # Ammeter / Voltmeter
        # -------------------------
        else:

            new_comp["layout_x"] = meter_x
            new_comp["layout_y"] = meter_y

            meter_y += 170

        layout.append(new_comp)

    # --------------------------------
    # Draw Preview
    # --------------------------------

    for comp in layout:

        x = int(comp["layout_x"])
        y = int(comp["layout_y"])

        cv2.circle(
            canvas,
            (x, y),
            10,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            canvas,
            comp["name"],
            (x + 20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 0),
            2
        )

    os.makedirs("output", exist_ok=True)

    with open("output/layout.json", "w") as f:

        json.dump(layout, f, indent=4)

    cv2.imwrite(
        "output/layout.png",
        canvas
    )

    return layout


# ---------------------------------------
# Run directly for testing
# ---------------------------------------

if __name__ == "__main__":

    with open("output/components.json") as f:

        components = json.load(f)

    layout = generate_layout(components)

    print("Layout Created Successfully!")

    print()

    for comp in layout:

        print(comp["name"], "->", comp["layout_x"], comp["layout_y"])
