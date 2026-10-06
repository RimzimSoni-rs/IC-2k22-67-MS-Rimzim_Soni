from pathlib import Path
import wave


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).parent.parent

INPUT_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# AUDIO METADATA ANALYSER
# ============================================================

def analyze_audio(audio_path):

    try:
        audio = wave.open(str(audio_path), "rb")
    except Exception as e:
        print("ERROR: Unable to open audio file.")
        print("Reason:", e)
        return

    # --------------------------------------------------------
    # AUDIO INFORMATION
    # --------------------------------------------------------

    channels = audio.getnchannels()
    sample_rate = audio.getframerate()
    sample_width = audio.getsampwidth()
    total_frames = audio.getnframes()

    # Bit depth
    bit_depth = sample_width * 8

    # Duration
    duration = total_frames / sample_rate if sample_rate > 0 else 0

    # Compression information
    compression_type = audio.getcomptype()
    compression_name = audio.getcompname()

    # File size
    file_size = audio_path.stat().st_size

    file_size_kb = file_size / 1024
    file_size_mb = file_size_kb / 1024

    audio.close()

    # ========================================================
    # DISPLAY AUDIO METADATA
    # ========================================================

    print("=" * 60)
    print("              AUDIO METADATA ANALYSER")
    print("=" * 60)

    print("\n---------- FILE INFORMATION ----------")

    print(f"File Name       : {audio_path.name}")
    print(
        f"File Format     : "
        f"{audio_path.suffix.upper().replace('.', '')}"
    )
    print(
        f"File Size       : {file_size} bytes "
        f"({file_size_kb:.2f} KB / {file_size_mb:.2f} MB)"
    )

    print("\n---------- AUDIO INFORMATION ----------")

    print(f"Channels        : {channels}")
    print(f"Channel Type    : {'Mono' if channels == 1 else 'Stereo' if channels == 2 else 'Multi-channel'}")
    print(f"Sampling Rate   : {sample_rate} Hz")
    print(f"Bit Depth       : {bit_depth} bits")
    print(f"Sample Width    : {sample_width} bytes")
    print(f"Total Frames    : {total_frames}")
    print(f"Duration        : {duration:.3f} seconds")
    print(f"Compression     : {compression_type}")
    print(f"Compression Name: {compression_name}")

    # ========================================================
    # SAVE REPORT
    # ========================================================

    report_path = OUTPUT_DIR / "audio_metadata_report.txt"

    with open(report_path, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("              AUDIO METADATA ANALYSER\n")
        report.write("=" * 60 + "\n\n")

        report.write("---------- FILE INFORMATION ----------\n\n")

        report.write(f"File Name       : {audio_path.name}\n")
        report.write(
            f"File Format     : "
            f"{audio_path.suffix.upper().replace('.', '')}\n"
        )
        report.write(
            f"File Size       : {file_size} bytes "
            f"({file_size_kb:.2f} KB / {file_size_mb:.2f} MB)\n"
        )

        report.write("\n---------- AUDIO INFORMATION ----------\n\n")

        report.write(f"Channels        : {channels}\n")
        report.write(
            f"Channel Type    : "
            f"{'Mono' if channels == 1 else 'Stereo' if channels == 2 else 'Multi-channel'}\n"
        )
        report.write(f"Sampling Rate   : {sample_rate} Hz\n")
        report.write(f"Bit Depth       : {bit_depth} bits\n")
        report.write(f"Sample Width    : {sample_width} bytes\n")
        report.write(f"Total Frames    : {total_frames}\n")
        report.write(f"Duration        : {duration:.3f} seconds\n")
        report.write(f"Compression     : {compression_type}\n")
        report.write(f"Compression Name: {compression_name}\n")

    print("\nReport saved at:")
    print(report_path)

    print("\n" + "=" * 60)
    print("       AUDIO METADATA ANALYSIS COMPLETED")
    print("=" * 60)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    audio_files = []

    audio_files += list(INPUT_DIR.glob("*.wav"))

    if not audio_files:

        print("No WAV audio found in the inputs folder.")

    else:

        audio_path = audio_files[0]

        analyze_audio(audio_path)