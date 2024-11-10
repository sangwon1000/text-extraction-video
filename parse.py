import json
import csv
from datetime import datetime
import pandas as pd

def parse_json_to_csv():
    # Read the JSON file
    with open('content_analysis.json', 'r') as file:
        data = json.load(file)
    
    # Prepare data for CSV
    restaurants = []
    for timestamp, content in data.items():
        # Content is already a dictionary, no need to parse it again
        if isinstance(content, str):
            try:
                content_data = json.loads(content)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON at timestamp {timestamp}")
                continue
        else:
            content_data = content
            
        if 'restaurants' in content_data:
            restaurants.extend(content_data['restaurants'])
    
    # Write to CSV
    # with open('restaurants_list.csv', 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     # Write header
    #     writer.writerow(['Restaurant Name', 'Description'])
    #     # Write data
    #     for restaurant in restaurants:
    #         writer.writerow([restaurant['name'], restaurant['description']])

    # print("CSV file has been created successfully!")
    
    # Create DataFrame
    df = pd.DataFrame(restaurants)
    print("\nDataFrame of restaurants:")
    print(df)
    return df

if __name__ == "__main__":
    df = parse_json_to_csv()
    # Convert restaurant names to lowercase
    df['name'] = df['name'].str.lower()
    
    # Group by restaurant name and combine descriptions
    grouped_df = df.groupby('name').agg({
        'description': lambda x: ' | '.join(x.unique())
    }).reset_index()
    
    print("\nCombined restaurants with lowercase names:")
    print(grouped_df)
    
    # Save to CSV
    grouped_df.to_csv('restaurants_combined.csv', index=False)
    print("\nSaved combined results to restaurants_combined.csv")
