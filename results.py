from background_script import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import friedmanchisquare
from statsmodels.stats.anova import AnovaRM

df = pd.DataFrame()

for x in os.listdir(DATA_PATH):
    df_tmp = pd.read_csv(os.path.join(DATA_PATH, x))
    df = pd.concat([df, df_tmp])

n_rows, n_cols = df.shape
groups = np.zeros((int(n_rows / 6), 6))
groups_df = []

for i, row in enumerate(range(0, n_rows, 6)):
    trial = df.iloc[row:row+6, :]
    for time_, fore, back in zip(trial["Completion Time"], trial["Foreground"], trial["Background"]):
        contrast_idx = CONTRASTS_BOTH.index((fore, back))
        groups[i, contrast_idx] = time_
        groups_df.append([i, contrast_idx, time_])

groups_df = pd.DataFrame(groups_df, columns=["Subject", "Contrast", "Time"])

friedman_test = friedmanchisquare(*groups)
print(friedman_test)
repeated_anova = AnovaRM(data=groups_df, depvar="Time", subject="Subject", within=["Contrast"]).fit()
print(repeated_anova)
