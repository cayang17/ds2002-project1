import pandas as pd
import requests
import sqlite3
import os

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# Source 1 (github user)
# replace with whatever username
def fetch_github_data(user="torvalds"):
    print(f"Fetching GitHub data for user: {user}")
    url = f"https://api.github.com/users/{user}/repos"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        repos = [{
            "name": repo["name"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "created_at": repo["created_at"]
        } for repo in data]
        df = pd.DataFrame(repos)
        df.to_csv("output/github_data.csv", index=False)
        return df
    except Exception as e:
        print("Error fetching GitHub data:", e)
        return pd.DataFrame()

# Source 2 (local csv file)
# replace with path of your csv
def load_ev_data(path="data/Electric_Vehicle_Population.csv"):
    try:
        df = pd.read_csv(path)
        # Drop and add some columns
        df = df.drop(columns=["VIN (1-10)", "DOL Vehicle ID"], errors="ignore")
        df["EV Type"] = df["Electric Vehicle Type"].fillna("Unknown")
        df.to_csv("output/ev_data_transformed.csv", index=False)
        return df
    except Exception as e:
        print("Error loading EV data:", e)
        return pd.DataFrame()

# merge and analyze
def merge_and_analyze(github_df, ev_df):
    # Example merge using dummy column (not necessary unless common key exists)
    merged_df = pd.concat([github_df.reset_index(drop=True), ev_df.reset_index(drop=True)], axis=1)
    merged_df.to_csv("output/merged_data.csv", index=False)
    return merged_df

# store in SQLite db
def save_to_sql(df, table_name, db_path="output/etl_data.db"):
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        print(f"Data stored in SQLite table: {table_name}")
    except Exception as e:
        print("Error saving to SQL:", e)

# summary
def generate_summary(original, name):
    summary = f"=== {name} Summary ===\nRows: {original.shape[0]}, Columns: {original.shape[1]}\n"
    return summary

# main pipeline
def main():
    github_df = fetch_github_data("torvalds")
    ev_df = load_ev_data()

    with open("output/etl_summary.txt", "w") as f:
        f.write(generate_summary(github_df, "GitHub API Data"))
        f.write(generate_summary(ev_df, "EV CSV Data"))

    merged_df = merge_and_analyze(github_df, ev_df)
    save_to_sql(merged_df, "merged_data")

if __name__ == "__main__":
    main()
