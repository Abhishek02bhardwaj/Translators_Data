import requests
import re
import csv


def get_user_titles_with_babel_from_csv(csv_file):
    titles = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            titles.append("User:" + row[1])  # Assuming usernames are in the second column
    return titles[:30]  # Limit titles to 30


def find_babel_languages(title):
    url = "https://en.wikipedia.org/w/index.php"
    params = {
        "title": title,
        "action": "raw"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        content = response.text
        babel_templates = re.findall(r"\{\{(?:#)?babel(?:[^}]*?)[^\w}](.*?)\}\}", content, re.IGNORECASE) or re.findall(r"\{\{(?:#)?Babel(?:[^}]*?)[^\w}](.*?)\}\}", content)
        if babel_templates:
            language_claims = []
            for template in babel_templates:
                languages = template.split("|")[0:]
                language_claims.extend(languages)
            return title, language_claims
    return title, []


# CSV file path
csv_file = 'usernames.csv'

# Fetch user titles with Babel templates from CSV
titles = get_user_titles_with_babel_from_csv(csv_file)

# Process Babel languages for each user
results = [find_babel_languages(title) for title in titles]

# Output CSV file path
output_csv_file = 'user_languages.csv'

# Filter results to include only usernames with languages
filtered_results = [(title, languages) for title, languages in results if languages]

# Write results to the output CSV file
with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['username', 'Languages'])
    writer.writerows(filtered_results)
