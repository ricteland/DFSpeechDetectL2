import os

# Path to your main folder
base_path = r'C:\Users\Usuario\Desktop\TUE\BEP 2025\data\BEP-L2-BonaFide'
prompt_set = set()

# Walk through all subdirectories
for root, dirs, files in os.walk(base_path):
    if 'transcripts' in root:
        print(f'Processing {root}...')
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    line = f.read().strip()
                    if line:
                        prompt_set.add(line)

# Save all unique prompts to a file
with open('prompt_bank.txt', 'w', encoding='utf-8') as f:
    for prompt in sorted(prompt_set):
        f.write(prompt + '\n')

print(f"Extracted {len(prompt_set)} unique prompts to 'prompt_bank.txt'")
