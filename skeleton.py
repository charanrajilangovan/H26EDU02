import cv2
import numpy as np
import os
from skimage.morphology import skeletonize

# ----------------------------------
# Load Binary Image
# ----------------------------------

binary = cv2.imread(
    "output/binary.png",
    cv2.IMREAD_GRAYSCALE
)

if binary is None:
    print("binary.png not found!")
    exit()

# ----------------------------------
# Convert to Binary (0 or 1)
# ----------------------------------

binary = binary > 0

# ----------------------------------
# Skeletonization
# ----------------------------------

skeleton = skeletonize(binary)

# ----------------------------------
# Convert Back to Image
# ----------------------------------

skeleton = (skeleton * 255).astype(np.uint8)

# ----------------------------------
# Save Output
# ----------------------------------

os.makedirs("output", exist_ok=True)

cv2.imwrite(
    "output/skeleton.png",
    skeleton
)

print("Skeleton Created Successfully!")
