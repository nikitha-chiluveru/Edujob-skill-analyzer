import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# -----------------------------
# STEP 1: Read all CSV & XLSX files
# -----------------------------

data_folder = "data"
all_dataframes = []

for file in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file)
    
    try:
        if file.endswith(".csv"):
            df = pd.read_csv(file_path)
            df["College"] = file.replace(".csv", "")
            all_dataframes.append(df)

        elif file.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            df["College"] = file.replace(".xlsx", "")
            all_dataframes.append(df)

    except Exception as e:
        print(f"❌ Error reading {file}: {e}")

# -----------------------------
# STEP 2: Merge all files
# -----------------------------

merged_df = pd.concat(all_dataframes, ignore_index=True)

print("✅ Total rows after merging:", len(merged_df))

# Save merged file
merged_df.to_csv("merged_colleges.csv", index=False)
print("✅ Merged file saved as merged_colleges.csv")

# -----------------------------
# STEP 3: Extract Topics Column
# -----------------------------

column_name = "Topics Covered"

if column_name not in merged_df.columns:
    print("❌ 'Topics Covered' column not found!")
    print("Available columns:", merged_df.columns)
    exit()

merged_df[column_name] = merged_df[column_name].fillna("")

# -----------------------------
# STEP 4: Apply TF-IDF
# -----------------------------

vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=1000
)

X = vectorizer.fit_transform(merged_df[column_name])

print("✅ TF-IDF Vector Shape:", X.shape)

# -----------------------------
# STEP 5: Apply K-Means
# -----------------------------

k = 5  # You can change cluster count

kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
merged_df["Cluster"] = kmeans.fit_predict(X)

print("✅ Clustering completed!")

# -----------------------------
# STEP 6: Save Final Output
# -----------------------------

merged_df.to_csv("clustered_output.csv", index=False)
print("✅ Clustered file saved as clustered_output.csv")

# -----------------------------
# STEP 7: Show Top Words Per Cluster
# -----------------------------

terms = vectorizer.get_feature_names_out()

print("\n================ CLUSTER INTERPRETATION ================")

for i in range(k):
    print(f"\n🔹 Cluster {i} Top Words:")
    center = kmeans.cluster_centers_[i]
    top_indices = center.argsort()[-10:][::-1]
    
    for index in top_indices:
        print(terms[index])

# -----------------------------
# STEP 8: Show Cluster Distribution by College
# -----------------------------

print("\n================ COLLEGE vs CLUSTER DISTRIBUTION ================")

distribution = merged_df.groupby(["College", "Cluster"]).size()
print(distribution)