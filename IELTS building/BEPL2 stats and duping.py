import os
import matplotlib.pyplot as plt
import soundfile as sf
import pandas as pd
import shutil
from collections import defaultdict

def bepl2_duration_plot(dataset_path):
    speaker_wav_counts = {}
    speaker_durations = {}

    # Loop over each speaker
    for speaker in os.listdir(dataset_path):
        speaker_path = os.path.join(dataset_path, speaker)
        wav_path = os.path.join(speaker_path, 'wav')

        if os.path.isdir(wav_path):
            print(f"Processing speaker: {speaker}")
            wav_files = [f for f in os.listdir(wav_path) if f.endswith('.wav')]
            total_duration = 0.0
            for wav_file in wav_files:
                filepath = os.path.join(wav_path, wav_file)
                try:
                    with sf.SoundFile(filepath) as f:
                        total_duration += len(f) / f.samplerate
                except RuntimeError:
                    print(f"Could not read {filepath}, skipping.")

            speaker_wav_counts[speaker] = len(wav_files)
            speaker_durations[speaker] = total_duration

    # Plotting
    fig, ax1 = plt.subplots(figsize=(14, 6))

    speakers = list(speaker_wav_counts.keys())
    counts = [speaker_wav_counts[s] for s in speakers]
    durations = [speaker_durations[s] for s in speakers]

    ax1.bar(speakers, counts, alpha=0.6, label='# WAV files')
    ax1.set_ylabel('Number of WAV files')
    ax1.set_xlabel('Speaker ID')
    ax1.tick_params(axis='x', rotation=90)

    # Twin axis for durations
    ax2 = ax1.twinx()
    ax2.plot(speakers, durations, 'r.-', label='Total duration (sec)')
    ax2.set_ylabel('Total Duration (seconds)')

    fig.suptitle('Per-Speaker WAV Count and Total Duration')
    fig.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


def duplicate_oversampled_wavs(data_path, dataset_root, filename_col='wav'):
    df = pd.read_csv(data_path)
    filename_counts = df[filename_col].value_counts()
    augmented_rows = []

    for fname, count in filename_counts.items():
        found_path = None
        for root, _, files in os.walk(dataset_root):
            if fname in files:
                found_path = os.path.join(root, fname)
                break

        if not found_path:
            print(f"[WARNING] File '{fname}' not found. Skipping.")
            continue

        dir_path = os.path.dirname(found_path)
        name, ext = os.path.splitext(fname)

        augmented_rows.append({filename_col: fname})

        for i in range(2, count + 1):
            new_fname = f"{name}_{i}{ext}"
            new_path = os.path.join(dir_path, new_fname)
            shutil.copy2(found_path, new_path)
            augmented_rows.append({filename_col: new_fname})
            print(f"Copied {found_path} → {new_path}")

    return pd.DataFrame(augmented_rows)


#duplicate_oversampled_wavs(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS merged balanced.csv", r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\BEP-L2-BonaFide")
bepl2_duration_plot(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\BEP-L2-BonaFide")