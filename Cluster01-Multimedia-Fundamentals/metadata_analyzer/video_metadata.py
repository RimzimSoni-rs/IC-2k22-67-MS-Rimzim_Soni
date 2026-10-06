from pathlib import Path
import cv2


# ==============================
# PATH CONFIGURATION
# ==============================

BASE_DIR = Path(__file__).parent.parent

INPUT_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==============================
# VIDEO METADATA ANALYSER
# ==============================

def analyze_video(video_path):

    # Open video
    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        print("ERROR: Unable to open video.")
        return

    # Get video properties
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = video.get(cv2.CAP_PROP_FPS)

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = total_frames / fps if fps > 0 else 0

    # Codec
    codec_value = int(video.get(cv2.CAP_PROP_FOURCC))

    codec = "".join(
        [
            chr((codec_value >> 0) & 0xFF),
            chr((codec_value >> 8) & 0xFF),
            chr((codec_value >> 16) & 0xFF),
            chr((codec_value >> 24) & 0xFF)
        ]
    )

    # File size
    file_size = video_path.stat().st_size

    # Close video
    video.release()

    # Convert file size
    file_size_kb = file_size / 1024
    file_size_mb = file_size_kb / 1024

    # ==============================
    # DISPLAY METADATA
    # ==============================

    print("=" * 60)
    print("              VIDEO METADATA ANALYSER")
    print("=" * 60)

    print("\n---------- FILE INFORMATION ----------")

    print(f"File Name       : {video_path.name}")
    print(f"File Format     : {video_path.suffix.upper().replace('.', '')}")
    print(
        f"File Size       : {file_size} bytes "
        f"({file_size_kb:.2f} KB / {file_size_mb:.2f} MB)"
    )

    print("\n---------- VIDEO INFORMATION ----------")

    print(f"Resolution      : {width} x {height}")
    print(f"Width           : {width}")
    print(f"Height          : {height}")
    print(f"Frame Rate      : {fps:.2f} FPS")
    print(f"Total Frames    : {total_frames}")
    print(f"Duration        : {duration:.3f} seconds")
    print(f"Codec           : {codec}")

    # ==============================
    # SAVE REPORT
    # ==============================

    report_path = OUTPUT_DIR / "video_metadata_report.txt"

    with open(report_path, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("              VIDEO METADATA ANALYSER\n")
        report.write("=" * 60 + "\n\n")

        report.write("---------- FILE INFORMATION ----------\n\n")

        report.write(f"File Name       : {video_path.name}\n")
        report.write(
            f"File Format     : "
            f"{video_path.suffix.upper().replace('.', '')}\n"
        )
        report.write(
            f"File Size       : {file_size} bytes "
            f"({file_size_kb:.2f} KB / {file_size_mb:.2f} MB)\n"
        )

        report.write("\n---------- VIDEO INFORMATION ----------\n\n")

        report.write(f"Resolution      : {width} x {height}\n")
        report.write(f"Width           : {width}\n")
        report.write(f"Height          : {height}\n")
        report.write(f"Frame Rate      : {fps:.2f} FPS\n")
        report.write(f"Total Frames    : {total_frames}\n")
        report.write(f"Duration        : {duration:.3f} seconds\n")
        report.write(f"Codec           : {codec}\n")

    print("\nReport saved at:")
    print(report_path)

    print("\n" + "=" * 60)
    print("       VIDEO METADATA ANALYSIS COMPLETED")
    print("=" * 60)


# ==============================
# MAIN PROGRAM
# ==============================

if __name__ == "__main__":

    video_files = []

    video_files += list(INPUT_DIR.glob("*.mp4"))
    video_files += list(INPUT_DIR.glob("*.avi"))
    video_files += list(INPUT_DIR.glob("*.mov"))
    video_files += list(INPUT_DIR.glob("*.mkv"))

    if not video_files:

        print("No video found in the inputs folder.")

    else:

        video_path = video_files[0]

        analyze_video(video_path)