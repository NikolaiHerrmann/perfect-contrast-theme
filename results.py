
from background_script import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import seaborn as sns
import pingouin as pg
from scipy.stats import friedmanchisquare
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.contingency_tables import cochrans_q
import os


X_LABEL = "Trial Number (Coding Task)"
LABELS = {0: "High Black-Back", 1: "Mid Black-Back", 2: "Low Black-Back",
          3: "High White-Back", 4: "Mid White-Back", 5: "Low White-Back"}
HATCH_TYPE = ["//", "//", "//", "\\", "\\", "\\"]

colors = np.asarray(CONTRASTS_BOTH) / 255
back_colors, fore_colors = colors[:, 0], colors[:, 1]

back_colors = np.tile(back_colors, (3, 1)).T.tolist()
fore_colors = np.tile(fore_colors, (3, 1)).T

plt.rcParams['hatch.linewidth'] = 0.5
FIGURE_PATH = "figures"


def anova(df):
    n_rows, n_cols = df.shape
    groups = np.zeros((6, int(n_rows / 6)))
    groups_df = []

    answers = np.zeros((int(n_rows / 6), 6))

    for i, row in enumerate(range(0, n_rows, 6)):
        trial = df.iloc[row:row+6, :]
        for time_, fore, back, answer in zip(trial["Completion Time"], trial["Foreground"], trial["Background"], trial["Answer Correct"]):
            contrast_idx = CONTRASTS_BOTH.index((fore, back))
            groups[contrast_idx, i] = time_
            groups_df.append([i, contrast_idx, time_])

            answers[i, contrast_idx] = answer

    groups_df = pd.DataFrame(groups_df, columns=["Subject", "Contrast", "Time"])

    print("Significance for Completion Time")
    print("Checking assumptions for Anova")
    print("1. Sphericity (should be non-significant)")
    sphericity = pg.sphericity(data=groups_df, dv="Time", subject="Subject", within="Contrast", method="mauchly")
    print(sphericity)

    print("2. Check for normality (should be non-significant)")
    normality = pg.normality(data=groups_df, dv="Time", group="Contrast", method="shapiro")
    print(normality)

    print("ANOVA test:")
    repeated_anova = AnovaRM(data=groups_df, depvar="Time", subject="Subject", within=["Contrast"]).fit()
    print(repeated_anova)
    # post-hoc: pg.pairwise_tests()

    print("Friedman test (non-parametric):")
    friedman_test = friedmanchisquare(*groups)
    print(friedman_test)
    # post-hoc: https://www.statology.org/nemenyi-test-python/

    print("Significance for Correct Responses")
    print("Cochran's Q test (non-parametric):")
    cochrans = cochrans_q(answers)
    print(cochrans)
    # post-hoc: McNemar tests with a Bonferroni correction (https://rasbt.github.io/mlxtend/user_guide/evaluate/cochrans_q/)


def make_theme_col(df):
    n_rows, n_cols = df.shape
    theme_index = np.zeros((n_rows, 1), dtype=int)

    for i in range(n_rows):
        theme_index[i] = CONTRASTS_BOTH.index((df["Foreground"].iloc[i], df["Background"].iloc[i]))

    df["Theme"] = theme_index.astype(str) 


def apply_patches(plot):
    count = 0
    for i in range(18):
        plot.patches[i].set_hatch(HATCH_TYPE[count])
        plot.patches[i].set_edgecolor(fore_colors[count])
        if (i + 1) % 3 == 0:
            count += 1

    patches = []
    for i in range(6):
        p = mpatches.Patch(facecolor=back_colors[i], edgecolor=fore_colors[i], hatch=HATCH_TYPE[i], label=LABELS[i])
        patches.append(p)

    plt.legend(handles=patches)


def save_plot(name):
    plt.savefig(os.path.join(FIGURE_PATH, name + ".pdf"), bbox_inches="tight")
    plt.savefig(os.path.join(FIGURE_PATH, name + ".png"), bbox_inches="tight", dpi=300)


def box_plot(df):
    make_theme_col(df)
    df["Theme"] = df["Theme"].apply(lambda x: LABELS[int(x)])

    df["Trial Number"] = df["Trial Number"].astype(int)
    boxplot = sns.boxplot(x=df["Trial Number"], y=df["Completion Time"], hue=df["Theme"], palette=back_colors)
    plt.xlabel(X_LABEL)
    #sns.move_legend(boxplot, "upper left", bbox_to_anchor=(1, 1))

    apply_patches(boxplot)

    save_plot("boxplot")
    plt.show()


def bar_plot(df):

    make_theme_col(df)
    
    df["Theme"] += df["Trial Number"].astype(str)

    df_ratio = df.groupby("Theme", as_index=False).mean()
    df_ratio["Theme"] = df_ratio["Theme"].apply(lambda x: LABELS[int(x[:-1])]) # remove trial number
    df_ratio["Trial Number"] = df_ratio["Trial Number"].astype(int)

    barplot = sns.barplot(x=df_ratio["Trial Number"], y=df_ratio["Answer Correct"], hue=df_ratio["Theme"], palette=back_colors)
    plt.xlabel(X_LABEL)
    plt.ylabel("Correctness Ratio")
    plt.title("Response Correctness across Themes")

    # for i in range(18):
    #     barplot.patches[i].set_edgecolor("black")

    apply_patches(barplot)

    save_plot("barplot")
    plt.show()


if __name__ == "__main__":
    df = pd.DataFrame()

    for x in os.listdir(DATA_PATH):
        df_tmp = pd.read_csv(os.path.join(DATA_PATH, x))
        df = pd.concat([df, df_tmp])

    anova(df)
    box_plot(df.copy(deep=True))
    bar_plot(df.copy(deep=True))

