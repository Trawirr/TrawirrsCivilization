from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.management import call_command
from .utils.map_utils import generate_random_string, map_value
from .utils.map_json_utils import get_map_field, get_map_height, get_reservoir
from .utils.map_image_utils import get_pixel_color

def main_view(request):
    context = {}
    return render(request, 'base.html', context)

def map_view(request, map_name):
    print(map_name)
    map_name_changed = map_name.replace("geo", "political") if "geo" in map_name else map_name.replace("political", "geo")
    context = {
        "map_name": map_name,
        "map_name_changed": map_name_changed,
        "map_size": get_map_field(map_name, "size")
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

def get_tooltip(request):
    print(request.GET['x'], request.GET['y'])
    map_name = request.GET.get('map_name', 'map')
    x = int(request.GET.get('x', 1)) - 1
    y = int(request.GET.get('y', 1)) - 1

    height = get_map_height(map_name, x, y)
    tooltip_content = f'({x}, {y})<br>Height: {height:.2f}m'

    reservoir = get_reservoir(map_name, x, y)
    if reservoir:
        tooltip_content += f"<br>{reservoir}"

    return HttpResponse(tooltip_content)