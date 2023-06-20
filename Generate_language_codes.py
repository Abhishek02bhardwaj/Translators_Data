import requests
import csv

# AW: Here are some parameters which simplify the results to only return "code" and skip the "specials":
#   https://meta.wikimedia.org/w/api.php?action=sitematrix&smlangprop=code&smtype=language
url = "https://meta.wikimedia.org/w/api.php?action=sitematrix&format=json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    language_codes = []
    sitematrix = data.get("sitematrix", {})
    for group_key, group_value in sitematrix.items():
        # AW: Confirmed that it really is this wild.  "specials" should be ignored.
        #   With the extra parameters above, this can be simplified BTW.
        if group_key.isdigit() and "code" in group_value:
            language_code = group_value["code"]
            # AW: a "set" would be better because it deduplicates.
            language_codes.append(language_code)

            # AW: Should be dedented to outside of the iteration.
            with open("language_codes_1.csv", "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Language Code"])
                # AW: Do this expansion when reading the file, keep the stored format simple.
                for code in language_codes:
                    writer.writerow([f"{code}"])
                    writer.writerow([f"{code}-N"])
                    for i in range(6):
                        writer.writerow([f"{code}-{i}"])

    print("Language codes saved successfully.")
else:
    raise ConnectionError("Failed to retrieve the Wikipedia language data.")
