from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.management import call_command
from .utils.map_utils import generate_random_string, map_value
from .utils.map_json_utils import get_map_field, get_mapped_height, get_map_names
from .utils.map_image_utils import get_pixel_color
from .utils.biomes_utils import BiomeHandler

def main_view(request):
    context = {}
    return render(request, 'base.html', context)

def map_view(request, map_name):
    if "geo" in map_name:
        map_name_changed = map_name.replace("geo", "political")
    elif "political" in map_name:
        map_name_changed = map_name.replace("political", "biomes")
    elif "biomes" in map_name:
        map_name_changed = map_name.replace("biomes", "geo")

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
    map_name = request.GET.get('map_name', 'map')
    x = int(request.GET.get('x', 1)) - 1
    y = int(request.GET.get('y', 1)) - 1

    map_handler = BiomeHandler(map_name)
    map_handler.load_map_info()
    map_handler.load_biome_info()

    height = map_handler.get_mapped_height(x, y)
    tooltip_content = f'({x}, {y})<br>Height: {height:.2f}m<br>{map_handler.get_temp_hum(x, y)}'

    reservoir = map_handler.get_area(x, y)
    if reservoir:
        tooltip_content += f"<br>{reservoir}"

    return HttpResponse(tooltip_content)

def gallery_view(request):
    context = {"maps": get_map_names()}
    return render(request, 'gallery.html', context)