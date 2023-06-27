import requests
import re
import csv
import json


def get_allowed_languages_from_csv(csv_file):
    allowed_languages = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            allowed_languages.append(row[0])
    return allowed_languages


def get_user_titles_with_babel_from_csv(csv_file):
    titles = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            titles.append("User:" + row[1])  # Assuming usernames are in the second column
    return titles[0:]


def extract_language_codes(template_text):
    code_pattern = r"(?<=\|)([^\|\[\]]+)(?=\|)"
    languages = re.findall(code_pattern, template_text)
    first_element = re.search(r"^[^\|]+", template_text)
    last_element = re.search(r"[^\|]+$", template_text)
    if first_element:
        first_element = first_element.group()
        languages.append(re.sub(r"^\['", '', first_element))
    if last_element:
        last_element = last_element.group()
        last_element = re.sub(r"'\]$", '', last_element)
        if last_element:
            languages.append(last_element)
    return languages


def fetch_content(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.text
    return None


def parse_babel_templates(content, allowed_languages):
    babel_templates = re.findall(r"\{\{Babel((?:(?!\{\{Babel)[^{}])+)\}\}", content, re.IGNORECASE)
    language_claims = []
    if babel_templates:
        for babel_template in babel_templates:
            user_text = str(babel_template)
            user_languages = extract_language_codes(user_text)
            valid_user_languages = set()
            for lang in user_languages:
                lang = lang.strip()
                lang = lang.rstrip('\n')
                if lang in allowed_languages:
                    valid_user_languages.add(lang)
            language_claims.extend(valid_user_languages)
    return language_claims


def find_babel_languages(title, allowed_languages):
    url = "https://en.wikipedia.org/w/index.php"
    params = {
        "title": title,
        "action": "raw"
    }
    content = fetch_content(url, params)
    if content:
        language_claims = parse_babel_templates(content, allowed_languages)
        return title, language_claims
    return title, []


def create_user_language_csv(csv_file, output_file, output_file_no_lang):
    allowed_languages = get_allowed_languages_from_csv('language_codes.csv')
    titles = get_user_titles_with_babel_from_csv(csv_file)
    results = [find_babel_languages(title, allowed_languages) for title in titles]
    filtered_results = [(title, languages) for title, languages in results if languages]
    filtered_results_no_lang = [(title,) for title, languages in results if not languages]

    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "language"])

        for title, languages in filtered_results:
            language_string = json.dumps(languages, separators=(',', ':'))
            writer.writerow([title, language_string])

    with open(output_file_no_lang, 'w', encoding='utf-8', newline='') as file_no_lang:
        writer_no_lang = csv.writer(file_no_lang)
        writer_no_lang.writerow(["username"])

        for title_no_lang in filtered_results_no_lang:
            writer_no_lang.writerow([title_no_lang[0]])

    print("CSV files created successfully:", output_file, output_file_no_lang)


if __name__ == '__main__':
    csv_file = 'usernames.csv'
    output_file = 'user_languages.csv'
    output_file_no_lang = 'users_without_languages.csv'
    create_user_language_csv(csv_file, output_file, output_file_no_lang)