from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connections
import json
from requests import Request, Session


def home_page(request):
    return redirect('login')


@login_required
def predictions(request):
    api_url = "http://20.199.1.156/predict"

    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }

    session = Session()
    session.headers.update(headers)

    responses = []

    with connections['secondary'].cursor() as cursor:
        cursor.execute('SELECT * FROM soon_release')
        results = cursor.fetchall()

        for row in results:

            data_to_send = {
            "titre_fr": row[1],
            "realisateur": row[2],
            "acteurs": [x.strip() for x in row[3].split('_')],
            "genres": [row[1]],
            "budget": 0,
            "date_sortie": "string",
            "compagnies_production": [
            "string"
            ],
            "titre_non_modifie": "string"
            }

            response = session.post(api_url, json=data_to_send)
            responses.append(json.loads(response.text))

    zipped_data = zip(results, responses)

        
    return render(request, 'main/predictions.html', context={"zipped_data": zipped_data})


@login_required
def historique(request):
    return render(request, 'main/historique.html')


@login_required
def monitoring(request):
    return render(request, 'main/monitoring.html')
