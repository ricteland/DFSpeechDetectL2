import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\Usuario\Desktop\TUE\BEP 2025\data\IELTS\IELTS data.csv")
df["Examinee_accent"] = df["Examinee_accent"].fillna("Native")


females_count = df["Examinee_gender"].value_counts()["F"]
males_count = df["Examinee_gender"].value_counts()["M"]
ratio_female_examinee = females_count / (females_count + males_count)
print("Ratio female examinee:", ratio_female_examinee)

females_count = df["Examinator_gender"].value_counts()["F"]
males_count = df["Examinator_gender"].value_counts()["M"]
ratio_female_examinator = females_count / (females_count + males_count)
print("Ratio female examinator:", ratio_female_examinator)

df["AccentStripped"] = df["Examinee_accent"].str.replace(" Accent", "", regex=False)

# Plot
df["AccentStripped"].value_counts().plot(kind="bar")
plt.xlabel("Accent")
plt.ylabel("Count")
plt.title("Distribution of Accents")
plt.tight_layout()
# plt.show()

df["Examinator_ID"].value_counts().plot(kind="bar")
plt.xlabel("Examinator ID")
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
plt.show()



