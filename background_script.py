
import json
import os
import random
import inspect
import time
import trial_1_func, trial_2_func, trial_3_func
import pandas as pd
from pynput.keyboard import Key, Controller


KEYBOARD = Controller()
RANDOM_SEED = 42
CONTRASTS = [(0, 255), (42, 212), (85, 170)]
CONTRASTS_BOTH = CONTRASTS + [x[::-1] for x in CONTRASTS]
PARENT_PATH = ".."
SETTINGS_PATH = os.path.join(PARENT_PATH, "settings_org.json")
FUNC_FILE_NAME = "code.txt"
VSCODE_PATH = os.path.join(".vscode", "settings.json")
DATA_PATH = "data"
DATA_PATH_EXP = os.path.join(PARENT_PATH, DATA_PATH)
COLS = ["Trial Number", "Background", "Foreground", "Completion Time", "Answer Correct", "True Answer", "Subject Answer"]


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


def show_function(trial_module_file, func_str):
    func = getattr(trial_module_file, func_str)
    lines = inspect.getsource(func)
    answer = func()

    with open(FUNC_FILE_NAME, "w") as f:
        f.write(lines)

    os.system(f"code {FUNC_FILE_NAME}")

    return answer


def rm_files():
    os.remove(VSCODE_PATH) if os.path.exists(VSCODE_PATH) else None
    os.remove(FUNC_FILE_NAME) if os.path.exists(FUNC_FILE_NAME) else None


def close_all_files():
    KEYBOARD.press(Key.ctrl)
    KEYBOARD.press("k")
    KEYBOARD.press("w")
    KEYBOARD.release("w")
    KEYBOARD.release("k")
    KEYBOARD.release(Key.ctrl)
    

def run_trial(trial_module_file):
    funcs = [f"func{x}" for x in range(1, 7)]
    results = []
    
    rm_files()

    contrasts = CONTRASTS_BOTH.copy()
    random.shuffle(contrasts)

    print("\n" * 20)
    trial_number = trial_module_file.__name__.split("_")[1]
    input(f"Trial {trial_number}! Hit enter to start experiment!")

    for i, (background, foreground) in enumerate(contrasts):

        vs_settings = io_json(SETTINGS_PATH)
        update_color(vs_settings, color(background), color(foreground))
        io_json(VSCODE_PATH, vs_settings)

        print("\n" * 20)
        true_answer = show_function(trial_module_file, funcs[i])

        start_time = time.time()

        while True:
            try:
                user_answer = input("Answer:")
                user_answer = int(user_answer)
                break
            except:
                print("Invalid input, didn't get an integer!")

        end_time = time.time()

        answer_graded = 1 if true_answer == user_answer else 0
        results.append((trial_number, background, foreground, end_time - start_time, answer_graded, true_answer, user_answer))

        close_all_files()

        input("Press enter to move onto next question.")

    rm_files()

    return results


if __name__ == "__main__":
    random.seed(RANDOM_SEED)

    if not os.path.exists(DATA_PATH_EXP):
        os.mkdir(DATA_PATH_EXP)
    
    trial_modules = [trial_1_func, trial_2_func, trial_3_func]
    results = []

    for trial in trial_modules:
        results += run_trial(trial)

    print("\nResults:\n", results)
    df = pd.DataFrame(results, columns=COLS)
    df.to_csv(os.path.join(DATA_PATH_EXP, "answers_" + str(time.time()) + ".csv"), sep=",", index=False)
