import cv2
import os
import numpy as np

# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

INPUT_IMAGE = "Cluster01-Multimedia-Fundamentals/inputs/sample.jpg"

OUTPUT_DIR = "Cluster02-Image-Processing/outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------
# Load Image
# ---------------------------------------------------------

image = cv2.imread(INPUT_IMAGE)

if image is None:
    print("ERROR: Could not find input image.")
    print("Expected:", INPUT_IMAGE)
    exit()

print("=" * 60)
print("              IMAGE ENHANCEMENT")
print("=" * 60)

print("\nInput image:", INPUT_IMAGE)

height, width = image.shape[:2]

print("Original resolution:", width, "x", height)


# ---------------------------------------------------------
# 1. Brightness and Contrast Enhancement
# ---------------------------------------------------------

brightness = 15
contrast = 1.2

brightness_contrast = cv2.convertScaleAbs(
    image,
    alpha=contrast,
    beta=brightness
)

path1 = os.path.join(
    OUTPUT_DIR,
    "brightness_contrast.jpg"
)

cv2.imwrite(path1, brightness_contrast)

print("[+] Brightness and contrast enhancement saved.")


# ---------------------------------------------------------
# 2. Sharpening
# ---------------------------------------------------------

kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

sharpened = cv2.filter2D(
    image,
    -1,
    kernel
)

path2 = os.path.join(
    OUTPUT_DIR,
    "sharpened_image.jpg"
)

cv2.imwrite(path2, sharpened)

print("[+] Sharpened image saved.")


# ---------------------------------------------------------
# 3. Histogram Equalization
# ---------------------------------------------------------

gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

hist_equalized = cv2.equalizeHist(gray)

path3 = os.path.join(
    OUTPUT_DIR,
    "histogram_equalized.jpg"
)

cv2.imwrite(path3, hist_equalized)

print("[+] Histogram equalized image saved.")


# ---------------------------------------------------------
# 4. CLAHE Enhancement
# ---------------------------------------------------------

lab = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2LAB
)

l_channel, a_channel, b_channel = cv2.split(lab)

clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

enhanced_l = clahe.apply(l_channel)

enhanced_lab = cv2.merge([
    enhanced_l,
    a_channel,
    b_channel
])

clahe_image = cv2.cvtColor(
    enhanced_lab,
    cv2.COLOR_LAB2BGR
)

path4 = os.path.join(
    OUTPUT_DIR,
    "clahe_enhanced.jpg"
)

cv2.imwrite(path4, clahe_image)

print("[+] CLAHE enhanced image saved.")


# ---------------------------------------------------------
# 5. Final Enhanced Image
# ---------------------------------------------------------

final_image = cv2.addWeighted(
    clahe_image,
    0.7,
    sharpened,
    0.3,
    0
)

final_path = os.path.join(
    OUTPUT_DIR,
    "final_enhanced_image.jpg"
)

cv2.imwrite(
    final_path,
    final_image
)

print("[+] Final enhanced image saved.")


# ---------------------------------------------------------
# 6. Before / After Comparison
# ---------------------------------------------------------

comparison = np.hstack([
    image,
    final_image
])

comparison_path = os.path.join(
    OUTPUT_DIR,
    "before_after_comparison.jpg"
)

cv2.imwrite(
    comparison_path,
    comparison
)

print("[+] Before/after comparison saved.")


# ---------------------------------------------------------
# Final Report
# ---------------------------------------------------------

print("\n--- Image Enhancement Report ---")

print("Original Resolution :", width, "x", height)
print("Brightness Adjustment :", brightness)
print("Contrast Factor :", contrast)
print("Sharpening :", "Applied")
print("Histogram Equalization :", "Applied")
print("CLAHE :", "Applied")

print("\nOutput files:")

for file in os.listdir(OUTPUT_DIR):
    print(" -", file)

print("\n" + "=" * 60)
print("       IMAGE ENHANCEMENT COMPLETED")
print("=" * 60)