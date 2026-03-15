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
# Estimation
"""

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mode

# %%
sample = pd.Series(np.random.normal(0, 1, size=5000))
sample

# %%
fig, ax = plt.subplots()
ax.hist(sample, bins=np.arange(-4, 4, 0.3))
plt.show()

# %%
np.mean(sample), np.std(sample)

# %% [markdown]
r"""
We didn't have to show it in graph but we can totally say that `np.random.normal` creates normally distributed numbers.
"""


# %%
def make_normal_sample(mu, sigma, n):
    return np.random.normal(mu, sigma, n)


# %%
ns = np.logspace(1, 5).astype(int)

# %% [markdown]
r"""
We are going to use these `n`s to see how the _estimator_ changes when the sample size increases.
"""

# %%
mu = 3.7
sigma = 0.46

# %%
means = [np.mean(make_normal_sample(mu, sigma, n)) for n in ns]
medians = [np.median(make_normal_sample(mu, sigma, n)) for n in ns]

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 3))
axes[0].plot(ns, means)
axes[1].plot(ns, medians)
axes[0].set_ylabel("Sample Mean")
axes[0].set_xlabel("Sample Size")
axes[1].set_ylabel("Sample Median")
axes[1].set_xlabel("Sample Size")
plt.tight_layout()
plt.show()

# %% [markdown]
r"""
Right here, we actually visualized how WLLN (Weak Law of Large Numbers) work. We also saw that in a normal distribution, both mean and median are great estimators; because mean, median and the mode is all equal in a normal distribution. Using mean would be better in this case, since it is more efficient.

**What is an estimator?:** When we say estimator, we are actually trying to say that best estimator of the population parameter as the sample size goes to infinity, where parameter can be anything you want (SD, mean, median etc.).
"""

# %% [markdown]
r"""
Before getting in more deeper into other stuff, I just want to clear out that we are using central tendency measures right now. All of them can be useful in appropriate conditions. However, which one is more useful may depend on the answer we’re looking for. Let’s illustrate this with an example from the real world.
"""

# %% [markdown]
r"""
If we tried to visualize the histogram of the world wealth, since most of the world works for roughly the same pay, but only a few are wealthy, we would see a right-skewed distribution.
"""

# %%
income = np.random.lognormal(9, 2.1, size=1_000_000)
bins = np.linspace(0, 200_000, 100)

# %%
fig, ax = plt.subplots()
ax.hist(income, bins=bins)
ax.set_xlim(0, 200_000)
ax.set_ylabel("Number of people (out of 1 mil.)")
ax.set_xlabel("Wage (dollars)")
plt.tight_layout()
plt.show()

# %% [markdown]
r"""
Let's also visualize the mean, median and the mode of this distribution.
"""

# %%
fig, ax = plt.subplots()
ax.hist(income, bins=bins)
ax.axvline(
    np.mean(income),
    linestyle="--",
    color="blue",
    alpha=0.5,
    label=f"mean ({np.mean(income):.2f})",
)
ax.axvline(
    np.median(income),
    linestyle="--",
    color="red",
    alpha=0.5,
    label=f"median ({np.median(income):.2f})",
)
ax.set_xlim(0, 200_000)
ax.set_ylabel("Number of people (out of 1 mil.)")
ax.set_xlabel("Wage (dollars)")
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
r"""
So comparing the mean and the median, which one would be closer to the answer we would get if we asked people about their wages? It would probably be the median value. Because the mean is very sensitive to outliers, and we have ultra-rich people in the distribution, we cannot rely on it.
"""

# %% [markdown]
r"""
So what does this have to do with estimation? Nothing. I just wanted to make it clearer that the fact we can obtain the same result using both the mean and the median above is a property of the normal distribution. Let's keep going with the estmiation.
"""
