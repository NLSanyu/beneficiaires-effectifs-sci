import requests
from bs4 import BeautifulSoup


import requests
from bs4 import BeautifulSoup


url = 'https://www.gouvernement.fr/personnalite/gabriel-attal?mission=premier-ministre'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# Trouver la section spécifique avec l'ID 'fr_accordion'
accordion = soup.find(id='fr_grid_row')


# Parcourir chaque sous-section
for section in accordion.find_all('section', class_='fr-accordion'):
    # Titre de la section
    title = section.find('h3').text.strip()


    # Parcourir chaque membre dans la section
    for member in section.find_all('li'):
        name = member.find('div', class_='fr-text--bold fr-mb-1v').text.strip()
        function = member.find('div', class_='fr-mb-1w').text.strip()
        print(f'Section: {title}, Nom: {name}, Fonction: {function}')
