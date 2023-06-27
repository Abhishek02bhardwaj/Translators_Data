import requests
import csv

url = "https://meta.wikimedia.org/w/api.php?action=sitematrix&smlangprop=code&smtype=language&format=json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    language_codes = set()

    sitematrix = data.get("sitematrix", {})
    for group_key, group_value in sitematrix.items():
        if isinstance(group_value, dict) and "code" in group_value:
            language_code = group_value["code"]
            language_codes.add(language_code)

    language_codes = sorted(language_codes)  # Sort the language codes alphabetically

    with open("language_codes.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Language Code"])
        for code in language_codes:
            writer.writerow([code])
            writer.writerow([f"{code}-N"])
            for i in range(6):
                writer.writerow([f"{code}-{i}"])
    print("Language codes saved successfully.")
else:
    raise ConnectionError("Failed to retrieve the Wikipedia language data.")
