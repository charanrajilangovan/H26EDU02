import cv2
import numpy as np
import os
import glob

# ----------------------------------
# Automatically find test image
# ----------------------------------
images = glob.glob("test.*")

if len(images) == 0:
    print("No test image found!")
    exit()

image_path = images[0]
print("Using:", image_path)

# ----------------------------------
# Load image
# ----------------------------------
image = cv2.imread(image_path)

if image is None:
    print("Cannot open image!")
    exit()

# ----------------------------------
# Convert to grayscale
# ----------------------------------
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ----------------------------------
# Blur
# ----------------------------------
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# ----------------------------------
# Threshold
# ----------------------------------
_, binary = cv2.threshold(
    blur,
    180,
    255,
    cv2.THRESH_BINARY_INV
)

# ----------------------------------
# Morphological Closing
# ----------------------------------
kernel = np.ones((3,3), np.uint8)

binary = cv2.morphologyEx(
    binary,
    cv2.MORPH_CLOSE,
    kernel,
    iterations=2
)

# ----------------------------------
# Detect Lines
# ----------------------------------
lines = cv2.HoughLinesP(
    binary,
    rho=1,
    theta=np.pi/180,
    threshold=40,
    minLineLength=25,
    maxLineGap=8
)

output = image.copy()

count = 0

if lines is not None:

    print("Detected:", len(lines), "lines")

    for line in lines:

        values = np.array(line).flatten()

        if len(values) != 4:
            continue

        x1, y1, x2, y2 = values

        cv2.line(
            output,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0,255,0),
            2
        )

        count += 1

else:

    print("No lines found!")

# ----------------------------------
# Save Output
# ----------------------------------
os.makedirs("output", exist_ok=True)

cv2.imwrite(
    "output/binary.png",
    binary
)

cv2.imwrite(
    "output/wires.png",
    output
)

print("Lines Drawn :", count)
print("Finished Successfully!")
