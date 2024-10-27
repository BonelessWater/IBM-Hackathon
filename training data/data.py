import pandas as pd
import os

def divide_and_clean_csv(input_file):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(input_file)
    
    # Get the first 10 unique IDs
    unique_ids = data['ID'].unique()[:10]
    
    # Create an output folder if it doesn't exist
    os.makedirs('output_csvs', exist_ok=True)
    
    # Loop through the first 10 IDs and generate separate CSVs
    for uid in unique_ids:
        # Filter the data for the current ID
        filtered_data = data[data['ID'] == uid]
        
        # Remove the last row and capture it
        last_row = filtered_data.iloc[-1]
        filtered_data = filtered_data.iloc[:-1]
        
        # Print the deleted row and the corresponding CSV file
        print(f"Deleted row from ID {uid}:\n{last_row}\n")
        
        # Save the remaining data to a new CSV file
        output_file = f'output_csvs/{uid}.csv'
        filtered_data.to_csv(output_file, index=False)

# Example usage
divide_and_clean_csv('your_input_file.csv')
