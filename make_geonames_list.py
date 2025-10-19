import csv
import os
import re

file_path = '/path/to/data/EM_Entities.csv'

csv_file = file_path
geo_bez_list = []
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        # Assumption: the column containing semicolon-separated values is named 'Geo. Bez.'
        # Adjust the field name below if your CSV uses a different header.
        value = row.get('Geo. Bez.')
        if not value:
            continue

        # Split on semicolons and add unique, trimmed parts
        # For each part, if a colon exists, use only the value (second part after first colon);
        # otherwise use the whole trimmed part.
        for part in value.split(';'):
            part = part.strip()
            if not part:
                continue

            if ':' in part:
                _, item = part.split(':', 1)
            else:
                item = part

            item = item.strip()
            # Remove trailing editorial marker " [...]" if present
            item = re.sub(r"\s*\[\.\.\.\]\s*$", "", item)
            # Remove uncertainty marker " (?)" if present
            item = item.replace(" (?)", "")
            # Also remove a trailing "(?)" without preceding space
            item = re.sub(r"\s*\(\?\)\s*$", "", item)
            # Normalize internal excessive spaces after removals
            item = re.sub(r"\s{2,}", " ", item).strip()
            



            if item and item not in geo_bez_list:
                geo_bez_list.append(item)

# Sort once and reuse
sorted_items = sorted(geo_bez_list)

# Save to CSV next to the input file
output_csv = os.path.join(os.path.dirname(file_path), 'extracted_single_geonames.csv')
with open(output_csv, 'w', newline='', encoding='utf-8') as out_f:
    writer = csv.writer(out_f)
    writer.writerow(['geoname'])
    for e in sorted_items:
        writer.writerow([e])

# Print to stdout as before
for e in sorted_items:
    print(e)
print(f"Total unique geographic entries: {len(geo_bez_list)}")
print(f"Saved CSV to: {output_csv}")

