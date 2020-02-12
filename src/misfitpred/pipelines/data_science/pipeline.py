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

from kedro.pipeline import Pipeline, node

from .nodes import (
        predict,
        report_accuracy,
        train_model,
        split_gamma,
        split_gamma_prime,
        )



def create_pipeline(**kwargs):
    return Pipeline(
        [
        node(
            func=split_gamma,
            inputs=["CompletePreprocessedAlloysGamma","params:test_data_ratio","params:random_seed"],
            outputs=dict(
                    train_x_gamma="train_x_gamma",
                    train_y_gamma="train_y_gamma",
                    test_x_gamma="test_x_gamma",
                    test_y_gamma="test_y_gamma",
                ),
            name="Split data for model training for gamma prediction",
        ),
        node(
            func=split_gamma_prime,
            inputs=["CompletePreprocessedAlloysGammaPrime","params:test_data_ratio","params:random_seed"],
            outputs=dict(
                    train_x_gamma_prime="train_x_gamma_prime",
                    train_y_gamma_prime="train_y_gamma_prime",
                    test_x_gamma_prime="test_x_gamma_prime",
                    test_y_gamma_prime="test_y_gamma_prime",
                ),
            name="Split data for model training for gamma prime prediction",
        ),
            node(
                func=train_model,
                inputs=["train_x_gamma", "train_y_gamma", "params:max_depth","params:n_estimators"],
                outputs="GammaModel",
                name="Training model for gamma lattice constant prediction"
            ),
            node(
                func=predict,
                inputs=["GammaModel", "test_x_gamma"],
                outputs="predictions_gamma",
                name="prediction for test basis for gamma lattice constant"
            ),
            node(
            func=report_accuracy,
            inputs=["predictions_gamma", "test_y_gamma"],
            outputs=None,
            name="accuracy metrics for gamma lattice constant"
            ),
            node(
                func=train_model,
                inputs=["train_x_gamma_prime", "train_y_gamma_prime", "params:max_depth","params:n_estimators"],
                outputs="GammaPrimeModel",
                name="Training model for gamma prime lattice constant prediction"
            ),
            node(
                func=predict,
                inputs=["GammaPrimeModel", "test_x_gamma_prime"],
                outputs="predictions_gamma_prime",
                name="prediction for test basis for gamma prime lattice constant"
            ),
            node(
            func=report_accuracy,
            inputs=["predictions_gamma_prime", "test_y_gamma_prime"],
            outputs=None,
            name="accuracy metrics for gamma prime lattice constant"
            ),
        ]
    )
