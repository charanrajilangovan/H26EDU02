import json
import cv2
import os

# -----------------------------
# Load image
# -----------------------------
image = cv2.imread("test.jpg")

if image is None:
    print("Image not found!")
    exit()

# -----------------------------
# Load components
# -----------------------------
with open("output/components.json", "r") as f:
    components = json.load(f)

# -----------------------------
# Draw graph nodes
# -----------------------------
for i, comp in enumerate(components):

    x = comp["x"]
    y = comp["y"]

    cv2.circle(image, (x, y), 6, (0, 0, 255), -1)

    cv2.putText(
        image,
        str(i),
        (x + 8, y - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2
    )

# -----------------------------
# Save
# -----------------------------
os.makedirs("output", exist_ok=True)

cv2.imwrite("output/component_graph.png", image)

print("Component graph created!")
