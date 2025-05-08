import os
import csv
import random
from pathlib import Path

data = r'C:\Users\Usuario\Desktop\TUE\BEP 2025\data\BEP-L2-BonaFide'
def generate_xtts_metadata(
    base_data_dir,
    output_train="metadata_train.csv",
    output_dev="metadata_dev.csv",
    dev_ratio=0.15
):
    rows = []

    # Loop through speaker folders
    for speaker_name in sorted(os.listdir(base_data_dir)):
        speaker_dir = os.path.join(base_data_dir, speaker_name)
        wav_dir = os.path.join(speaker_dir, "wav")
        txt_dir = os.path.join(speaker_dir, "transcript")

        if not os.path.isdir(wav_dir) or not os.path.isdir(txt_dir):
            continue

        for wav_file in sorted(os.listdir(wav_dir)):
            if not wav_file.endswith(".wav"):
                continue

            base_filename = os.path.splitext(wav_file)[0]
            txt_file = os.path.join(txt_dir, base_filename + ".txt")
            wav_file_path = os.path.abspath(os.path.join(wav_dir, wav_file))

            if os.path.isfile(txt_file):
                with open(txt_file, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                if text:
                    rows.append((wav_file_path, text, speaker_name))
            else:
                print(f"⚠️ Skipping missing transcript: {txt_file}")

    # Shuffle and split into train/dev
    random.shuffle(rows)
    split_index = int(len(rows) * (1 - dev_ratio))
    train_rows = rows[:split_index]
    dev_rows = rows[split_index:]

    # Write both CSVs
    for filename, data in [(output_train, train_rows), (output_dev, dev_rows)]:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["audio_filepath", "text", "speaker_name"])
            writer.writerows(data)
        print(f"✅ Saved {filename} with {len(data)} samples.")

# Example usage:
generate_xtts_metadata(data)
