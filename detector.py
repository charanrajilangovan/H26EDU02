from ultralytics import YOLO
import json
import os
import math

# Load YOLO model only once
model = YOLO("best.pt")


def detect_components(image_path):
    """
    Detect components from an image.

    Parameters:
        image_path (str): Path to input image.

    Returns:
        list: List of detected components.
    """

    results = model.predict(
        source=image_path,
        conf=0.40,
        iou=0.30,
        save=False
    )

    result = results[0]

    components = []

    # -----------------------------
    # Read detections
    # -----------------------------
    for box in result.boxes:

        cls = int(box.cls[0])

        name = model.names[cls]

        conf = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        components.append({
            "name": name,
            "confidence": conf,
            "x": cx,
            "y": cy,
            "bbox": [x1, y1, x2, y2]
        })

    # -----------------------------
    # Remove duplicate detections
    # -----------------------------
    filtered = []

    DISTANCE = 45

    for comp in components:

        duplicate = False

        for saved in filtered:

            if comp["name"] != saved["name"]:
                continue

            d = math.sqrt(
                (comp["x"] - saved["x"]) ** 2 +
                (comp["y"] - saved["y"]) ** 2
            )

            if d < DISTANCE:

                duplicate = True

                if comp["confidence"] > saved["confidence"]:
                    saved.update(comp)

                break

        if not duplicate:
            filtered.append(comp)

    # -----------------------------
    # Save JSON
    # -----------------------------
    os.makedirs("output", exist_ok=True)

    with open("output/components.json", "w") as f:
        json.dump(filtered, f, indent=4)

    return filtered


# -----------------------------
# Run directly (for testing)
# -----------------------------
if __name__ == "__main__":

    components = detect_components("test.jpg")

    print("\nDetected Components\n")

    for c in components:
        print(c)

    print("\nTotal:", len(components))
