# --
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
# What is Fisher Information?
"""

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm

# %%
np.random.seed(92)

# %%
TRUE_MU = 85.0
KNOWN_SIGMA = 12.0

# %%
api_logs = np.random.normal(loc=TRUE_MU, scale=KNOWN_SIGMA, size=5)
api_logs_50 = np.random.normal(loc=TRUE_MU, scale=KNOWN_SIGMA, size=50)
print(f"Recorded API response times (ms) (n=5): {np.round(api_logs, 2)}")
print(f"Recorded API response times (ms) (n=50): {np.round(api_logs, 2)}")

# %%
mle_mu = np.mean(api_logs)
mle_mu_50 = np.mean(api_logs_50)
print(f"Sample mean (MLE of mu) (n=5) {mle_mu}")
print(f"Sample mean (MLE of mu) (n=50): {mle_mu_50}")

# %%
x_axis = np.linspace(40, 130, 500)

# %%
pdf_curve = norm.pdf(x_axis, loc=mle_mu, scale=KNOWN_SIGMA)
pdf_curve_50 = norm.pdf(x_axis, loc=mle_mu_50, scale=KNOWN_SIGMA)

# %%
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].set_title("n=5")
axes[0].plot(x_axis, pdf_curve)
axes[0].axvline(mle_mu, label="Sample mean", color="green", alpha=0.3)
axes[0].axvline(TRUE_MU, label="Population mean", color="red", alpha=0.3)
axes[0].scatter(api_logs, np.zeros_like(api_logs), color="green", alpha=0.3)
axes[0].legend()
axes[1].set_title("n=50")
axes[1].plot(x_axis, pdf_curve_50)
axes[1].axvline(mle_mu_50, label="Sample mean", color="green", alpha=0.3)
axes[1].axvline(TRUE_MU, label="Population mean", color="red", alpha=0.3)
axes[1].scatter(api_logs_50, np.zeros_like(api_logs_50), color="green", alpha=0.3)
axes[1].legend()
plt.show()

# %%
mu_guesses = np.linspace(0, 150, 500)

# %%
api_logs

# %% [markdown]
r"""
$$
\begin{aligned}
\verb|norm.pdf(api_logs, ...)| : f(x_i \mid \mu, \sigma) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left( -\frac{(x_i - \mu)^2}{2\sigma^2} \right) \\
\verb|np.prod(...)| : L(\mu) = \prod_{i=1}^{5} f(x_i \mid \mu, \sigma) \\
\verb|raw_likelihoods| = \begin{bmatrix} L(\mu_1) \\ L(\mu_2) \\ \vdots \\ L(\mu_{500}) \end{bmatrix}
\end{aligned}
$$
"""

# %%
raw_likelihoods = np.array(
    [np.prod(norm.pdf(api_logs, loc=guess, scale=KNOWN_SIGMA)) for guess in mu_guesses]
)
raw_likelihoods

# %% [markdown]
r"""
$$$
\begin{aligned}
\verb|np.sum(...)| : l(\mu) = \sum_{i=1}^{5} \ln\big(f(x_i \mid \mu, \sigma)\big) \\ 
\verb|log_likelihoods| = \begin{bmatrix} l(\mu_1) \\ l(\mu_2) \\ \vdots \\ l(\mu_{500}) \end{bmatrix}
\end{aligned}
$$$
"""

# %%
log_likelihoods = np.array(
    [
        np.sum(norm.logpdf(api_logs, loc=guess, scale=KNOWN_SIGMA))
        for guess in mu_guesses
    ]
)
log_likelihoods

# %%
log_likelihoods_50 = np.array(
    [
        np.sum(norm.logpdf(api_logs_50, loc=guess, scale=KNOWN_SIGMA))
        for guess in mu_guesses
    ]
)

# %%
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].set_title("n=5")
axes[0].plot(mu_guesses, raw_likelihoods)
axes[0].axvline(mle_mu, color="black", linestyle="--", label=f"Peak = {mle_mu:.1f}ms")
axes[0].set_xlabel("Guessed average latency (ms)")
axes[0].set_ylabel("Probability Product $L(\\theta)=\prod_{i=1}^{n} f(x_i| \\theta)$")
axes[0].legend()

axes[1].set_title("n=5")
axes[1].plot(mu_guesses, log_likelihoods, color="navy")
axes[1].axvline(mle_mu, color="black", linestyle="--", label=f"Peak = {mle_mu:.1f}ms")
axes[1].set_xlabel("Guessed average latency (ms)")
axes[1].set_ylabel("Sum of Log-Probabilities $\sum_{i=1}^{n}ln(f(x_i|\\theta))$")
axes[1].legend()
plt.tight_layout()
plt.show()

# %%
fig, ax = plt.subplots()

plt.plot(mu_guesses, log_likelihoods, color="black", label="initial $\\ell$ (n=5)")
plt.plot(
    mu_guesses,
    log_likelihoods_50,
    color="darkorange",
    linestyle="-",
    label=f"$\ell$ when n=50",
)
plt.legend()
plt.show()

# %% [markdown]
r"""
## Fisher Informaiton
"""

# %%
sample_size_50_universes = np.random.normal(
    loc=TRUE_MU, scale=KNOWN_SIGMA, size=(5000, 50)
)

# %% [markdown]
r"""
We know that the MLE for the mean is the sample mean.
"""

# %%
means_of_universes = np.mean(sample_size_50_universes, axis=1)

# %%
brute_force_variance = np.var(means_of_universes)

# %%
fisher_information = 50 / KNOWN_SIGMA**2

# %%
print(f"Brute force variance of the score function: {1/brute_force_variance}")
print(f"Fisher information: {fisher_information}")
