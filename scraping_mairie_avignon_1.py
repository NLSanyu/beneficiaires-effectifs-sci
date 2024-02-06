import csv
import requests
from bs4 import BeautifulSoup


url = 'https://www.avignon.fr/ma-mairie/le-maire-et-le-conseil-municipal'
response = requests.get(url, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver tous les éléments qui contiennent les informations des membres du gouvernement
members = soup.find_all('div', class_='tx-dce-pi1')

with open('ListeMairieAvignon.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(["Nom"])

    for member in members:
        # Trouver le nom dans le titre de la carte
        name = member.find('span', class_='thumbnail-link-label').text.strip()
        fonction = member.find('span', class_='thumbnail-excerpt').text.strip()
        # Trouver la fonction dans la description de la carte
        writer.writerow([name])
        print(f'Fonction: {fonction}')
