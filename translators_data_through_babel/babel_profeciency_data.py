import csv
import json


def filter_languages(first_csv_file, second_csv_file, output_file):
    # Step 1: Filter and drop rows with disallowed languages

    # Read the language codes from the second CSV and store them in a set
    language_codes = set()
    with open(second_csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            language_codes.add(row[0])

    # Open the first CSV file for reading
    with open(first_csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Create a list to store filtered rows
        filtered_rows = []

        # Iterate over the rows in the first CSV
        for row in reader:
            language_used = row['language_used']

            # Check if the language_used is in the set of language codes
            if language_used in language_codes:
                filtered_rows.append(row)

    # Step 2: Format rows into desired output format

        # Define the column names for input and output CSV files
        input_username_column = 'username'
        input_language_column = 'language_used'
        input_level_column = 'language_level'
        output_username_column = 'username'
        output_language_column = 'language'

    # Group filtered rows by username and merge language entries
    merged_rows = {}
    for row in filtered_rows:
        username = row[input_username_column]
        language = f"{row[input_language_column]}-{row[input_level_column]}"

        if username not in merged_rows:
            merged_rows[username] = [language]
        else:
            merged_rows[username].append(language)

    # Transform the grouped data into output rows
    output_rows = []
    for username, languages in merged_rows.items():
        formatted_username = f"{username}"
        formatted_languages = json.dumps(languages)
        output_rows.append({output_username_column: formatted_username, output_language_column: formatted_languages})

    # Write the output CSV file
    fieldnames = [output_username_column, output_language_column]
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print("Output CSV file created successfully:", output_file)


# Provide the input file paths and output file path
first_csv_file = 'raw/knwiki_language_profeciency_babel_raw.csv'
second_csv_file = 'language_codes.csv'
output_file = 'result/knwiki_language_profeciency_babel.csv'

# Call the function to filter and format the data
filter_languages(first_csv_file, second_csv_file, output_file)
