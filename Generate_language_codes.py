import requests
import re
import csv

url = "https://en.wikipedia.org/w/index.php?title=List_of_Wikipedias&action=edit&section=9"
response = requests.get(url)
if response.status_code == 200:
    content = response.text

    # Extract language codes using regular expressions
    pattern = r"\{\{WP7\|([^\|\}]+)"
    language_codes = re.findall(pattern, content)

    # Generate six combinations for each language code
    combinations = []
    for code in language_codes:
        combinations.append(code)
        combinations.append(code + "-N")
        combinations.append(code + "-0")
        combinations.append(code + "-1")
        combinations.append(code + "-2")
        combinations.append(code + "-3")
        combinations.append(code + "-4")
        combinations.append(code + "-5")

    # Create a CSV file and write the language codes
    output_file = "language_codes.csv"
    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Language Code"])  # Write header row
        writer.writerows([[code] for code in combinations])

    print("CSV file created successfully:", output_file)
else:
    print("Failed to retrieve the Wikipedia page.")
