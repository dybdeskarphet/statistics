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
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import trimboth, norm
from scipy.integrate import simpson

# %% [markdown]
r"""
We start with the PDF of the normal distribution. Formula of normal distribution PDF is:

$$
\frac {1}{\sqrt {2\pi \sigma ^{2}}}}e^{-{\frac {(x-\mu )^{2}}{2\sigma ^{2}}}
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
