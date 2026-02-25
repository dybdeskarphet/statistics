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
# Probability Density Functions
"""

# %%
from random import sample
import matplotlib
from matplotlib.lines import lineStyles
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f, trimboth, norm
from scipy.integrate import simpson

# %% [markdown]
r"""
## Normal distribution PDF

We start with the PDF of the normal distribution. Formula of normal distribution PDF is:

$$
\frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}
$$

Let's evaulate range of weights (NSFG birth data) using Normal PDF.
"""

# %%
birth = pd.read_csv("./data/2002FemPreg_after_01.csv")
birth

# %%
trimmed_weight = trimboth(birth["totalwgt_kg"].dropna(), 0.01)


# %%
trim_mean, trim_std = np.mean(trimmed_weight), np.std(trimmed_weight)
trim_high, trim_low = trim_mean + trim_std * 4, trim_mean - trim_std * 4

# %%
x_ticks = np.linspace(trim_low, trim_high, 201)

# %%
norm_dist = norm.pdf(x_ticks, trim_mean, trim_std)
norm_pdf = pd.Series(norm_dist, index=x_ticks)
norm_pdf

# %%
fig, ax = plt.subplots()
ax.plot(norm_pdf.index, norm_pdf)
plt.show()

# %% [markdown]
r"""
We know that area under PDF equals to 1, let's test that too.
"""

# %%
simpson(x=x_ticks, y=norm_dist)

# %% [markdown]
r"""
If we wanted to find the fraction of birth weights between 1 and 2 kgs, we could do:
"""

# %%
x_between_1_2 = np.linspace(1, 2, 201)
y_between_1_2 = norm.pdf(x_between_1_2, trim_mean, trim_std)
simpson(x=x_between_1_2, y=y_between_1_2)

# %% [markdown]
r"""
We can also find the fraction by $F_X(2) - F_X(1)$
"""

# %%
norm.cdf(2, trim_mean, trim_std) - norm.cdf(1, trim_mean, trim_std)

# %% [markdown]
r"""
## Kernel Density Estimation (KDE)

We can use KDE to estimate a PDF from the discrete data.
"""

# %%
birth_weights = birth["totalwgt_kg"].dropna()
trimmed_weight = pd.Series(trimboth(birth_weights, 0.02))

# %%
np.random.seed(3)
n = 500
sample_birth_weights = trimmed_weight.sample(n)
sample_birth_weights

# %%
weight_kde_pmf = pd.Series(1 / n, index=sample_birth_weights)
weight_kde_pmf
len(weight_kde_pmf)

# %% [markdown]
r"""
We can find the optimal $h$ using _Scott's rule of thumb_.

$$
h \approx 1.06 \cdot \hat{\sigma}n^{\frac{1}{5}}
$$
"""

# %%
x_vals = np.linspace(0, 7, 1000)
h = 1.06 * sample_birth_weights.std() * len(sample_birth_weights) ** (-1 / 5)
h

# %%
norm_dist = norm.pdf(
    x_vals, loc=sample_birth_weights.mean(), scale=sample_birth_weights.std()
)
norm_pdf = pd.Series(norm_dist, index=x_vals)
norm_pdf

# %%
fig, ax = plt.subplots(1, 3, figsize=(16, 4))
ax[0].bar(weight_kde_pmf.index, weight_kde_pmf, width=0.01, color="red", alpha=0.6)
kde_total = np.zeros_like(x_vals)
for point in sample_birth_weights:
    kernel = norm.pdf(x_vals, loc=point, scale=h) * (1 / n)
    ax[1].plot(x_vals, kernel, color="gray", alpha=0.5, linestyle="-", linewidth=0.1)
    kde_total += kernel

ax[2].plot(norm_pdf.index, norm_pdf, color="blue", alpha=0.5)
ax[2].plot(x_vals, kde_total, color="red")

ax[0].set_xlabel("Weight")
ax[0].set_ylabel(f"1/{n}")
ax[0].set_title("First step - Data points for each weight")

ax[1].set_title("Second Step - Normal distribution PDFs for each weight")

ax[2].set_xlabel("Weight (kg)")
ax[2].set_ylabel("Probability")
ax[2].set_title("KDE plot of weights")


plt.show()

# %% [markdown]
r"""
We have our KDE plot. In some cases, like here where we have too many data points, it is better to use KDE plot instead of a histogram.

We can calculate the area below our KDE plot to ensure that our KDE plot is also a PDF.
"""

# %%
simpson(x=x_vals, y=kde_total)

# %% [markdown]
r"""
## The Distribution Framework

At this point, we have a complete set of ways to represent distributions: PMFs, CDFs and PDFs. Now, let's learn how to transform one to another.

<img src="/notes/assets/distribution_framework.png" height="300"/>
"""
