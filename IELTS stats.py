import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import librosa
import os

df = pd.read_csv(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS merged.csv")


females_count = df["Examinee_gender"].value_counts()["F"]
males_count = df["Examinee_gender"].value_counts()["M"]
ratio_female_examinee = females_count / (females_count + males_count)


females_count = df["Examinator_gender"].value_counts()["F"]
males_count = df["Examinator_gender"].value_counts()["M"]
ratio_female_examinator = females_count / (females_count + males_count)


df["AccentStripped"] = df["Accent"].str.replace(" Accent", "", regex=False)

# Plot
df["AccentStripped"].value_counts().plot(kind="bar")
plt.xlabel("Accent")
plt.ylabel("Count")
plt.title("Distribution of Accents")
plt.tight_layout()
# plt.show()

df[df["Speaker_ID"] < 9]["Speaker_ID"].value_counts().plot(kind="bar")
plt.xlabel("Speaker_ID")
plt.ylabel("Count")
plt.title("Distribution of Examinator IDs")
# plt.show()

grouped = df.groupby(["Examinee_gender", "AccentStripped"]).size().reset_index(name="count")

# Plot using seaborn
plt.figure(figsize=(12, 6))
gender_palette = {"F": "hotpink", "M": "dodgerblue"}
sns.barplot(data=grouped, x="AccentStripped", y="count", hue="Examinee_gender", palette=gender_palette)

plt.xlabel("Accent")
plt.ylabel("Number of Examinees")
plt.title("Accent Distribution by Gender")
plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()


for accent in df["AccentStripped"].unique():
    plt.hist(df[df["AccentStripped"] == accent]["Score"], density=True, bins=100, alpha=0.5, label=accent)
    plt.title(f"Score Distribution for {accent}")
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.tight_layout()
    # plt.show()


def get_duration(filepath):
    path = os.path.join(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS clips", filepath)
    try:
        duration = librosa.get_duration(path=path)
        return duration/60
    except Exception as e:
        print(f"Error with {filepath}: {e}")
        return None

df["Duration"] = df["wav"].apply(get_duration)

def get_proficiency(score):
    if int(score) <= 4:
        return 'Low'
    elif 5 <= int(score) <= 7:
        return 'Medium'
    else:
        return 'High'

df['Proficiency'] = df['Score'].apply(get_proficiency)


durations = df.groupby(["AccentStripped", "Examinee_gender", "Proficiency"])["Duration"].sum().reset_index()

print(df[(df["AccentStripped"] == "Native") & (df["Proficiency"] == "Low")])
