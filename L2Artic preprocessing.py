import pandas as pd
import os
from downsampler import downsample_audio
import shutil
from sklearn.model_selection import train_test_split

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


def create_xtts_metadata(wav_dir, transcript_dir, output_dir, eval_percentage=0.15, speaker_metadata=None):
    metadata = {"audio_file": [], "text": [], "speaker_name": []}
    os.makedirs(output_dir, exist_ok=True)

    for wav_file in os.listdir(wav_dir):
        if wav_file.endswith(".wav"):
            base = os.path.splitext(wav_file)[0]
            transcript_path = os.path.join(transcript_dir, f"{base}.txt")
            if not os.path.exists(transcript_path):
                print(f"Missing transcript for {wav_file}")
                continue

            with open(transcript_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()

            # Extract speaker from filename
            speaker_id = base.split("_")[0]

            if speaker_metadata and speaker_id not in speaker_metadata:
                print(f"Skipping {wav_file}: unknown speaker ID '{speaker_id}'")
                continue

            # Optional: Use gender/lang label instead of just ID
            speaker_label = f"{speaker_metadata[speaker_id][0]}_{speaker_metadata[speaker_id][1]}"

            metadata["audio_file"].append(f"wavs/{wav_file}")
            metadata["text"].append(text)
            metadata["speaker_name"].append(speaker_label)

    df = pd.DataFrame(metadata)
    df = df.sample(frac=1, random_state=42)  # shuffle

    # Split
    num_val = int(len(df) * eval_percentage)
    df_eval = df[:num_val].sort_values("audio_file")
    df_train = df[num_val:].sort_values("audio_file")

    df_train.to_csv(os.path.join(output_dir, "metadata_train.csv"), sep="|", index=False)
    df_eval.to_csv(os.path.join(output_dir, "metadata_eval.csv"), sep="|", index=False)

    print(f"✅ Created metadata_train.csv ({len(df_train)} samples)")
    print(f"✅ Created metadata_eval.csv ({len(df_eval)} samples)")
    return df_train, df_eval


def downsample_l2arctic(root_dir):
    for speaker in os.listdir(root_dir):
        if speaker in metadata:
            print(f"Processing {speaker}...")
            input_dir_prev = os.path.join(root_dir, speaker)
            input_dir = os.path.join(input_dir_prev, speaker)
            wav_dir = os.path.join(input_dir, 'wav')
            downsample_audio(input_directory=wav_dir, output_directory=wav_dir, rate=24000)


def move_wavs_l2(metadata, root_dir):
    wavs_dir = os.path.join(root_dir, 'wavs')
    os.makedirs(wavs_dir, exist_ok=True)

    for speaker in metadata:
        speaker_wav_dir = os.path.join(root_dir, speaker, speaker, 'wav')
        if not os.path.isdir(speaker_wav_dir):
            print(f"Skipping {speaker}: 'wav' folder not found.")
            continue

        for filename in os.listdir(speaker_wav_dir):
            if filename.endswith('.wav'):
                src_path = os.path.join(speaker_wav_dir, filename)
                new_filename = f"{speaker}_{filename}"
                dst_path = os.path.join(wavs_dir, new_filename)

                shutil.copy2(src_path, dst_path)
                print(f"Moved wav: {new_filename}")

def move_transcripts_l2(metadata, root_dir):
    txt_dir = os.path.join(root_dir, 'transcripts')
    os.makedirs(txt_dir, exist_ok=True)

    for speaker in metadata:
        speaker_txt_dir = os.path.join(root_dir, speaker, speaker, 'transcript')
        if not os.path.isdir(speaker_txt_dir):
            print(f"Skipping {speaker}: 'transcript' folder not found.")
            continue

        for filename in os.listdir(speaker_txt_dir):
            if filename.endswith('.txt'):
                src_path = os.path.join(speaker_txt_dir, filename)
                new_filename = f"{speaker}_{filename}"
                dst_path = os.path.join(txt_dir, new_filename)

                shutil.copy2(src_path, dst_path)
                print(f"Moved transcript: {new_filename}")


#  downsample_l2arctic(root_dir)

create_xtts_metadata(
    wav_dir=r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\l2arctic_release_v5.0\wavs",
    transcript_dir=r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\l2arctic_release_v5.0\transcripts",
    output_dir=r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\l2arctic_release_v5.0",
    eval_percentage=0.15,
    speaker_metadata=metadata
)
