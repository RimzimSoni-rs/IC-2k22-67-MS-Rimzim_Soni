from PIL import Image, ExifTags
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent.parent

INPUT_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# IMAGE METADATA ANALYSER
# ============================================================

def analyze_image(image_path):
    """
    Extract image metadata required for the
    Multimedia Metadata Analyzer activity.
    """

    image = Image.open(image_path)

    # --------------------------------------------------------
    # Basic file information
    # --------------------------------------------------------

    file_size_bytes = image_path.stat().st_size
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024

    # --------------------------------------------------------
    # Image information
    # --------------------------------------------------------

    file_format = image.format
    mode = image.mode

    width = image.width
    height = image.height

    resolution = f"{width} x {height}"

    total_pixels = width * height

    # --------------------------------------------------------
    # Colour depth
    # --------------------------------------------------------

    colour_depth_map = {
        "1": 1,
        "L": 8,
        "P": 8,
        "RGB": 24,
        "RGBA": 32,
        "CMYK": 32,
        "YCbCr": 24,
        "I": 32,
        "F": 32
    }

    colour_depth = colour_depth_map.get(mode, "Unknown")

    # --------------------------------------------------------
    # EXIF metadata
    # --------------------------------------------------------

    exif_data = image.getexif()

    exif_metadata = {}

    if exif_data:
        for tag_id, value in exif_data.items():

            tag_name = ExifTags.TAGS.get(tag_id, tag_id)

            # Avoid extremely large binary metadata
            if isinstance(value, bytes):
                value = f"<binary data: {len(value)} bytes>"

            exif_metadata[tag_name] = value

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print()
    print("=" * 55)
    print("           IMAGE METADATA ANALYSER")
    print("=" * 55)

    print("\n---------- FILE INFORMATION ----------")

    print("File Name       :", image_path.name)
    print("File Format     :", file_format)
    print(
        "File Size       :",
        f"{file_size_bytes} bytes "
        f"({file_size_kb:.2f} KB / {file_size_mb:.2f} MB)"
    )

    print("\n---------- IMAGE INFORMATION ----------")

    print("Image Mode      :", mode)
    print("Resolution      :", resolution)
    print("Width           :", width)
    print("Height          :", height)
    print("Total Pixels    :", total_pixels)

    print("\n---------- COLOUR DEPTH ----------")

    if isinstance(colour_depth, int):
        print("Colour Depth    :", colour_depth, "bits per pixel")
    else:
        print("Colour Depth    :", colour_depth)

    print("\n---------- METADATA ----------")

    if exif_metadata:

        print("EXIF Metadata   : Available")

        for key, value in exif_metadata.items():
            print(f"{key:<20}: {value}")

    else:

        print("EXIF Metadata   : Not available")

    print("\n" + "=" * 55)

    return {
        "file_name": image_path.name,
        "format": file_format,
        "file_size_bytes": file_size_bytes,
        "file_size_kb": file_size_kb,
        "file_size_mb": file_size_mb,
        "mode": mode,
        "resolution": resolution,
        "width": width,
        "height": height,
        "total_pixels": total_pixels,
        "colour_depth": colour_depth,
        "exif_metadata": exif_metadata
    }


# ============================================================
# SAVE CONSOLIDATED REPORT
# ============================================================

def save_report(data):

    report_path = OUTPUT_DIR / "image_metadata_report.txt"

    with open(report_path, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("           IMAGE METADATA ANALYSER REPORT\n")
        report.write("=" * 60 + "\n\n")

        report.write("FILE INFORMATION\n")
        report.write("-" * 60 + "\n")

        report.write(f"File Name       : {data['file_name']}\n")
        report.write(f"File Format     : {data['format']}\n")
        report.write(
            f"File Size       : {data['file_size_bytes']} bytes\n"
        )
        report.write(
            f"File Size       : {data['file_size_kb']:.2f} KB\n"
        )
        report.write(
            f"File Size       : {data['file_size_mb']:.2f} MB\n"
        )

        report.write("\nIMAGE INFORMATION\n")
        report.write("-" * 60 + "\n")

        report.write(f"Image Mode      : {data['mode']}\n")
        report.write(f"Resolution      : {data['resolution']}\n")
        report.write(f"Width           : {data['width']}\n")
        report.write(f"Height          : {data['height']}\n")
        report.write(f"Total Pixels    : {data['total_pixels']}\n")

        report.write("\nCOLOUR DEPTH\n")
        report.write("-" * 60 + "\n")

        if isinstance(data["colour_depth"], int):
            report.write(
                f"Colour Depth    : "
                f"{data['colour_depth']} bits per pixel\n"
            )
        else:
            report.write(
                f"Colour Depth    : {data['colour_depth']}\n"
            )

        report.write("\nMETADATA\n")
        report.write("-" * 60 + "\n")

        if data["exif_metadata"]:

            report.write("EXIF Metadata   : Available\n\n")

            for key, value in data["exif_metadata"].items():
                report.write(f"{key:<20}: {value}\n")

        else:

            report.write("EXIF Metadata   : Not available\n")

        report.write("\n")
        report.write("=" * 60 + "\n")
        report.write("              ANALYSIS COMPLETED\n")
        report.write("=" * 60 + "\n")

    print("\nReport saved at:")
    print(report_path)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("UNIT 1 - IMAGE METADATA ANALYSER")
    print("=" * 60)

    # Find image files in inputs folder
    image_files = []

    image_files += list(INPUT_DIR.glob("*.jpg"))
    image_files += list(INPUT_DIR.glob("*.jpeg"))
    image_files += list(INPUT_DIR.glob("*.png"))
    image_files += list(INPUT_DIR.glob("*.gif"))
    image_files += list(INPUT_DIR.glob("*.tiff"))
    image_files += list(INPUT_DIR.glob("*.tif"))

    if not image_files:

        print("\nNo image found in the inputs folder.")
        print("Please place an image inside:")
        print(INPUT_DIR)

    else:

        # Use the first image found
        image_path = image_files[0]

        print("\nInput Image:")
        print(image_path)

        result = analyze_image(image_path)

        save_report(result)

        print("\n" + "=" * 60)
        print("IMAGE METADATA ANALYSIS COMPLETED")
        print("=" * 60)