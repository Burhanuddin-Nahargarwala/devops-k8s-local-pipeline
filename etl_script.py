import requests
import pandas as pd
import os

print("Starting ETL process...")

# --- EXTRACT ---
# Fetching data from a public API (JSONPlaceholder)
API_URL = "https://jsonplaceholder.typicode.com/users"
print(f"Extracting data from {API_URL}")
response = requests.get(API_URL)
data = response.json()

# --- TRANSFORM ---
# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)

# Perform a simple transformation: select specific columns and rename them
print("Transforming data...")
transformed_df = df[['id', 'name', 'username', 'email', 'company']]
transformed_df = transformed_df.rename(columns={
    'id': 'user_id',
    'name': 'full_name'
})
# Extract the company name from the nested dictionary
transformed_df['company_name'] = transformed_df['company'].apply(lambda c: c['name'])
transformed_df = transformed_df.drop(columns=['company'])


# --- LOAD ---
# Define the output path. We will mount a volume here in Kubernetes.
OUTPUT_DIR = "/app/output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

output_path = os.path.join(OUTPUT_DIR, "processed_users.csv")
print(f"Loading data to {output_path}")

# Save the transformed data to a CSV file
transformed_df.to_csv(output_path, index=False)

print("ETL process complete!")