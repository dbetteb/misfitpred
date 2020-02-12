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


def predict_mismatch(GammaModel, GammaPrimeModel, Alloy,Tmin,Tmax):
    temps = np.linspace(Tmin,Tmax,5)
    GammaElem = ['Nickel', 'Cobalt', 'Chromium', 'Molybdenum', 'Tungsten', 'Aluminium', 'Titanium', 'Niobium', 'Tantalum', 'Hafnium', 'Rhenium', 'Vanadium', 'Ferrite', 'Galium', 'Copper', 'Gold']
    GammaPrimElem = ['Nickel', 'Cobalt', 'Chromium', 'Molybdenum', 'Tungsten', 'Aluminium', 'Titanium', 'Niobium', 'Tantalum', 'Hafnium', 'Rhenium', 'Vanadium', 'Ferrite', 'Galium']
    x_gamma = []
    for temp in temps:
        li = [temp]
        for elem in GammaElem:
            li.append(Alloy[elem])
        x_gamma.append(li)
    x_gamma_prime = []
    for temp in temps:
        li = [temp]
        for elem in GammaPrimElem:
            li.append(Alloy[elem])
        x_gamma_prime.append(li)
    AlphaGamma = GammaModel.predict(x_gamma)
    AlphaGammaPrime = GammaPrimeModel.predict(x_gamma_prime)
    delta = (AlphaGammaPrime-AlphaGamma)/(AlphaGammaPrime+AlphaGamma)
    return temps, delta


Alloys = dict()

Alloys['SRR99'] = dict([
    ('Nickel',0.687),
    ('Chromium',0.085),
    ('Cobalt',0.05),
    ('Molybdenum',0.00),
    ('Tungsten',0.095),
    ('Tantalum',0.028),
    ('Niobium',0.00),
    ('Aluminium',0.055),
    ('Titanium',0.0),
    ('Hafnium',0.00),
    ('Rhenium',0.00),
    ('Vanadium',0.00),
    ('Ferrite',0.00),
    ('Galium',0.00),
    ('Copper',0.00),
    ('Gold',0.00),
    ])

Alloys['CMSX-4'] = dict([
    ('Nickel',0.622),
    ('Chromium',0.065),
    ('Cobalt',0.10),
    ('Molybdenum',0.006),
    ('Tungsten',0.06),
    ('Tantalum',0.06),
    ('Niobium',0.00),
    ('Aluminium',0.056),
    ('Titanium',0.000),
    ('Hafnium',0.001),
    ('Rhenium',0.03),
    ('Vanadium',0.00),
    ('Ferrite',0.00),
    ('Galium',0.00),
    ('Copper',0.00),
    ('Gold',0.00),
    ])




Alloys['CMSX-10'] = dict([
    ('Nickel',0.6977),
    ('Chromium',0.02),
    ('Cobalt',0.03),
    ('Molybdenum',0.004),
    ('Tungsten',0.05),
    ('Tantalum',0.08),
    ('Niobium',0.001),
    ('Aluminium',0.057),
    ('Titanium',0.00),
    ('Hafnium',0.0003),
    ('Rhenium',0.06),
    ('Vanadium',0.00),
    ('Ferrite',0.00),
    ('Galium',0.00),
    ('Copper',0.00),
    ('Gold',0.00),
    ])


Alloys['MISFIT1'] = dict([
    ('Nickel',0.5011),
    ('Cobalt',0.1907),
    ('Chromium',0.2018),
    ('Molybdenum',0.0079),
    ('Tungsten',0.0244),
    ('Aluminium',0.0392),
    ('Titanium',0.0022),
    ('Niobium',0.0),
    ('Tantalum',0.0059),
    ('Hafnium',0.0001),
    ('Rhenium',0.0267),
    ('Vanadium',0.0),
    ('Ferrite',0.0),
    ('Galium',0.0),
    ('Copper',0.0),
    ('Gold',0.0),
    ])

Alloys['AM1'] = dict([
    ('Nickel',0.638),
    ('Cobalt',0.065),
    ('Chromium',0.078),
    ('Molybdenum',0.02),
    ('Tungsten',0.0057),
    ('Aluminium',0.052),
    ('Titanium',0.011),
    ('Niobium',0.0),
    ('Tantalum',0.079),
    ('Hafnium',0.00),
    ('Rhenium',0.0),
    ('Vanadium',0.0),
    ('Ferrite',0.0),
    ('Galium',0.0),
    ('Copper',0.0),
    ('Gold',0.0),
    ])
