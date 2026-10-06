import cv2
from pathlib import Path


# ---------------------------------------------------------
# Directory Configuration
# ---------------------------------------------------------

INPUT_DIR = Path(__file__).parent.parent / "inputs"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Video Frame Extraction
# ---------------------------------------------------------

def extract_video_frames(video_path):

    # Open the video
    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        print("Error: Could not open video.")
        return

    # Get video information
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = total_frames / fps if fps > 0 else 0

    print("\n========== VIDEO INFORMATION ==========")

    print("File Name:", video_path.name)
    print("Width:", width)
    print("Height:", height)
    print("Resolution:", width, "x", height)
    print("Frame Rate:", round(fps, 2), "FPS")
    print("Total Frames:", total_frames)
    print("Duration:", round(duration, 3), "seconds")

    print("\n========== FRAME EXTRACTION ==========")

    # Number of frames to extract
    number_of_frames = 5

    # Calculate interval between extracted frames
    if total_frames > number_of_frames:
        interval = total_frames // number_of_frames
    else:
        interval = 1

    extracted_count = 0

    for i in range(number_of_frames):

        frame_number = i * interval

        # Do not go beyond the video
        if frame_number >= total_frames:
            break

        # Move video to the required frame
        video.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_number
        )

        success, frame = video.read()

        if not success:
            print(
                "Could not read frame:",
                frame_number
            )
            continue

        output_path = (
            OUTPUT_DIR /
            f"frame_{extracted_count + 1}.jpg"
        )

        cv2.imwrite(
            str(output_path),
            frame
        )

        extracted_count += 1

        print(
            f"Frame {extracted_count} "
            f"extracted from frame number "
            f"{frame_number}"
        )

        print(
            "Saved at:",
            output_path
        )

    # Release video
    video.release()

    print("\n========================================")
    print(" VIDEO FRAME EXTRACTION COMPLETED")
    print("Frames extracted:", extracted_count)
    print("========================================")


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    video_files = list(INPUT_DIR.glob("*.mp4"))
    video_files += list(INPUT_DIR.glob("*.avi"))
    video_files += list(INPUT_DIR.glob("*.mkv"))

    if not video_files:

        print(
            "No video found in the inputs folder."
        )

        print(
            "Please add an MP4, AVI, or MKV video."
        )

    else:

        video_path = video_files[0]

        print("\n========================================")
        print(" UNIT 1 - VIDEO FRAME EXTRACTION")
        print("========================================")

        extract_video_frames(video_path)