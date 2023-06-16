import requests
import re
import csv


# AW: Important reference data, perhaps this will move into its own file for
# reusability.  Should also include an explanation of how it was generated so
# that the data can be refreshed later.
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


# AW: Split this function so that the parsing can be tested separately from fetching.
def find_babel_languages(title):
    url = "https://en.wikipedia.org/w/index.php"
    params = {
        "title": title,
        "action": "raw"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        content = response.text
        babel_templates = re.findall(r"\{\{Babel((?:(?!\{\{Babel)[^{}])+)\}\}", content, re.IGNORECASE)
        # print("\n")
        # print("title:", title)
        # print("babel_templates:", babel_templates)
        language_claims = []
        if babel_templates:
            for babel_template in babel_templates:
                user_text = str(babel_template)
                user_languages = extract_language_codes(user_text)
                # print("user_languages:", user_languages)
                valid_user_languages = set()  # Use a set to store unique language codes
                for lang in user_languages:
                    sub_languages = lang.split('|')
                    # print("sub_languages:", sub_languages)
                    for sub_lang in sub_languages:
                        sub_lang = sub_lang.strip()  # Strip leading and trailing spaces
                        sub_lang = sub_lang.rstrip('\n')  # Remove any trailing '/n' characters
                        if '-' in sub_lang:
                            language_code, proficiency = sub_lang.rsplit('-', 1)  # Split on the last '-'
                            if language_code in allowed_languages:
                                valid_user_languages.add(sub_lang)  # Add unique language codes to the set
                        elif '|' not in sub_lang and sub_lang in allowed_languages:
                            valid_user_languages.add(sub_lang)  # Add unique language codes to the set

                language_claims.extend(valid_user_languages)  # Extend the list with valid user languages

                # print("valid_user_languages:", valid_user_languages)
                # print("language_claims:", language_claims)
        return title, language_claims

    return title, []


# CSV file path
csv_file = 'usernames2.csv'

# AW: Commands at the top level make it impossible to test, etc.  Better to wrap
# everything in a function and use the `if __name__ == '__main__':` convention
# to handle running on the command line.

# Fetch user titles with Babel templates from CSV
titles = get_user_titles_with_babel_from_csv(csv_file)

# Process Babel languages for each user
results = []
for title in titles:
    try:
        result = find_babel_languages(title)
        results.append(result)
    except Exception as e:
        print(f"Error occurred for user title: {title}")
        print(f"Error message: {str(e)}")

# Output CSV file path
output_csv_file = 'user_languages_test_3.csv'

# Filter results to include only usernames with languages
# AW: Maybe I broke the language list manual encoding?  `json.dumps` will be easier, anyway.
filtered_results = [(title, languages) for title, languages in results if languages]

# Write results to the output CSV file
with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['username', 'Languages'])
    writer.writerows(filtered_results)
