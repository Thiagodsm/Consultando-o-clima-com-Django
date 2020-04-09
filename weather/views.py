from django.shortcuts import render, redirect
import requests
import json
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&lang=pt_br&units=metric&appid=a444eaf406381462486fe3e776816448'
    city = 'London'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            # checking is the city already exists
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                # checking if the city(name) is valid, via cod 200 or 404
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Cidade não existe!'
            else:
                err_msg = 'Cidade já existe na base de dados!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Cidade adicionada com sucesso!'
            message_class = 'is-success'

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
       
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
        
    context = {
        'weather_data': weather_data, 
        'form': form,
        'message': message,
        'message_class': message_class
        }
    return render(request, 'weather/weather.html', context)
 
 
 
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')