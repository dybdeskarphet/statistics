# ---
# jupyter:
#   jupytext:
#     cell_markers: '"""'
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
r"""
# Relationship between variables

There is a popular survey called NLSY97, it has data about students taking verbal and mathematical tests, we are going to use this data for seeing that if a student good at math is also good at verbal exams too.
"""

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# %%
stud = pd.read_csv("./data/nlsy97-extract.csv.gz").replace([-1, -2, -3, -4, -5], np.nan)

# %%
stud["sat_verbal"] = stud["R9793800"]
stud["sat_math"] = stud["R9793900"]

# %%
cols = ["sat_verbal", "sat_math"]
for c in cols:
    invalid = stud[c] < 200
    stud.loc[invalid, c] = np.nan

stud_valid = stud.dropna(subset=cols).copy()
stud_valid.shape

# %%
stud_valid[["sat_verbal", "sat_math"]]

# %% [markdown]
r"""
## Scatter Plots

Now that we have our columns, let's see if there is a correlation between verbal and math score.
"""

# %%
fig, ax = plt.subplots()
ax.scatter(stud_valid["sat_verbal"], stud_valid["sat_math"], s=5)
plt.show()

# %% [markdown]
r"""
Becuase the scores are rounded of the nearest multiple of 10, we cannot bring back the data, but we can add random noise.
"""


# %%
def jit(seq, std=1):
    return np.random.normal(0, std, len(seq)) + seq


# %%
sat_verbal_jitter = jit(stud_valid["sat_verbal"], 3)
sat_math_jitter = jit(stud_valid["sat_math"], 3)

# %%
fig, ax = plt.subplots()
ax.scatter(sat_verbal_jitter, sat_math_jitter, s=5, alpha=0.5)
ax.set_xlabel("SAT Math")
ax.set_ylabel("SAT Verbal")
plt.show()

# %% [markdown]
r"""
We can see some kind of correlation, but we had to tweak a lot of stuff to get the visualization right.
"""

# %% [markdown]
r"""
## Decile Plots

We have to divide the data to deciles, hence the name of the plot.
"""

# %%
deciles = pd.qcut(stud_valid["sat_verbal"], 30, labels=False) + 1
deciles.value_counts().sort_index()

# %%
stud_groupby = stud_valid.groupby(deciles)
math_groupby_ser = stud_groupby["sat_math"]
median = math_groupby_ser.quantile(0.5)
low = math_groupby_ser.quantile(0.1)
high = math_groupby_ser.quantile(0.9)
ixs = stud_groupby["sat_verbal"].quantile(0.5)
ixs

# %%
fig, ax = plt.subplots()
ax.fill_between(ixs, low, high, alpha=0.2)
ax.plot(ixs, median, label="median")
ax.set_xlabel("SAT Verbal")
ax.set_ylabel("SAT Math")
plt.show()

# %% [markdown]
r"""
We can see that relationship between SAT Math score and SAT Verbal score of respondents are somewhat has linear correlation.
"""

# %% [markdown]
r"""
## Correlation

When NLSY respondents were in 9th grade, many of them took the math section of the PIAT. Let's see if there is a correlation between PIAT Math score and the SAT Math score.
"""

# %%
stud_valid["piat_math"] = stud_valid["R1318200"]
stud_piat_sat = stud_valid.dropna(subset=["piat_math"])
stud_piat_sat.reset_index(inplace=True)
stud_piat_sat

# %%
stud_piat_sat_pdf = (
    stud_piat_sat["piat_math"].value_counts(normalize=True).sort_index().cumsum()
)

# %%
fig, ax = plt.subplots()
ax.plot(stud_piat_sat_pdf.index, stud_piat_sat_pdf)
plt.show()

# %%
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(stud_piat_sat["piat_math"], stud_piat_sat["sat_math"], s=5)
ax.set_xlabel("PIAT Math")
ax.set_ylabel("SAT Math")
plt.show()

# %% [markdown]
r"""
I just want to see if visualization would get better if I used min-max scaler for both columns
"""

# %%
scaler = MinMaxScaler()
stud_piat_sat["piat_math_minmax"] = scaler.fit_transform(stud_piat_sat[["piat_math"]])
stud_piat_sat["sat_math_minmax"] = scaler.fit_transform(stud_piat_sat[["sat_math"]])
stud_piat_sat

# %%
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(stud_piat_sat["piat_math_minmax"], stud_piat_sat["sat_math_minmax"], s=5)
ax.set_xlabel("PIAT Math (min-max scaled)")
ax.set_ylabel("SAT Math (min-max scaled)")
plt.show()

# %% [markdown]
r"""
Again, we can rougly say that people who did well in PIAT Math are likely to do well on SAT Math.
"""

# %% [markdown]
r"""
But since the title is "correlation", let's investigate **Pearson correlation coefficient**, often just called **correlation**.

Before that we have to standardize both of the columns to standardize. Standard score of a sample X can be calculate with the below formula.

$$
Z = \frac{x - \bar{x}}{s}
$$

But we are going to use `StandardScaler` which also does the same thing for a dataset.
"""

# %%
std_scaler = StandardScaler()
stud_piat_sat["piat_math_norm"] = std_scaler.fit_transform(stud_piat_sat[["piat_math"]])
stud_piat_sat["sat_math_norm"] = std_scaler.fit_transform(stud_piat_sat[["sat_math"]])
stud_piat_sat[["piat_math_norm", "sat_math_norm"]]

# %%
fig, axes = plt.subplots(2, 1, figsize=(7, 4))
axes[0].axhline(y=0, color="black", alpha=0.15)
axes[1].axhline(y=0, color="black", alpha=0.15)
axes[0].plot(stud_piat_sat["piat_math_norm"])
axes[1].plot(stud_piat_sat["sat_math_norm"])
axes[0].set_xlim(100, 200)
axes[1].set_xlim(100, 200)
axes[0].set_ylabel("z-score")
axes[1].set_ylabel("z-score")
plt.show()

# %% [markdown]
r"""
Even though it's hard to read it like this, we can totally see some kind of correlation here.
"""

# %% [markdown]
r"""
We can find the correlation coefficients using the below formula, and since we calculated the z-scores of our relevant columns, There is just one step left.

$$
r = \frac{\sum (z_x z_y)}{n-1}
$$
"""

# %%
print("r =", np.mean(stud_piat_sat["piat_math_norm"] * stud_piat_sat["sat_math_norm"]))

# %% [markdown]
r"""
This means that, if someone's PIAT Math score is 1 standard deviation above the mean, we expect their SAT math score to be 0.64 standard deviations above the mean, on average. Since the correlation coefficient is symmetric, the opposite is also true.
"""

# %%
print("r =", np.mean(stud_piat_sat["sat_math_norm"] * stud_piat_sat["piat_math_norm"]))
