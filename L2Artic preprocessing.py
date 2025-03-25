import pandas as pd
import os
from downsampler import downsample_audio

metadata = {
    'ABA': ('M', 'Arabic'),
    'SKA': ('F', 'Arabic'),
    'YBAA': ('M', 'Arabic'),
    'ZHAA': ('F', 'Arabic'),
    'BWC': ('M', 'Chinese'),
    'LXC': ('F', 'Chinese'),
    'NCC': ('F', 'Chinese'),
    'TXHC': ('M', 'Chinese'),
    'ASI': ('M', 'Hindi'),
    'RRBI': ('M', 'Hindi'),
    'SVBI': ('F', 'Hindi'),
    'TNI': ('F', 'Hindi'),
    'HJK': ('F', 'Korean'),
    'HKK': ('M', 'Korean'),
    'YDCK': ('F', 'Korean'),
    'YKWK': ('M', 'Korean'),
    'EBVS': ('M', 'Spanish'),
    'ERMS': ('M', 'Spanish'),
    'MBMPS': ('F', 'Spanish'),
    'NJS': ('F', 'Spanish'),
    'HQTV': ('M', 'Vietnamese'),
    'PNV': ('F', 'Vietnamese'),
    'THV': ('F', 'Vietnamese'),
    'TLV': ('M', 'Vietnamese'),
}

data = []
root_dir = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\l2arctic_release_v5.0"

def create_csv_l2arctic(metadata, root_dir):
    for speaker, (gender, lang) in metadata.items():
        accent = f"{'Male' if gender == 'M' else 'Female'} {lang}"
        speaker_path_prev = os.path.join(root_dir, speaker)
        speaker_path = os.path.join(speaker_path_prev, speaker)
        wav_path = os.path.join(speaker_path, 'wav')
        txt_path = os.path.join(speaker_path, 'transcript')
        print(f"Processing {speaker}...")
        if not os.path.isdir(wav_path) or not os.path.isdir(txt_path):
            print(f"Skipping {speaker}: missing folders.")
            continue

        for filename in os.listdir(wav_path):
            if filename.endswith('.wav'):
                base = os.path.splitext(filename)[0]
                wav_file = f"{speaker}\\{speaker}\\wav\\{filename}"
                txt_file = os.path.join(txt_path, f"{base}.txt")

                if not os.path.exists(txt_file):
                    print(f"Transcript missing for {wav_file}")
                    continue

                with open(txt_file, 'r', encoding='utf-8') as f:
                    transcript = f.read().strip()

                data.append({
                    'wav': wav_file,
                    'transcript': transcript,
                    'accent': accent
                })

def downsample_l2arctic(root_dir):
    for speaker in os.listdir(root_dir):
        if speaker in metadata:
            print(f"Processing {speaker}...")
            input_dir_prev = os.path.join(root_dir, speaker)
            input_dir = os.path.join(input_dir_prev, speaker)
            wav_dir = os.path.join(input_dir, 'wav')
            downsample_audio(input_directory=wav_dir, output_directory=wav_dir, rate=24000)


# create_csv_l2arctic(metadata, root_dir)
# df = pd.DataFrame(data)
# df.to_csv(r'C:\Users\Usuario\Desktop\TUE\BEP 2025\data\l2arctic_release_v5.0\L2artic.csv', index=False)
# print("Dataset created with", len(df), "rows.")
#
# downsample_l2arctic(root_dir)

df = pd.read_csv(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\l2arctic_release_v5.0\L2artic.csv")
print(df["accent"].value_counts())
