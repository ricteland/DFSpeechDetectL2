import os
import whisper
from pydub import AudioSegment


class AudioTranscriber:
    def __init__(self, input_folder, clips_folder, txt_folder, model_name="turbo", device="cuda"):
        """
        Initializes the AudioTranscriber class.

        :param input_folder: Path to the folder containing original audio files.
        :param clips_folder: Path to save split audio clips.
        :param txt_folder: Path to save transcript files.
        :param model_name: Whisper model to use (default: "base-en").
        :param device: Device to run Whisper on ("cuda" for GPU, "cpu" for CPU).
        """
        self.input_folder = input_folder
        self.clips_folder = clips_folder
        self.txt_folder = txt_folder
        self.device = device

        # Ensure output directories exist
        os.makedirs(self.clips_folder, exist_ok=True)
        os.makedirs(self.txt_folder, exist_ok=True)

        # Load Whisper model
        print(f"Loading Whisper model: {model_name} on {device}...")
        self.model = whisper.load_model(model_name, device=device)

    def transcribe_and_divide(self, audio_path):
        """
        Splits an audio file into segments based on Whisper's transcription timestamps.

        :param audio_path: Path to the input audio file.
        :return: List of (clip_path, transcript) tuples.
        """

        # Step 1: Transcribe the full audio
        result = self.model.transcribe(audio_path, language="en", word_timestamps=True)
        segments = result["segments"]

        # Load the full audio
        audio = AudioSegment.from_wav(audio_path)
        filename_base = os.path.splitext(os.path.basename(audio_path))[0]

        clip_paths = []

        print("Splitting audio into segments...")
        # Step 2: Iterate over Whisper's segments and split the audio
        for i, segment in enumerate(segments):
            start_time = int(segment["start"] * 1000)  # Convert to milliseconds
            end_time = int(segment["end"] * 1000)  # Convert to milliseconds
            text = segment["text"]

            if end_time - start_time < 1000:
                continue

            # Extract segment audio
            clip = audio[start_time:end_time]

            # Save the clip
            clip_filename = f"{filename_base}_segment_{i + 1}.wav"
            clip_path = os.path.join(self.clips_folder, clip_filename)
            clip.export(clip_path, format="wav")

            # Save transcript
            txt_filename = f"{filename_base}_segment_{i + 1}.txt"
            txt_path = os.path.join(self.txt_folder, txt_filename)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            clip_paths.append((clip_path, text))
            print(f"Saved segment {i + 1}: {clip_filename} ({segment['start']}s - {segment['end']}s)")

        return clip_paths

    def process_all_files(self):
        """
        Processes all WAV files in the input folder by transcribing them,
        splitting them into Whisper-based segments, and saving transcripts.
        """
        for filename in os.listdir(self.input_folder):
            if filename.endswith(".wav"):
                file_path = os.path.join(self.input_folder, filename)
                print(f"\nTranscribing and splitting: {filename}")

                # Step 1: Transcribe & split based on segments
                self.transcribe_and_divide(file_path)

        print("\n✅ Processing complete! All segmented clips and transcripts saved.")


# === Usage ===
if __name__ == "__main__":
    input_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\test"
    clips_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS clips"
    txt_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS txt"

    transcriber = AudioTranscriber(input_folder, clips_folder, txt_folder, device="cuda")
    transcriber.process_all_files()
