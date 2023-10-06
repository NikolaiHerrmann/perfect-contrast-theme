
import json
import os


def io_json(file_name, dic=None):
    if dic:
        with open(file_name, "w") as f:
            json.dump(dic, f)
    else:
        with open(file_name) as f:
            dic = json.load(f)
    
    return dic


def update_color(dic, background, foreground):
    color_key = 'workbench.colorCustomizations'
    
    for key, val in dic[color_key].items():
        key_lower = key.lower()
        color = val
        if "background" in key_lower or "background" in val:
            color = background
        elif "foreground" in key_lower or "foreground" in val:
            color = foreground
        
        dic[color_key][key] = color


path = "settings_org.json"
vs_settings = io_json(path)
update_color(vs_settings, "#000000", "#808080")
print(vs_settings)
io_json(os.path.join(".vscode", "settings.json"), vs_settings)