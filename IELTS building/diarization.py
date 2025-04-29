import os
from pyannote.audio import Pipeline
from pydub import AudioSegment
import torch

class SpeakerDiarizationProcessor:
    def __init__(self, input_folder, output_folder, huggingface_token, max_speakers=3):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.huggingface_token = huggingface_token
        self.max_speakers = max_speakers
        self.pipeline = None  # <- lazy init

        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

    def load_pipeline(self):
        """Load the Pyannote speaker diarization model."""
        if self.pipeline is None:
            print("Loading Pyannote speaker diarization model...")
            pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.huggingface_token,
            )
            pipeline.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            self.pipeline = pipeline

    def process_file(self, file_path):
        """Process a single audio file and save speaker-separated audio segments."""
        self.load_pipeline()  # <- only load when needed

        filename = os.path.basename(file_path)
        print(f"Diarizing: {filename}")
        diarization = self.pipeline(file_path, max_speakers=self.max_speakers)
        audio = AudioSegment.from_wav(file_path)

        # Store separated speaker segments
        speakers_audio = {}

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start_ms = int(turn.start * 1000)
            end_ms = int(turn.end * 1000)
            segment_audio = audio[start_ms:end_ms]

            if speaker not in speakers_audio:
                speakers_audio[speaker] = segment_audio
            else:
                speakers_audio[speaker] += segment_audio

        return speakers_audio

    def process_all_files(self):
        """Process all .wav files in the input folder."""
        for filename in os.listdir(self.input_folder):
            if filename.endswith(".wav"):
                file_path = os.path.join(self.input_folder, filename)
                speakers_audio = self.process_file(file_path)
                print(f"Found {len(speakers_audio)} speakers in {filename}")
                for speaker, speaker_audio in speakers_audio.items():
                    output_filename = f"{filename[:8]}_{speaker}.wav"
                    output_path = os.path.join(self.output_folder, output_filename)
                    speaker_audio.export(output_path, format="wav")
                    print(f"Saved: {output_path}")

        print("Processing complete!")
