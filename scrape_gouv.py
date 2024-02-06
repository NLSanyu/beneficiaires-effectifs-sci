import csv
import requests
from bs4 import BeautifulSoup


url = 'https://www.gouvernement.fr/composition-du-gouvernement'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# Trouver tous les éléments qui contiennent les informations des membres du gouvernement
members = soup.find_all('div', class_='fr-grid-row fr-grid-row--gutters fr-cards-group')

with open('listeGouvernement.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(["Nom", "Fonction"])

    for member in members:
        # Trouver le nom dans le titre de la carte
        name = member.find('h3', class_='fr-card__title').text.strip()
        # Trouver la fonction dans la description de la carte
        function = member.find('p', class_='fr-card__desc').text.strip()

        writer.writerow([name, function])

        print(f'Nom: {name}, Fonction: {function}')

