import pandas as pd
import os

def clean_dataset(input_file_path, output_file_path):
    """
    Automated Data Cleaning Pipeline:
    - Strips whitespace & standardizes text cases
    - Parses and standardizes date formats
    - Handles missing currency values
    - Splits compound columns
    - Removes exact duplicates
    """
    if not os.path.exists(input_file_path):
        print(f"Error: The file {input_file_path} was not found.")
        return

    print(f"Loading raw dataset from {input_file_path}...")
    df = pd.read_csv(input_file_path, engine='python')

    # 1. Clean Customer Names
    if 'Customer_Name' in df.columns:
        df['Customer_Name'] = df['Customer_Name'].astype(str).str.strip().str.title()

    # 2. Standardize Dates
    if 'Join_Date' in df.columns:
        df['Join_Date'] = pd.to_datetime(df['Join_Date'], errors='coerce').dt.strftime('%Y-%m-%d')

    # 3. Clean Currency and Numerical Values
    if 'Amount_USD' in df.columns:
        df['Amount_USD'] = (
            df['Amount_USD']
            .astype(str)
            .str.replace('$', '', regex=False)
            .str.replace(',', '', regex=False)
        )
        df['Amount_USD'] = pd.to_numeric(df['Amount_USD'], errors='coerce').fillna(0.0)

    # 4. Split Compound Columns if present (e.g., City_Status)
    if 'City_Status' in df.columns:
        df[['City', 'Status']] = df['City_Status'].str.split('_', expand=True)
        df['City'] = df['City'].str.strip().str.title()
        df['Status'] = df['Status'].str.strip().str.upper()
        df = df.drop(columns=['City_Status'])

    # 5. Remove Exact Duplicates
    initial_row_count = len(df)
    df = df.drop_duplicates()
    removed_count = initial_row_count - len(df)

    # 6. Export Clean Data
    df.to_csv(output_file_path, index=False)
    print(f"Success! Cleaned data saved to {output_file_path}.")
    print(f"Removed {removed_count} duplicate rows. Total valid records: {len(df)}")

if __name__ == "__main__":
    input_path = "raw_data.csv"
    output_path = "client_ready_output.csv"
    clean_dataset(input_path, output_path)
