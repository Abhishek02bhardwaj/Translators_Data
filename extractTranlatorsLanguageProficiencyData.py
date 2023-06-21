import requests
import re
import csv


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


# AW: See simplified implementation in review-1
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


# AW: suggest to split into units
# 	extract snippets
# 	parse template into parameters
# 	filter to languages / and optionally warn for bad data
def parse_babel_templates(content, allowed_languages):
    babel_templates = re.findall(r"\{\{Babel((?:(?!\{\{Babel)[^{}])+)\}\}", content, re.IGNORECASE)
    language_claims = []
    if babel_templates:
        for babel_template in babel_templates:
            user_text = str(babel_template)
            user_languages = extract_language_codes(user_text)
            valid_user_languages = set()
            for lang in user_languages:
                sub_languages = lang.split('|')
                for sub_lang in sub_languages:
                    sub_lang = sub_lang.strip()
                    sub_lang = sub_lang.rstrip('\n')
                    if sub_lang in allowed_languages:
                        valid_user_languages.add(sub_lang)

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


def create_user_language_csv(csv_file, output_file):
    allowed_languages = get_allowed_languages_from_csv('language_codes.csv')
    titles = get_user_titles_with_babel_from_csv(csv_file)
    results = [find_babel_languages(title, allowed_languages) for title in titles]
    # AW: we might want to keep the empty data as well?
    filtered_results = [(title, languages) for title, languages in results if languages]

    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "language"])

        for title, languages in filtered_results:
            # AW: Use a more standard format such as json.dumps or
            # "|".join(foo), currently this needs to be parsed with
            # ast.literal_eval and couples us to Python more than necessary.
            language_string = '[' + ', '.join([f"'{lang}'" for lang in languages]) + ']'
            writer.writerow([title, language_string])

    print("CSV file created successfully:", output_file)


if __name__ == '__main__':
    csv_file = 'usernames.csv'
    output_file = 'user_languages.csv'
    create_user_language_csv(csv_file, output_file)
