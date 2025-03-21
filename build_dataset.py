import pandas as pd
import os
from transcription_splitting import AudioTranscriber
from downsampler import downsample_audio
from diarization import SpeakerDiarizationProcessor
import warnings
warnings.filterwarnings("ignore")

def file_id_to_nr(file):
    fileid = os.path.basename(file)[5:8]
    id = int(fileid)
    return id

class Preprocessor:

    def __init__(self, input_directory, diarized_path, output_directory, hf_token, speaker_nr = 3, device = "cuda"):
        self.input_path = input_directory
        self.diarized_path = diarized_path
        self.output_path = output_directory
        self.device = device
        self.speaker_nr = speaker_nr
        self.hf = hf_token

    def downsample(self, rate=24000):
        downsample_audio(input_directory= self.input_path ,
                         output_directory=self.diarized_path ,
                         rate=rate)

    def diarize_file(self):
        diarizer = SpeakerDiarizationProcessor(input_folder=self.input_path,
                                               output_folder=self.diarized_path,
                                               huggingface_token=self.hf,
                                               max_speakers=self.speaker_nr)
        diarizer.process_all_files()

    def transcribe_file(self):
        transcriber = AudioTranscriber(input_folder=self.diarized_path,
                                       clips_folder = self.output_path,
                                       txt_folder=self.output_path,
                                       device=self.device)
        transcriber.process_all_files()

        print(f"Deleting files in {self.diarized_path}")
        for filename in os.listdir(self.diarized_path):
            file_path = os.path.join(self.diarized_path, filename)
            os.remove(file_path)


    def preprocess_files(self):
        print("Preprocessing files...")

        # print("Diarizing...")
        # self.diarize_file()

        print("Downsampling...")
        self.downsample()


        print("Transcribing and splitting...")
        self.transcribe_file()


input = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS data"
diarized = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS diarized"
output = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS clips"
with open('your_file.txt', 'r', encoding='utf-8') as file:
    hf_token = file.readline()

Preprocessor(input, diarized, output, hf_token, 3, "cuda").preprocess_files()



