from django.shortcuts import render, redirect


def home_page(request):
    return redirect('login')


def estimation(request):
    return render(request, 'main/estimation.html')
