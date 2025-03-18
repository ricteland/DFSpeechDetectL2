import os
from pydub import AudioSegment

# Set your directory path
input_path = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\test"  # Change this to your folder path
output_path = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\downsample_test"

def show_audio_properties(directory_path):
    duration_total = 0
    for filename in os.listdir(directory_path):
        if filename.endswith(".wav"):  # Process only .wav files
            file_path = os.path.join(directory_path, filename)

            # Load the audio file
            audio = AudioSegment.from_file(file_path)

            # Extract required properties
            duration = len(audio) / 1000  # Convert from ms to seconds
            duration_total += duration
            sampling_rate = audio.frame_rate  # Hz
            loudness = audio.dBFS  # Loudness in decibels (RMS-based)
            channels = audio.channels  # 1 = Mono, 2 = Stereo
            bit_depth = audio.sample_width * 8  # Convert from bytes to bits (8, 16, 24, 32)

            print(f"File: {filename}")
            print(f"  Sampling Rate: {sampling_rate/1000} kHz")
            print(f"  Loudness: {loudness:.2f} dBFS")
            print(f"  Channels: {'Mono' if channels == 1 else 'Stereo'}")
            print(f"  Bit Depth: {bit_depth}-bit\n")

    print(f"Total duration:{duration_total/3600} hours")



def downsample_audio(directory_path, output_directory, rate=24000):
    # Iterate through all WAV files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".wav"):  # Process only .wav files
            file_path = os.path.join(directory_path, filename)
            output_path = os.path.join(output_directory, filename)  # Save with same filename

            # Load the original audio file
            audio = AudioSegment.from_file(file_path)

            # Resample to 24kHz (24000 Hz)
            downsampled_audio = audio.set_frame_rate(rate)

            # Export the resampled file
            downsampled_audio.export(output_path, format="wav")

            print(f"Processed: {filename} → Downsampled to 24kHz and saved to {output_path}")

