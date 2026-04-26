import pandas as pd

df1 = pd.read_csv("final_datasets.csv")
df2 = pd.read_csv("human_mixed_dataset.csv")

df = pd.concat([df1, df2])
df = df.drop_duplicates(subset=["text"])

print(df.shape)
print(df["final_label"].value_counts())

# Step 1: lowercase everything
df["final_label"] = df["final_label"].str.lower()

# Step 2: map all variations to clean labels
def clean_label(label):
    if "delusional" in label:
        return "delusional"
    elif "realistic" in label:
        return "realistic"
    else:
        return None  # remove garbage labels

df["final_label"] = df["final_label"].apply(clean_label)

# Step 3: drop unwanted rows
df = df.dropna(subset=["final_label"])

# Step 4: check again
print(df["final_label"].value_counts())
df.to_csv("final_cleaned_dataset.csv", index=False)
df_check = pd.read_csv("final_cleaned_dataset.csv")
print(df_check["final_label"].value_counts())