
from background_script import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import seaborn as sns
import pingouin as pg
from scipy.stats import friedmanchisquare
from statsmodels.stats.anova import AnovaRM


X_LABEL = "Trial Number (Coding Task)"


def anova(df):
    n_rows, n_cols = df.shape
    groups = np.zeros((6, int(n_rows / 6)))
    groups_df = []

    for i, row in enumerate(range(0, n_rows, 6)):
        trial = df.iloc[row:row+6, :]
        for time_, fore, back in zip(trial["Completion Time"], trial["Foreground"], trial["Background"]):
            contrast_idx = CONTRASTS_BOTH.index((fore, back))
            groups[contrast_idx, i] = time_
            groups_df.append([i, contrast_idx, time_])

    groups_df = pd.DataFrame(groups_df, columns=["Subject", "Contrast", "Time"])

    print("Checking assumptions for Anova")

    print("1. Sphericity (should be non-significant)")
    sphericity = pg.sphericity(data=groups_df, dv="Time", subject="Subject", within="Contrast", method="mauchly")
    print(sphericity)

    print("2. Check for normality (should be non-significant)")
    normality = pg.normality(data=groups_df, dv="Time", group="Contrast", method="shapiro")
    print(normality)

    print("ANOVA:")
    repeated_anova = AnovaRM(data=groups_df, depvar="Time", subject="Subject", within=["Contrast"]).fit()
    print(repeated_anova)
    # post-hoc: pg.pairwise_tests()

    print("Friedman (non-parametric):")
    friedman_test = friedmanchisquare(*groups)
    print(friedman_test)
    # post-hoc: https://www.statology.org/nemenyi-test-python/


def box_plot(df):
    df["Theme"] = df["Background"].astype(str) + df["Foreground"].astype(str)

    plt.rcParams['figure.figsize'] = (8, 5)
    boxplot = sns.boxplot(x=df["Trial Number"], y=df["Completion Time"], hue=df["Theme"])
    plt.xlabel("Trial Number (Coding Task)")
    #sns.move_legend(boxplot, "upper left", bbox_to_anchor=(1, 1))
    plt.savefig("boxplot.pdf", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    df = pd.DataFrame()

    for x in os.listdir(DATA_PATH):
        df_tmp = pd.read_csv(os.path.join(DATA_PATH, x))
        df = pd.concat([df, df_tmp])

    anova(df)
    #box_plot(df.copy(deep=True))





    # df["Theme"] = df["Background"].astype(str) + df["Foreground"].astype(str) + df["Trial Number"].astype(str)
    # df_ratio = df.groupby("Theme", as_index=False).mean()
    # df_ratio["Theme"] = df_ratio["Theme"].apply(lambda x: x[:-1])

    # color = sns.color_palette("Greys")

    # colors = [(0, 0, 0), (170, 170, 170), (212, 212, 212), (255, 255, 255), (42, 42, 42), (85, 85, 85)]
    # colors = np.asarray(colors) / 255

    # barplot = sns.barplot(x=df_ratio["Trial Number"], y=df_ratio["Answer Correct"], hue=df_ratio["Theme"], palette=colors.tolist())
    # plt.xlabel(X_LABEL)

    # hatch_colors = [(255, 255, 255), (85, 85, 85), (42, 42, 42), (0, 0, 0), (212, 212, 212), (170, 170, 170)]
    # hatch_colors = np.asarray(hatch_colors) / 255

    # count = 0
    # for i in range(18):
    #     barplot.patches[i].set_hatch("..")
    #     barplot.patches[i].set_edgecolor(hatch_colors[count])
    #     print(hatch_colors[count], count, i)
    #     if (i + 1) % 3 == 0:
    #         count += 1

    # patches = []
    # for i in range(6):
    #     p = mpatches.Patch(facecolor=colors[i], edgecolor=hatch_colors[i], hatch="..", label="yy")
    #     patches.append(p)
    # plt.legend(handles=patches)
    # plt.show()

    
