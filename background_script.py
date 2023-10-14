
import json
import os
import random
import inspect
import time
import test_functions
import numpy as np


RANDOM_SEED = 42
CONTRASTS = [(0, 255), (42, 212), (85, 170)]
PARENT_PATH = ".."
SETTINGS_PATH = os.path.join(PARENT_PATH, "settings_org.json")
FUNC_FILE_NAME = "code.txt"
VSCODE_PATH = os.path.join(".vscode", "settings.json")


def io_json(file_name, dic=None):
    if dic:
        with open(file_name, "w") as f:
            json.dump(dic, f, indent=4)
    else:
        with open(file_name) as f:
            dic = json.load(f)
    
    return dic


def update_color(dic, background, foreground):
    color_key = "workbench.colorCustomizations"
    
    for key, val in dic[color_key].items():
        key_lower = key.lower()
        color = val
        if "background" in key_lower or "background" in val:
            color = background
        elif "foreground" in key_lower or "foreground" in val:
            color = foreground
        
        dic[color_key][key] = color


def rgb_to_hex(r, g, b):
    def in_range(x):
        return x >= 0 and x <= 255
    
    assert in_range(r) and in_range(g) and in_range(b)

    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def color(x):
    return rgb_to_hex(x, x, x)


def show_function(func_str):
    func = getattr(test_functions, func_str)
    lines = inspect.getsource(func)
    answer = func()

    with open(FUNC_FILE_NAME, "w") as f:
        f.write(lines)

    os.system(f"code {FUNC_FILE_NAME}")

    return answer


def rm_files():
    os.remove(VSCODE_PATH) if os.path.exists(VSCODE_PATH) else None
    os.remove(FUNC_FILE_NAME) if os.path.exists(FUNC_FILE_NAME) else None
    

def run_trial(funcs):
    results = np.zeros((6, 4))
    
    rm_files()

    contrasts = [x[::-1] for x in CONTRASTS] + CONTRASTS
    random.shuffle(contrasts)

    input("Hit enter to start experiment!")

    for i, (background, foreground) in enumerate(contrasts):

        vs_settings = io_json(SETTINGS_PATH)
        update_color(vs_settings, color(background), color(foreground))
        io_json(VSCODE_PATH, vs_settings)

        true_answer = show_function(funcs[i])

        start_time = time.time()

        while True:
            try:
                user_answer = input("Answer:")
                user_answer = int(user_answer)
                break
            except:
                print("Invalid input!")

        end_time = time.time()

        results[i, :] = [end_time - start_time, 1 if user_answer == true_answer else 0, true_answer, user_answer]

        input("Press space to move onto next question.")

    rm_files()

    return results


if __name__ == "__main__":
    random.seed(RANDOM_SEED)
    
    all_funcs = [f"func{x}" for x in range(1, 7)]

    results = run_trial(all_funcs)
    np.savetxt(os.path.join(PARENT_PATH, "answers.csv"), results, delimiter=",")
