import requests
import re
import csv

allowed_languages = ['aa', 'ab', 'ace', 'ady', 'af', 'ak', 'als', 'alt', 'am', 'ami', 'an', 'ang', 'ar', 'arc', 'ary', 'arz', 'as', 'ast', 'atj', 'av', 'avk', 'awa', 'ay', 'az', 'azb', 'ba', 'ban', 'bar', 'bat-smg', 'bcl', 'be', 'be-tarask', 'bg', 'bh', 'bi', 'bjn', 'blk', 'bm', 'bn', 'bo', 'bpy', 'br', 'bs', 'bug', 'bxr', 'ca', 'cbk-zam', 'cdo', 'ce', 'ceb', 'ch', 'cho', 'chr', 'chy', 'ckb', 'co', 'cr', 'crh', 'cs', 'csb', 'cu', 'cv', 'cy', 'da', 'dag', 'de', 'din', 'diq', 'dsb', 'dty', 'dv', 'dz', 'ee', 'el', 'eml', 'en', 'eo', 'es', 'et', 'eu', 'ext', 'fa', 'ff', 'fi', 'fiu-vro', 'fj', 'fo', 'gur', 'fr', 'frp', 'frr', 'fur', 'fy', 'ga', 'gag', 'gan', 'gcr', 'gd', 'gl', 'glk', 'gn', 'gom', 'gor', 'got', 'gu', 'guw', 'gv', 'ha', 'hak', 'haw', 'he', 'hi', 'hif', 'ho', 'hr', 'hsb', 'ht', 'hu', 'hy', 'hyw', 'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'ilo', 'inh', 'io', 'is', 'it', 'iu', 'ja', 'jam', 'jbo', 'jv', 'ka', 'kaa', 'kab', 'kbd', 'kbp', 'kcg', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'koi', 'kr', 'krc', 'ks', 'ksh', 'ku', 'kv', 'kw', 'ky', 'la', 'lad', 'lb', 'lbe', 'lez', 'lfn', 'lg', 'li', 'lij', 'lld', 'lmo', 'ln', 'lo', 'lrc', 'lt', 'ltg', 'lv', 'mad', 'mai', 'map-bms', 'mdf', 'mg', 'mh', 'mhr', 'mi', 'min', 'mk', 'ml', 'mn', 'mni', 'mnw', 'mr', 'mrj', 'ms', 'mt', 'mus', 'mwl', 'my', 'myv', 'mzn', 'na', 'nah', 'nap', 'nds', 'nds-nl', 'ne', 'new', 'ng', 'nia', 'nl', 'nn', 'no', 'nov', 'nqo', 'nrm', 'nso', 'nv', 'ny', 'oc', 'olo', 'om', 'or', 'os', 'pa', 'pag', 'pam', 'pap', 'pcd', 'pcm', 'pdc', 'pfl', 'pi', 'pih', 'pl', 'pms', 'pnb', 'pnt', 'ps', 'pt', 'pwn', 'qu', 'rm', 'rmy', 'rn', 'ro', 'roa-rup', 'roa-tara', 'ru', 'rue', 'rw', 'sa', 'sah', 'sat', 'sc', 'scn', 'sco', 'sd', 'se', 'sg', 'sh', 'shi', 'shn', 'si', 'simple', 'sk', 'skr', 'sl', 'smn', 'sm', 'sn', 'so', 'sq', 'sr', 'srn', 'ss', 'st', 'stq', 'su', 'sv', 'sw', 'szl', 'szy', 'ta', 'tay', 'tcy', 'te', 'tet', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tpi', 'tr', 'trv', 'ts', 'tt', 'tum', 'tw', 'ty', 'tyv', 'udm', 'ug', 'uk', 'ur', 'uz', 've', 'vec', 'vep', 'vi', 'vls', 'vo', 'wa', 'war', 'guc', 'wo', 'wuu', 'xal', 'xh', 'xmf', 'yi', 'yo', 'za', 'zea', 'zh', 'zh-classical', 'zh-min-nan', 'zh-yue', 'zu']

def get_user_titles_with_babel_from_csv(csv_file):
    titles = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            titles.append("User:" + row[1])  # Assuming usernames are in the second column
    return titles[0:]


def extract_language_codes(template_text):
    code_pattern = r"[a-z]{2,3}(?:-[a-zA-Z0-9])?"
    languages = re.findall(code_pattern, template_text, re.IGNORECASE)
    return languages


def find_babel_languages(title):
    url = "https://en.wikipedia.org/w/index.php"
    params = {
        "title": title,
        "action": "raw"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        content = response.text
        user_templates = re.findall(r"\{\{user[^}]*?([a-z]{2,3}-\d)(?=[^}]*?\}\})", content, re.IGNORECASE)
        language_claims = []
        if user_templates:
            user_text = str(user_templates)
            user_languages = extract_language_codes(user_text)
            valid_user_languages = set()  # Use a set to store unique language codes
            for lang in user_languages:
                language_code, proficiency = lang.split('-')
                if language_code in allowed_languages:
                    valid_user_languages.add(lang)  # Add unique language codes to the set

            language_claims.extend(valid_user_languages)
        return title, language_claims

    return title, []


# CSV file path
csv_file = 'usernames.csv'

# Fetch user titles with Babel templates from CSV
titles = get_user_titles_with_babel_from_csv(csv_file)

# Process Babel languages for each user
results = [find_babel_languages(title) for title in titles]

# Filter results to exclude users with empty valid_user_languages
filtered_results = [(title, languages) for title, languages in results if languages]

# Create a CSV file and write the filtered results
output_file = 'user_languages.csv'

with open(output_file, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Username", "Language"])  # Write header row

    for title, languages in filtered_results:
        language_string = '[' + ', '.join([f"'{lang}'" for lang in languages]) + ']'
        writer.writerow([title, language_string])

print("CSV file created successfully: ", output_file)
