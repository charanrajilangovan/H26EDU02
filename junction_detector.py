import cv2
import numpy as np
import os

# -----------------------
# Load Binary Image
# -----------------------

binary = cv2.imread(
    "output/binary.png",
    cv2.IMREAD_GRAYSCALE
)

if binary is None:
    print("binary.png not found!")
    exit()

# -----------------------
# Find Corners/Junctions
# -----------------------

corners = cv2.goodFeaturesToTrack(
    binary,
    maxCorners=300,
    qualityLevel=0.01,
    minDistance=10
)

output = cv2.cvtColor(
    binary,
    cv2.COLOR_GRAY2BGR
)

count = 0

if corners is not None:

    corners = np.int32(corners)

    for corner in corners:

        x, y = corner.ravel()

        cv2.circle(
            output,
            (x, y),
            5,
            (0,0,255),
            -1
        )

        count += 1

print("Junctions Found :", count)

os.makedirs("output", exist_ok=True)

cv2.imwrite(
    "output/junctions.png",
    output
)

print("Finished!")
