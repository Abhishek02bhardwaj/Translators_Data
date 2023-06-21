import requests
import csv

url = "https://meta.wikimedia.org/w/api.php?action=sitematrix&format=json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    language_codes = []
    sitematrix = data.get("sitematrix", {})
    for group_key, group_value in sitematrix.items():
        if group_key.isdigit() and "code" in group_value:
            language_code = group_value["code"]
            language_codes.append(language_code)

            with open("language_codes_1.csv", "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Language Code"])
                for code in language_codes:
                    writer.writerow([f"{code}"])
                    writer.writerow([f"{code}-N"])
                    for i in range(6):
                        writer.writerow([f"{code}-{i}"])

    print("Language codes saved successfully.")
else:
    raise ConnectionError("Failed to retrieve the Wikipedia language data.")
