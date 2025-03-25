import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt

df_ielts = pd.read_csv(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS data.csv")
filenames = os.listdir(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS clips")
df_names = pd.DataFrame(filenames, columns=["Filename"])

df_txt = df_names[df_names["Filename"].str.endswith(".txt")].reset_index(drop=True)
df_names = df_names[df_names["Filename"].str.endswith(".wav")].reset_index(drop=True)

df_ielts["VideoIndex"] = df_ielts["ID"].str.extract(r"IELTS(\d{3})").astype(int)

df_names["VideoIndex"] = df_names["Filename"].str.extract(r"IELTS(\d{3})_").astype(int)
df_names["Speaker"] = df_names["Filename"].str.extract(r"_(Examiner|Student)_segment_")
df_names["Segment"] = df_names["Filename"].str.extract(r"_segment_(\d+)").astype(int)
df_names["Filename"] = df_names["Filename"].str.slice(start=0, stop=-4)
df_txt["Filename"] = df_txt["Filename"].str.slice(start=0, stop=-4)
merged_df = pd.merge(df_ielts, df_names, on='VideoIndex', how='inner')


def create_speaker_id(row):
    max_id = df_ielts["Examinator_ID"].max().astype(int)
    if row["Speaker"] == "Examiner":
        return row["Examinator_ID"]
    else:
        return max_id + row["VideoIndex"]

merged_df["Speaker_ID"] = merged_df.apply(create_speaker_id, axis=1)


def add_text_column(base_dir, df_txt):
    texts = []
    for filename in df_txt['Filename']:
        if len(texts) % 1000 == 0:
            print(f"Processing file {len(texts)}/{len(df_txt)}")
        file_path = os.path.join(base_dir, filename + ".txt")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                line = f.readline().strip()  # Read first line
                texts.append(line)
        except FileNotFoundError:
            texts.append(None)  # or "", depending on your preference
            print(f"⚠️ File not found: {file_path}")
    df_txt['text'] = texts
    return df_txt

df_txt = add_text_column(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS clips", df_txt)
df_txt["VideoIndex"] = df_txt["Filename"].str.extract(r"IELTS(\d{3})_").astype(int)
df_txt["Segment"] = df_txt["Filename"].str.extract(r"_segment_(\d+)").astype(int)
df_txt["Speaker"] = df_txt["Filename"].str.extract(r"_(Examiner|Student)_segment_")

final_df = pd.merge(merged_df, df_txt, on=['VideoIndex', 'Segment', 'Speaker'], how='inner')
final_df["wav"] = final_df["Filename_x"] + ".wav"

print(len(final_df))
print(final_df.columns)

final_df['Accent'] = np.where(
    final_df['Speaker'] == 'Examiner',
    'Native',
    final_df['Examinee_accent']
)
final_df = final_df.drop(columns=["ID", "Examinator_ID", "Examinator_age", "Channel",
                                  "Filename_x", "Filename_y", "Examinee_accent"])

final_df = final_df.rename(columns={"text": "Transcript"})

final_df.to_csv(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS merged.csv", index=False)

