import torch
from TTS.api import TTS

# Print available TTS models
view_models = input("View models? [y/n]\n")
if view_models == "y":
    tts_manager = TTS().list_models()
    all_models = tts_manager.list_models()
    print("TTS models:\n", all_models, "\n", sep = "")

# Prompt model selection
model = input("Enter model:\n")
# for example, tts_models/multilingual/multi-dataset/xtts_v2

# Example voice cloning with selected model
tts = TTS((model), progress_bar=True).to("cuda")
tts.tts_to_file("This is a voice cloning test. My name is Pedro Gonzalez and I want to talk as much as possible to provide a great test hello! [sigh]", speaker_wav=r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS students\IELTS011.wav_SPEAKER_02.wav",
                language="en", file_path=r"C:\Users\Usuario\Desktop\TUE\BEP 2025\test_models\XTTS\output.wav")