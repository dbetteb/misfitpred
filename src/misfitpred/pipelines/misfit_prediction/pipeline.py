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
"""Data engineering pipeline defition
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    preprocess_alloys_gamma_table,
    preprocess_alloys_gamma_prime_table,
    augment_preprocess_alloys_gamma_table,
    augment_preprocess_alloys_gamma_prime_table,
    plot_corr_gamma,
    plot_corr_gamma_prime,
    merge_alloys,
    pairplot_merge,
    )
def create_pipeline(**kwargs):
    return Pipeline(
        [
        node(
            func=preprocess_alloys_gamma_table,
            inputs="AlloysGamma",
            outputs="PreprocessedAlloysGamma",
            name="Preprocessing_Alloys_Gamma_Table",
        ),
        node(
            func=preprocess_alloys_gamma_prime_table,
            inputs="AlloysGammaPrime",
            outputs="PreprocessedAlloysGammaPrime",
            name="Preprocessing_Alloys_Gamma_Prime_Table",
        ),
        node(
            func=augment_preprocess_alloys_gamma_table,
            inputs=["PreprocessedAlloysGamma","AlphaGammaAlloys"],
            outputs="CompletePreprocessedAlloysGamma",
            name="Augmenting_Alloys_Gamma_Table",
        ),
        node(
            func=augment_preprocess_alloys_gamma_prime_table,
            inputs=["PreprocessedAlloysGammaPrime","AlphaGammaPrimeAlloys"],
            outputs="CompletePreprocessedAlloysGammaPrime",
            name="Augmenting_Alloys_Gamma_Prime_Table",
        ),
        node(
            func=plot_corr_gamma,
            inputs=["AlloysGamma","params:plot_corr"],
            outputs="CorrelationPlotsAlloysGamma",
            name="Plotting_Correlation_Alloys_Gamma",
        ),
        node(
            func=plot_corr_gamma_prime,
            inputs=["AlloysGammaPrime","params:plot_corr"],
            outputs="CorrelationPlotsAlloysGammaPrime",
            name="Plotting_Correlation_Alloys_Gamma_Prime",
        ),
        node(
            func=merge_alloys,
            inputs=["CompletePreprocessedAlloysGamma","CompletePreprocessedAlloysGammaPrime"],
            outputs="MasterAlloys",
            name="Merging all alloys",
        ),
        node(
            func=pairplot_merge,
            inputs=["MasterAlloys","params:hist_vars"],
            outputs="PairPlotsAlloys",
            name="Pairplot for Alloys",
        ),
        ]
    )
