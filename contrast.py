

def michelson_contrast(l_min, l_max):
    return abs((l_max - l_min)) / (l_max + l_min)


if __name__ == "__main__":
    step_size = 3

    background = 0
    foreground = 255

    dec = (255 / 2) / step_size

    print("\nBackground, Foreground, Michelson Contrast \n---")

    for i in range(step_size):
        back, fore = round(background), round(foreground)
        print(f"{back}, {fore}, {michelson_contrast(back, fore)} \n---")
        background += dec
        foreground -= dec