import os
import whisper
from pydub import AudioSegment


class AudioTranscriber:
    def __init__(self, input_folder, clips_folder, txt_folder, model_name="base.en", device="cuda"):
        """
        Initializes the AudioTranscriber class.

        :param input_folder: Path to the folder containing original audio files.
        :param clips_folder: Path to save split audio clips.
        :param txt_folder: Path to save transcript files.
        :param model_name: Whisper model to use (default: "base.en").
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

    def split_audio(self, audio_path, clip_length_ms=6000):
        """
        Splits an audio file into 6-second clips and saves them to the clips folder.

        :param audio_path: Path to the input audio file.
        :param clip_length_ms: Length of each audio clip in milliseconds (default: 6000ms or 6s).
        :return: List of file paths for the generated audio clips.
        """
        audio = AudioSegment.from_wav(audio_path)
        filename_base = os.path.splitext(os.path.basename(audio_path))[0]

        num_clips = len(audio) // clip_length_ms + (1 if len(audio) % clip_length_ms != 0 else 0)
        clip_paths = []

        for i in range(num_clips):
            start_time = i * clip_length_ms
            end_time = min((i + 1) * clip_length_ms, len(audio))
            clip = audio[start_time:end_time]

            # Save the clip in the clips folder
            clip_filename = f"{filename_base}_clip_{i + 1}.wav"
            clip_path = os.path.join(self.clips_folder, clip_filename)
            clip.export(clip_path, format="wav")

            clip_paths.append(clip_path)

        return clip_paths

    def transcribe_clip(self, clip_path):
        """
        Transcribes an audio clip using Whisper and saves the transcript as a .txt file.

        :param clip_path: Path to the audio clip to transcribe.
        """
        result = self.model.transcribe(clip_path, language="en")
        transcript_text = result["text"]

        # Create a .txt filename with the same name as the audio clip
        txt_filename = os.path.splitext(os.path.basename(clip_path))[0] + ".txt"
        txt_path = os.path.join(self.txt_folder, txt_filename)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        print(f"Saved transcript: {txt_path}")

    def process_all_files(self):
        """
        Processes all WAV files in the input folder by splitting them into clips,
        transcribing each clip, and saving transcripts.
        """
        for filename in os.listdir(self.input_folder):
            if filename.endswith(".wav"):
                file_path = os.path.join(self.input_folder, filename)
                print(f"Processing: {filename}")

                # Step 1: Split into 6-second clips
                clip_paths = self.split_audio(file_path)

                # Step 2: Transcribe each clip and save transcript
                for clip_path in clip_paths:
                    self.transcribe_clip(clip_path)

        print("Processing complete! All clips are in 'IELTS clips' and transcripts in 'IELTS txt'.")


# === Usage ===
if __name__ == "__main__":
    input_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\test"
    clips_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS clips"
    txt_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS txt"

    transcriber = AudioTranscriber(input_folder, clips_folder, txt_folder, model_name="base.en", device="cuda")
    transcriber.process_all_files()
