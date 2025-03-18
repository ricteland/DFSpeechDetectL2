import os


def rename_audio_files(folder_path, prefix="IELTS"):
    # Get all audio files in the directory
    audio_files = [f for f in os.listdir(folder_path) if
                   f.lower().endswith(('.mp3', '.wav'))]

    # Sort files to maintain order
    audio_files.sort(key=lambda f: os.path.getctime(os.path.join(folder_path, f)))

    # Rename files with format IELTS001, IELTS002, ...
    for index, file_name in enumerate(audio_files, start=90):
        file_extension = os.path.splitext(file_name)[1]  # Get file extension
        new_name = f"{prefix}{index:03d}{file_extension}"  # Format with leading zeros
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {file_name} -> {new_name}")




