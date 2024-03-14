import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.avignon.fr/ma-mairie/le-maire-et-le-conseil-municipal/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver tous les éléments qui contiennent les informations des membres du gouvernement
members = soup.find_all('div', class_='tx-dce-pil')

with open('membresMairieAvignon.csv', 'w', newline='', encoding='utf-8') as file:

    writer = csv.writer(file)

    writer.writerow(["Nom", "Fonction"])

    for member in members:
        # Trouver le nom dans le titre de la carte
        name = member.find('span', class_='thumbnail-link-label').get_text()
        # Trouver la fonction dans la description de la carte
        function = member.find('span', class_='thumbnail-excerpt').get_text()

        writer.writerow([name, function])
