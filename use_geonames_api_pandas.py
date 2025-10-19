import pandas as pd
import requests
import os

# --- Configuration ---
GEONAMES_USERNAME = 'GEONAMES USERNAME HERE'  # Replace with your GeoNames username
INPUT_CSV = '/path/to/data/EM_geonames_clean.csv'
base, ext = os.path.splitext(INPUT_CSV)
OUTPUT_CSV = f"{base}_coord{ext}"

# --- Function to query GeoNames API ---
def get_geonames_data(place_names):
    """Try each candidate name in order and return the first successful match.

    Returns: (matched_query_name, geonameId, lat, lng, requests_made)
    """
    requests_made = 0
    for place_name in place_names:
        if not place_name:
            continue
        url = 'http://api.geonames.org/searchJSON'
        params = {
            'q': place_name,
            'maxRows': 1,
            'username': GEONAMES_USERNAME
        }
        requests_made += 1
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('totalResultsCount', 0) > 0:
                geoname = data['geonames'][0]
                return place_name, geoname.get('geonameId'), geoname.get('lat'), geoname.get('lng'), requests_made
    return None, None, None, None, requests_made

# --- Load data ---
# Read tab-separated CSV, ignoring completely empty lines
df = pd.read_csv(INPUT_CSV, sep='\t', comment='#').dropna(how='all')

# Add output columns
df['geoname'] = None
df['geonameId'] = None
df['latitude'] = None
df['longitude'] = None

# --- Process each row ---
processed_rows = 0
total_api_requests = 0
for idx, row in df.iterrows():
    # Collect non-empty candidate place names
    place_names = [str(val).strip() for val in row if pd.notna(val) and str(val).strip()]
    
    # Query GeoNames
    matched_name, geoname_id, lat, lng, reqs = get_geonames_data(place_names)
    total_api_requests += reqs
    
    # Store results
    df.at[idx, 'geoname'] = matched_name
    df.at[idx, 'geonameId'] = geoname_id
    df.at[idx, 'latitude'] = lat
    df.at[idx, 'longitude'] = lng

    # Progress logging after every 100 processed rows
    processed_rows += 1
    if processed_rows % 100 == 0:
        print(f"Processed {processed_rows} rows; API requests so far: {total_api_requests}")

# --- Save updated data ---
# Ensure 'geoname' is the first column in the output
cols = ['geoname'] + [c for c in df.columns if c != 'geoname']
df[cols].to_csv(OUTPUT_CSV, sep='\t', index=False)
print(f"✅ Done! Results written to {OUTPUT_CSV}")
print(f"Total rows processed: {processed_rows}; total API requests made: {total_api_requests}")