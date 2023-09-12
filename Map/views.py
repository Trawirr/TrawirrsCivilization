from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.management import call_command
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .utils.map_utils import generate_random_string, map_value, get_tile_color
from .utils.map_json_utils import get_map_field, get_mapped_height, get_map_names
from .utils.map_image_utils import get_pixel_color
from .utils.biomes_utils import BiomeHandler
from Map.models import Map, FavouriteMap

def empty_view(request):
    return HttpResponse()

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

@login_required
def generate_form_view(request):
    context = {}
    return render(request, 'generate_form.html', context)

@login_required
def generate_map(request):
    map_name = generate_random_string()
    call_command("CreateMap", 
                 size=int(request.GET['size']),  
                 octaves=request.GET['octaves'], 
                 sealevel=float(request.GET['sealevel']), 
                 border=int(request.GET['border']),
                 name=map_name,
                 username=request.user.username
                 )
    context = {}
    print(f"Generate map, map name: {map_name}")
    return map_view(request, map_name+"_geo.png")

def get_tooltip(request):
    map_name = request.GET.get('map_name', 'map')
    x = int(request.GET.get('x', 1)) - 1
    y = int(request.GET.get('y', 1)) - 1

    map_handler = BiomeHandler(map_name)
    map_handler.load_map_info()
    map_handler.load_biome_info()

    height = map_handler.get_mapped_height(x, y)
    tooltip_content = f'({x}, {y})<br>Height: {height:.2f}m'

    reservoir = map_handler.get_area(x, y)
    if reservoir:
        tooltip_content += f"<br>{reservoir}"

    return HttpResponse(tooltip_content)

def gallery_view(request, gallery_type):
    maps = Map.objects.all()
    if request.user.is_authenticated: 
        favourite_maps = FavouriteMap.objects.filter(user=request.user).values_list("map__name", flat=True)
    else:
        favourite_maps = []
    context = {
        "maps": maps,
        "favourite_maps": favourite_maps,
        'gallery_type': gallery_type,
        }
    return render(request, 'gallery.html', context)

@login_required
def users_gallery_view(request):
    user = request.user
    context = {"maps": Map.objects.filter(author=user).values_list("name", flat=True)}
    return render(request, 'gallery.html', context)

@login_required
def add_to_favourites(request):
    print(request.POST, list(request.POST.keys()), sep="\n")
    map_name = list(request.POST.keys())[0][3:]
    selected_map = Map.objects.get(name=map_name)
    user = request.user
    if FavouriteMap.objects.filter(user=user, map=selected_map).count() > 0:
        FavouriteMap.objects.get(user=user, map=selected_map).delete()
        return HttpResponse(f"""<span class="heart-icon far fa-heart" hx-post="/add_to_favourites" hx-include="[name='map{map_name}']" hx-target="this" hx-swap="outerHTML">
            <input type="hidden" value="{map_name}" name="map{map_name}">
        </span>""")
    else:
        new_favourite_map = FavouriteMap(user=user, map=selected_map)
        new_favourite_map.save()
        return HttpResponse(f"""<span class="heart-icon fas fa-heart" hx-post="/add_to_favourites" hx-include="[name='map{map_name}']" hx-target="this" hx-swap="outerHTML">
            <input type="hidden" value="{map_name}" name="map{map_name}">
        </span>""")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main')