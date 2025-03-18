import os
import re
from pyannote.audio import Pipeline
from pydub import AudioSegment
import torch

class SpeakerDiarizationProcessor:
    def __init__(self, input_folder, output_folder, huggingface_token, max_speakers=3):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.huggingface_token = huggingface_token
        self.max_speakers = max_speakers

        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

        # Load Pyannote pipeline
        self.pipeline = self.load_pipeline()

    def load_pipeline(self):
        """Load the Pyannote speaker diarization model."""
        print("Loading Pyannote speaker diarization model...")
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=self.huggingface_token,
        )
        pipeline.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        return pipeline

    def process_file(self, file_path):
        """Process a single audio file and save speaker-separated audio segments."""
        filename = os.path.basename(file_path)

        print(f"Processing: {filename}")
        diarization = self.pipeline(file_path, max_speakers=self.max_speakers)
        audio = AudioSegment.from_wav(file_path)

        # Store separated speaker segments
        speakers_audio = {}

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start_ms = int(turn.start * 1000)  # Convert to milliseconds
            end_ms = int(turn.end * 1000)
            segment_audio = audio[start_ms:end_ms]

            if speaker not in speakers_audio:
                speakers_audio[speaker] = segment_audio
            else:
                speakers_audio[speaker] += segment_audio

        # Save extracted speakers
        for speaker, speaker_audio in speakers_audio.items():
            output_filename = f"{filename}_{speaker}.wav"
            output_path = os.path.join(self.output_folder, output_filename)
            speaker_audio.export(output_path, format="wav")
            print(f"Saved: {output_path}")

    def process_all_files(self):
        """Process all .wav files in the input folder."""
        for filename in os.listdir(self.input_folder):
            if filename.endswith(".wav"):
                file_path = os.path.join(self.input_folder, filename)
                self.process_file(file_path)

        print("Processing complete!")



# === Usage ===
if __name__ == "__main__":
    # Define paths
    input_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\temp"
    output_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS diarized"
    huggingface_token = open("hf.txt", "r").read().strip()

    # Initialize and run processing
    processor = SpeakerDiarizationProcessor(input_folder, output_folder, huggingface_token)
    processor.process_all_files()
