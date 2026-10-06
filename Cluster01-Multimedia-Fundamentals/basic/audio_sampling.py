import wave
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Directory Configuration
# ---------------------------------------------------------

INPUT_DIR = Path(__file__).parent.parent / "inputs"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 1. Read and Analyse Audio
# ---------------------------------------------------------

def analyze_audio(audio_path):

    with wave.open(str(audio_path), "rb") as audio:

        channels = audio.getnchannels()
        sample_width = audio.getsampwidth()
        sample_rate = audio.getframerate()
        number_of_frames = audio.getnframes()

        duration = number_of_frames / sample_rate

        bit_depth = sample_width * 8

        print("\n========== AUDIO INFORMATION ==========")

        print("File Name:", audio_path.name)
        print("Channels:", channels)
        print("Sampling Rate:", sample_rate, "Hz")
        print("Bit Depth:", bit_depth, "bits")
        print("Number of Frames:", number_of_frames)
        print("Duration:", round(duration, 3), "seconds")


# ---------------------------------------------------------
# 2. Read Audio Samples
# ---------------------------------------------------------

def read_audio_samples(audio_path):

    with wave.open(str(audio_path), "rb") as audio:

        sample_width = audio.getsampwidth()
        number_of_frames = audio.getnframes()

        raw_data = audio.readframes(number_of_frames)

        if sample_width == 1:

            samples = np.frombuffer(
                raw_data,
                dtype=np.uint8
            )

        elif sample_width == 2:

            samples = np.frombuffer(
                raw_data,
                dtype=np.int16
            )

        elif sample_width == 4:

            samples = np.frombuffer(
                raw_data,
                dtype=np.int32
            )

        else:

            raise ValueError(
                "Unsupported audio sample width."
            )

    return samples


# ---------------------------------------------------------
# 3. Audio Sampling
# ---------------------------------------------------------

def demonstrate_sampling(audio_path):

    samples = read_audio_samples(audio_path)

    with wave.open(str(audio_path), "rb") as audio:
        sample_rate = audio.getframerate()

    # Display only the first part of the signal
    number_of_samples_to_display = min(
        len(samples),
        sample_rate // 10
    )

    selected_samples = samples[
        :number_of_samples_to_display
    ]

    time = np.arange(
        len(selected_samples)
    ) / sample_rate

    plt.figure(figsize=(10, 5))

    plt.plot(time, selected_samples)

    plt.title("Audio Sampling - Original Samples")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")

    plt.grid(True)

    output_path = OUTPUT_DIR / "audio_sampling.png"

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()

    print("\n========== AUDIO SAMPLING ==========")
    print("Sampling rate:", sample_rate, "Hz")
    print("Sampling graph saved at:", output_path)


# ---------------------------------------------------------
# 4. Audio Quantization
# ---------------------------------------------------------

def demonstrate_quantization(audio_path):

    samples = read_audio_samples(audio_path)

    with wave.open(str(audio_path), "rb") as audio:
        sample_width = audio.getsampwidth()

    original_bit_depth = sample_width * 8

    # Quantize to 8 bits for demonstration
    target_bit_depth = 8

    if original_bit_depth <= target_bit_depth:

        quantized_samples = samples.copy()

    else:

        min_value = samples.min()
        max_value = samples.max()

        # Normalize original samples to 0-255
        normalized = (
            (samples - min_value)
            / (max_value - min_value)
        )

        quantized_samples = (
            normalized * 255
        ).astype(np.uint8)

    number_of_samples_to_display = min(
        len(quantized_samples),
        5000
    )

    original_display = samples[
        :number_of_samples_to_display
    ]

    quantized_display = quantized_samples[
        :number_of_samples_to_display
    ]

    plt.figure(figsize=(10, 5))

    plt.plot(
        original_display,
        label="Original"
    )

    plt.plot(
        quantized_display,
        label="Quantized to 8-bit"
    )

    plt.title("Audio Quantization")
    plt.xlabel("Sample Number")
    plt.ylabel("Amplitude")

    plt.legend()
    plt.grid(True)

    output_path = OUTPUT_DIR / "audio_quantization.png"

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()

    print("\n========== AUDIO QUANTIZATION ==========")
    print("Original Bit Depth:",
          original_bit_depth, "bits")

    print("Target Quantization:",
          target_bit_depth, "bits")

    print(
        "Quantization graph saved at:",
        output_path
    )


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    audio_files = list(
        INPUT_DIR.glob("*.wav")
    )

    if not audio_files:

        print(
            "No WAV audio file found "
            "in the inputs folder."
        )

    else:

        audio_path = audio_files[0]

        print("\n========================================")
        print(" UNIT 1 - AUDIO SAMPLING & QUANTIZATION")
        print("========================================")

        analyze_audio(audio_path)

        demonstrate_sampling(audio_path)

        demonstrate_quantization(audio_path)

        print("\n========================================")
        print(" AUDIO PROCESSING COMPLETED")
        print("========================================")