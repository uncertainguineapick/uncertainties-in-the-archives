import pandas as pd

file_path = '/path/to/data/EM_Entities.csv'

# Read the CSV file
df = pd.read_csv(file_path, sep=';')

# Function to parse the Geo. Bez. column
def parse_geo_bez(geo_bez_string):
    """Parse semicolon-separated key-value pairs from Geo. Bez. column."""
    result = {}
    
    if pd.isna(geo_bez_string):
        return result
    
    # Split by semicolon
    parts = str(geo_bez_string).split(';')
    
    for part in parts:
        part = part.strip()
        if ':' in part:
            # Split at the first colon
            key, value = part.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # If key already exists, combine values (handle multiple same keys)
            if key in result:
                if isinstance(result[key], list):
                    result[key].append(value)
                else:
                    result[key] = [result[key], value]
            else:
                result[key] = value
        else:
            # Handle parts without colon - add to special key
            if part:  # Only add non-empty parts
                key = 'without_details'
                if key in result:
                    if isinstance(result[key], list):
                        result[key].append(part)
                    else:
                        result[key] = [result[key], part]
                else:
                    result[key] = part
    
    return result

# Apply the parsing function to create new columns
geo_data = df['Geo. Bez.'].apply(parse_geo_bez)

# Get all unique keys to create columns
all_keys = set()
for data in geo_data:
    all_keys.update(data.keys())

print("Found geographic keys:", sorted(all_keys))

# Create new columns for each key
for key in all_keys:
    df[f'Geo_{key}'] = geo_data.apply(lambda x: x.get(key, None))

# Display the results
print(f"\nOriginal shape: {df.shape}")
print(f"New columns added: {len(all_keys)}")
print(f"New shape: {df.shape}")

print("\nSample of restructured data:")
geo_columns = [col for col in df.columns if col.startswith('Geo_')]
print(df[['Name', 'Geo. Bez.'] + geo_columns].head())

print("\nValue counts for each new geographic column:")
for col in sorted(geo_columns):
    non_null_count = df[col].notna().sum()
    print(f"{col}: {non_null_count} non-null values")

# Save the restructured dataframe
output_path = file_path.replace('.csv', '_restructured.csv')
df.to_csv(output_path, sep=';', index=False)
print(f"\nRestructured data saved to: {output_path}")








