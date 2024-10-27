import pandas as pd
import os
import json

def create_master_json(input_file, output_file='master_short.json'):
    # Load the input CSV into a DataFrame
    data = pd.read_csv(input_file)

    # Get the first 10 unique IDs
    unique_ids = data['ID'].unique()[:50]

    # Initialize the master JSON structure
    master_json = []

    # Loop through the first 10 IDs
    for uid in unique_ids:
        # Filter the data for the current ID
        filtered_data = data[data['ID'] == uid]

        # Remove the last row and capture its latitude and longitude
        last_row = filtered_data.iloc[-1]
        lat, lon = last_row['Latitude'], last_row['Longitude']

        # Print the latitude and longitude of the deleted row
        print(f"Deleted location from ID {uid}: Latitude: {lat}, Longitude: {lon}")

        # Remove the last row from the DataFrame
        filtered_data = filtered_data.iloc[:-1]

        # Prepare the entry for the master JSON
        entry = {
            "id": str(uid)[-3:],  # Keep only the last 3 digits of the ID
            "input": filtered_data[['Latitude', 'Longitude']].to_dict(orient='records'),
            "output": {
                "Latitude": lat,
                "Longitude": lon
            }
        }

        # Append the entry to the master JSON list
        master_json.append(entry)

    # Save the master JSON to a file
    with open(output_file, 'w') as f:
        json.dump(master_json, f, indent=4)

# Example usage
create_master_json('atlantic.csv')
