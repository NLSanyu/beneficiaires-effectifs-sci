from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    erreur = None
    data = None

    if request.method == 'POST':
        siren = request.form.get('siren')
        token = os.getenv('API_TOKEN')
        url = f"https://api.pappers.fr/v2/company?api_token={token}&siren={siren}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json().get('beneficiaires_effectifs')
        else:
            erreur = f"Erreur : {response.status_code}"

    return render_template('index.html', erreur=erreur, data=data)

if __name__ == '__main__':
    app.run(debug=True)
