import os
import pandas as pd


def balance_dataset(input_csv, output_csv, target_clips=650):
    # Load the full dataset
    full_df = pd.read_csv(input_csv)

    # Select only the necessary columns for grouping
    grouping_df = full_df[['wav', 'Examinee_gender', 'Accent']]

    # Resample each (gender, accent) group
    balanced_dfs = []

    for (gender, accent), group in grouping_df.groupby(['Examinee_gender', 'Accent']):
        if len(group) >= target_clips:
            sampled_group = group.sample(n=target_clips, random_state=42)
        else:
            sampled_group = group.sample(n=target_clips, replace=True, random_state=42)

        # Now get the full corresponding rows
        full_sampled_group = full_df.loc[sampled_group.index]
        balanced_dfs.append(full_sampled_group)

    # Combine everything into a single dataframe
    balanced_df = pd.concat(balanced_dfs).reset_index(drop=True)

    # Save the balanced dataset
    balanced_df.to_csv(output_csv, index=False)

    print(f"Saved balanced dataset with {len(balanced_df)} samples to {output_csv}!")

    return balanced_df


def move_selected_samples(balanced_df, clips_folder):
    os.makedirs(f"{clips_folder}/balanced", exist_ok=True)
    for index, row in balanced_df.iterrows():
        filename = row['wav']
        base_filename = os.path.splitext(filename)[0]

        source_wav = f"{clips_folder}/{filename}"
        destination_wav = f"{clips_folder}/balanced/{filename}"

        source_txt = f"{clips_folder}/{base_filename}.txt"
        destination_txt = f"{clips_folder}/balanced/{base_filename}.txt"

        if os.path.exists(source_wav):
            os.rename(source_wav, destination_wav)
        if os.path.exists(source_txt):
            os.rename(source_txt, destination_txt)


if __name__ == "__main__":
    input_csv = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS merged.csv"
    output_csv = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS merged balanced.csv"
    clips_folder = r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS clips"

    balanced_df = balance_dataset(input_csv, output_csv, target_clips=650)
    move_selected_samples(balanced_df, clips_folder)