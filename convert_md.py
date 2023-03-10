import os
import re
import csv
import json

input_md_file = "README.md"
output_csv_filename = "licenses.csv"
output_json_filename = "licenses.json"

# Construct the output file paths next to the script
script_path = os.path.dirname(os.path.abspath(__file__))
output_csv_file_path = os.path.join(script_path, output_csv_filename)
output_json_file_path = os.path.join(script_path, output_json_filename)

# Initialize a list to hold the table rows as dictionaries
rows = []
# Open the output file for writing
# Open the input file for reading
with open(input_md_file, mode="r") as input_file:
    header_processed = False
    for line in input_file:
        # Process each line
        if line.startswith("|") and not line.strip().startswith("|-"):
            split_line = [entry.strip() for entry in line.split("|") if entry.strip()]

            # Extract the link from the last field
            link_pattern = r"\[.*\]\((.*)\)"
            match = re.search(link_pattern, split_line[-1])
            if match:
                link = match.group(1)
            else:
                link = ""

            # Construct a dictionary for the row
            if not header_processed:
                header_processed = True
                header_names = split_line
            else:
                row = {}
                for i, key in enumerate(header_names):
                    row[key] = split_line[i]
                row["Link"] = link
                # Add the dictionary to the list
                rows.append(row)

# Open the output CSV file for writing
with open(output_csv_file_path, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    # Write the headers
    writer.writerow(header_names)

    # Write the data rows
    for row in rows:
        writer.writerow(row.values())

# Open the output JSON file for writing
with open(output_json_file_path, mode="w") as json_file:
    # Convert the list of dictionaries to a JSON string
    json_data = json.dumps(rows, indent=4)

    # Write the JSON string to the file
    json_file.write(json_data)
