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
# pylint: disable=invalid-name

import logging
from typing import Any, Dict

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split


import numpy as np
import pandas as pd


def train_model(X, y, max_depth, n_estimators):
    """Train a simple gradient boosting regressor
    """
    reg = GradientBoostingRegressor(max_depth=3, n_estimators=n_estimators)
    reg.fit(X, y)
    return reg


def predict(model, test_x):
    """Node for making predictions given a pre-trained model and a test set.
    """
    return model.predict(test_x)


def report_accuracy(predictions, y_test):
    """Node for reporting the accuracy of the predictions performed by the
    previous node. Notice that this function has no outputs, except logging.
    """

    accuracy = np.sum(np.abs(predictions-y_test)/y_test) / len(y_test)
    # Log the accuracy of the model
    log = logging.getLogger(__name__)
    log.info("Model Average MAE on test set: %0.2f%%", accuracy * 100)


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

def split_gamma_prime(complete_preprocess_alloys_gamma_prime_table: pd.DataFrame,
        test_ratio: float, seed: int):
    """Split data for gamma prime constant model training"""
    li = list(complete_preprocess_alloys_gamma_prime_table.keys())
    X  = complete_preprocess_alloys_gamma_prime_table[li[:-1]].values
    y  = complete_preprocess_alloys_gamma_prime_table[li[-1]].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=seed)
    return dict(
        train_x_gamma_prime=X_train,
        train_y_gamma_prime=y_train,
        test_x_gamma_prime=X_test,
        test_y_gamma_prime=y_test,
    )
