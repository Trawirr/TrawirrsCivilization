from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.management import call_command
from .utils.map_utils import generate_random_string

def main_view(request):
    context = {}
    return render(request, 'base.html', context)

def map_view(request, map_name):
    print(map_name)
    map_name_changed = map_name.replace("geo", "political") if "geo" in map_name else map_name.replace("political", "geo")
    context = {
        "map_name": map_name,
        "map_name_changed": map_name_changed
        }
    return render(request, 'map.html', context)

def generate_form_view(request):
    context = {}
    return render(request, 'generate_form.html', context)

def generate_map(request):
    print("Generating map...")
    map_name = generate_random_string()
    call_command("CreateMap", 
                 size=int(request.GET['size']),  
                 octaves=request.GET['octaves'], 
                 sealevel=float(request.GET['sealevel']), 
                 border=int(request.GET['border']),
                 name=map_name
                 )
    context = {}
    return map_view(request, map_name+"_geo.png")