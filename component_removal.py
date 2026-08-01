from ultralytics import YOLO
import cv2
import os

# -----------------------------
# Load YOLO Model
# -----------------------------
model = YOLO("best.pt")

# -----------------------------
# Load Image
# -----------------------------
image_path = "test.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

# -----------------------------
# Detect Components
# -----------------------------
results = model.predict(
    source=image_path,
    conf=0.25,
    save=False
)

result = results[0]

# -----------------------------
# Remove Components
# -----------------------------
for box in result.boxes:

    x1, y1, x2, y2 = map(int, box.xyxy[0])

    # Small padding
    pad = 5

    x1 = max(0, x1-pad)
    y1 = max(0, y1-pad)
    x2 = min(image.shape[1], x2+pad)
    y2 = min(image.shape[0], y2+pad)

    # Paint detected component white
    image[y1:y2, x1:x2] = (255,255,255)

# -----------------------------
# Save Output
# -----------------------------
os.makedirs("output", exist_ok=True)

cv2.imwrite("output/components_removed.png", image)

print("Components Removed Successfully!")
