# Copyright 2018-2019 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

PLEASE DELETE THIS FILE ONCE YOU START WORKING ON YOUR OWN PROJECT!
"""

from typing import Any, Dict, List

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split

def _parse_percentage(x: float):
    return float(x)/100.

def preprocess_alloys_table(alloys_table: pd.DataFrame):
    """Preprocess alloys compositions

       Args:
            alloys_table: temperature and compositions for alloys (DataFrame)
       Returns:
            alloys_table_processed: temperature and compositions (in real) for alloys (DataFrame)
    """
    elements = alloys_table.keys()[1:]
    # Keep all chemical elements
    print("Toto")
    for elem in elements:
        alloys_table[elem] = alloys_table[elem].apply(_parse_percentage)

    return alloys_table

def preprocess_alloys_gamma_table(alloys_gamma_table: pd.DataFrame):
    """Preprocess alloys for gamma lattice constant prediction"""
    return preprocess_alloys_table(alloys_gamma_table)

def preprocess_alloys_gamma_prime_table(alloys_gamma_prime_table: pd.DataFrame):
    """Preprocess alloys for gamma prime lattice constant prediction"""
    return preprocess_alloys_table(alloys_gamma_prime_table)

def augment_preprocess_alloys_gamma_table(preprocess_alloys_gamma_table: pd.DataFrame,
        alpha_gamma: pd.DataFrame):
    """Add Alpha Gamma result to preprocessed alloys gamma table"""
    preprocess_alloys_gamma_table['AlphaGamma'] = alpha_gamma.values
    return preprocess_alloys_gamma_table

def augment_preprocess_alloys_gamma_prime_table(preprocess_alloys_gamma_prime_table: pd.DataFrame,
        alpha_gamma_prime: pd.DataFrame):
    """Add Alpha Gamma Prime result to preprocessed alloys gamma prime table"""
    preprocess_alloys_gamma_prime_table['AlphaGammaPrime'] = alpha_gamma_prime.values
    return preprocess_alloys_gamma_prime_table

def plot_corr_gamma(alloys_table: pd.DataFrame, plot_corr: bool):
    """Plot correlations between alloys compositions"""
    if plot_corr:
        elem = alloys_table.shape[1]-1
        corr = alloys_table[list(alloys_table.keys()[1:])].corr()
        mask = np.triu(np.ones_like(corr, dtype=np.bool))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        f, ax = plt.subplots(figsize=(11, 9))
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
        plt.title(r"Correlation of the $16$ chemical elements for $\alpha_{\gamma}$", fontsize=14)
        return plt
    else:
        return None

def plot_corr_gamma_prime(alloys_table: pd.DataFrame, plot_corr: bool):
    """Plot correlations between alloys compositions"""
    if plot_corr:
        elem = alloys_table.shape[1]-1
        corr = alloys_table[list(alloys_table.keys()[1:])].corr()
        mask = np.triu(np.ones_like(corr, dtype=np.bool))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        f, ax = plt.subplots(figsize=(11, 9))
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
        plt.title(r"Correlation of the $14$ chemical elements for $\alpha_{\gamma'}$", fontsize=14)
        return plt
    else:
        return None

def merge_alloys(complete_preprocess_alloys_gamma_table: pd.DataFrame,
        complete_preprocess_alloys_gamma_prime_table: pd.DataFrame):
    """Merge all alloys into one table for analytics"""
    li = list(complete_preprocess_alloys_gamma_prime_table.keys()[:-1])
    df = pd.merge(complete_preprocess_alloys_gamma_table,
        complete_preprocess_alloys_gamma_prime_table, on=li, how='outer')
    df['Phase'] = 0
    Phase = []
    for rows in df.iterrows():
        if np.isnan(rows[1].AlphaGamma) & ~np.isnan(rows[1].AlphaGammaPrime):
            Phase.append(r"$\gamma'$")
        elif ~np.isnan(rows[1].AlphaGamma) & np.isnan(rows[1].AlphaGammaPrime):
            Phase.append(r"$\gamma$")
        else:
            Phase.append(r"$\gamma$ and $\gamma'$")
    df['Phase'] = Phase
    return df

def pairplot_merge(merge_table: pd.DataFrame,hist_vars: List):
    """Pairplot for different alloys compositions"""
    sns.pairplot(merge_table, vars=hist_vars, hue="Phase", corner=True, diag_kind="kde")
    plt.subplots_adjust(left=0.07, bottom=0.07)
    return plt

def split_gamma(complete_preprocess_alloys_gamma_table: pd.DataFrame,
        test_ratio: float, seed: int):
    """Split data for gamma constant model training"""
    li = list(complete_preprocess_alloys_gamma_table.keys())
    X  = complete_preprocess_alloys_gamma_table[li[:-1]].values
    y  = complete_preprocess_alloys_gamma_table[li[-1]].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=seed)
    return dict(
        train_x_gamma=X_train,
        train_y_gamma=y_train,
        test_x_gamma=X_test,
        test_y_gamma=y_test,
    )
