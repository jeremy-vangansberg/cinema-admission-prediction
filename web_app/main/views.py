from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home_page(request):
    return redirect('login')


@login_required
def predictions(request):
    return render(request, 'main/predictions.html')


@login_required
def historique(request):
    return render(request, 'main/historique.html')


@login_required
def monitoring(request):
    return render(request, 'main/monitoring.html')
