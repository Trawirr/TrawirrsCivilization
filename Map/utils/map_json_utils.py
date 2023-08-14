import json

def get_map_field(map_name, field_name):
    map_name = map_name.replace("_geo", "").replace("_political", "").replace(".png", "")
    with open(f"static/map_jsons/{map_name}.json") as f:
        data = json.load(f)
        return data[field_name]