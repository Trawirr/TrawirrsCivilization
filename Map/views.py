from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def main_view(request):
    context = {}
    return render(request, 'base.html', context)

def map_view(request, map_name):
    print(map_name)
    context = {"map_name": map_name}
    return render(request, 'map.html', context)

    # with open("static/images/map_rgb.png", "rb") as f:
    #     return HttpResponse(f.read(), content_type="image/jpeg")

    # image_url = "static/images/map_rgb.png"
    # return JsonResponse({"image_url": image_url})