
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from background_script import *
from results import *


def subplot():
    fig, axs = plt.subplots(9, 1, figsize=(5, 7))
    fig.tight_layout()
    count = 0

    for j, x, in enumerate(os.listdir(DATA_PATH)):
        df = pd.read_csv(os.path.join(DATA_PATH, x))

        for i in range(3):
            idx = i * 6
            times = df.iloc[idx:idx+6, :]["Completion Time"].to_numpy().tolist()
            axs[count].scatter([times.pop(0)], [0], label="Comprehension Question 1", color="tab:orange")
            axs[count].scatter(times, np.zeros((len(times), 1)), label="Comprehension Questions 2 to 6", color="tab:blue")
            axs[count].set_yticks([])
            axs[count].set_ylabel(f"$\\it{{Participant {j + 1}}}$\nTask {i + 1}", rotation=0)
            axs[count].yaxis.set_label_coords(-0.11, 0.05)
            count += 1

    fig.supxlabel("Completion Time (Seconds)", y=-0.03)
    plt.suptitle("Completion Time of First Comprehension Question \n Compared to Subsequent Ones", y=1.06)
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -4.5))

    plt.savefig(os.path.join(FIGURE_PATH, "first_theme_times.pdf"), bbox_inches="tight")

if __name__ == "__main__":
    subplot()