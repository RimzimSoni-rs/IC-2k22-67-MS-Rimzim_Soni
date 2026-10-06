from PIL import Image
from pathlib import Path


# ---------------------------------------------------------
# Directory Configuration
# ---------------------------------------------------------

INPUT_DIR = Path(__file__).parent.parent / "inputs"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 1. Image Information
# Requirement:
# Image resolution and colour depth analysis
# ---------------------------------------------------------

def analyze_image(image_path):
    image = Image.open(image_path)

    print("\n========== IMAGE INFORMATION ==========")

    print("File Name:", image_path.name)
    print("Format:", image.format)
    print("Mode:", image.mode)

    print("Resolution:", image.size)
    print("Width:", image.width)
    print("Height:", image.height)

    total_pixels = image.width * image.height
    print("Total Pixels:", total_pixels)


# ---------------------------------------------------------
# 2. Colour Depth Analysis
# Requirement:
# Image resolution and colour depth analysis
# ---------------------------------------------------------

def analyze_color_depth(image_path):
    image = Image.open(image_path)

    # Approximate colour depth based on image mode
    mode_to_depth = {
        "1": 1,
        "L": 8,
        "P": 8,
        "RGB": 24,
        "RGBA": 32,
        "CMYK": 32
    }

    color_depth = mode_to_depth.get(image.mode, "Unknown")

    print("\n========== COLOUR DEPTH ANALYSIS ==========")

    print("Image Mode:", image.mode)
    print("Colour Depth:", color_depth, "bits per pixel")

    total_pixels = image.width * image.height
    print("Total Pixels:", total_pixels)

    if isinstance(color_depth, int):
        raw_size_bits = total_pixels * color_depth
        raw_size_bytes = raw_size_bits / 8
        raw_size_kb = raw_size_bytes / 1024

        print("Approx. Uncompressed Size:",
              round(raw_size_kb, 2), "KB")


# ---------------------------------------------------------
# 3. RGB to Grayscale Conversion
# Requirement:
# RGB and Grayscale images
# ---------------------------------------------------------

def convert_to_grayscale(image_path):
    image = Image.open(image_path)

    grayscale = image.convert("L")

    output_path = OUTPUT_DIR / "grayscale_image.jpg"

    grayscale.save(output_path)

    print("\n========== GRAYSCALE CONVERSION ==========")

    print("Original image:", image_path.name)
    print("Grayscale image saved at:", output_path)


# ---------------------------------------------------------
# 4. RGB to HSV Conversion
# Requirement:
# RGB to HSV conversion
# ---------------------------------------------------------

def convert_to_hsv(image_path):
    image = Image.open(image_path).convert("RGB")

    # Convert RGB image to HSV
    hsv_image = image.convert("HSV")

    # Separate HSV channels
    hue, saturation, value = hsv_image.split()

    # Save individual channels because
    # PNG does not directly support Pillow's HSV mode.
    hue_path = OUTPUT_DIR / "hue_channel.png"
    saturation_path = OUTPUT_DIR / "saturation_channel.png"
    value_path = OUTPUT_DIR / "value_channel.png"

    hue.save(hue_path)
    saturation.save(saturation_path)
    value.save(value_path)

    print("\n========== HSV CONVERSION ==========")

    print("Original image:", image_path.name)
    print("HSV conversion completed successfully.")

    print("Hue channel saved at:", hue_path)
    print("Saturation channel saved at:", saturation_path)
    print("Value channel saved at:", value_path)


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    # Find supported image files
    image_files = list(INPUT_DIR.glob("*.jpg"))
    image_files += list(INPUT_DIR.glob("*.jpeg"))
    image_files += list(INPUT_DIR.glob("*.png"))
    image_files += list(INPUT_DIR.glob("*.tiff"))
    image_files += list(INPUT_DIR.glob("*.tif"))

    if not image_files:

        print("No image found in the inputs folder.")

    else:

        # Use the first image found
        image_path = image_files[0]

        print("\n========================================")
        print(" UNIT 1 - IMAGE DATA REPRESENTATION")
        print("========================================")

        # Image information
        analyze_image(image_path)

        # Resolution and colour depth
        analyze_color_depth(image_path)

        # RGB -> Grayscale
        convert_to_grayscale(image_path)

        # RGB -> HSV
        convert_to_hsv(image_path)

        print("\n========================================")
        print(" IMAGE PROCESSING COMPLETED")
        print("========================================")