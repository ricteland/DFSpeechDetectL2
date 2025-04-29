import os
import shutil
import pandas as pd

csv_path = "C:/Users/Usuario/Desktop/TUE/BEP 2025/data/IELTS/IELTS merged.csv"
folder_path = "C:/Users/Usuario/Desktop/TUE/BEP 2025/data/IELTS/IELTS clips/balanced/wavs"
df = pd.read_csv(csv_path)
print(df["Speaker_ID"])


def organize_by_accent(folder_path: str, metadata_df: pd.DataFrame):
    # Create a map from filename to accent
    file_to_accent = metadata_df.set_index("wav")["Accent"].to_dict()

    for filename in os.listdir(folder_path):
        # Only process .wav and .txt files
        if not (filename.endswith(".wav") or filename.endswith(".txt")):
            continue

        # Check if there's a .wav file in metadata that matches this file (or its base name)
        base_name = filename.rsplit(".", 1)[0]
        wav_name = base_name + ".wav"

        accent = file_to_accent.get(wav_name)
        if accent:
            accent_folder = os.path.join(folder_path, accent)
            os.makedirs(accent_folder, exist_ok=True)

            src = os.path.join(folder_path, filename)
            dst = os.path.join(accent_folder, filename)
            shutil.move(src, dst)
            print(f"Moved {filename} → {accent}/")
        else:
            print(f"Skipped: {filename} (no matching wav in metadata)")

def organize_by_gender(folder_path: str, metadata_df: pd.DataFrame):
    file_to_gender = metadata_df.set_index("wav")["Examinee_gender"].to_dict()

    for filename in os.listdir(folder_path):
        # Only process .wav and .txt files
        if not (filename.endswith(".wav") or filename.endswith(".txt")):
            continue

        # Check if there's a .wav file in metadata that matches this file (or its base name)
        base_name = filename.rsplit(".", 1)[0]
        wav_name = base_name + ".wav"

        gender = file_to_gender.get(wav_name)
        if gender:
            gender_folder = os.path.join(folder_path, gender)
            os.makedirs(gender_folder, exist_ok=True)

            src = os.path.join(folder_path, filename)
            dst = os.path.join(gender_folder, filename)
            shutil.move(src, dst)
            print(f"Moved {filename} → {gender}/")
        else:
            print(f"Skipped: {filename} (no matching wav in metadata)")


for directory in os.listdir(folder_path):
    organize_by_gender(os.path.join(folder_path, directory), df)


