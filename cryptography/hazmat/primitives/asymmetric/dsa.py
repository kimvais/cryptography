# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

import six

from cryptography import utils


def generate_parameters(key_size, backend):
    return backend.generate_dsa_parameters(key_size)


def generate_private_key(key_size, backend):
    return backend.generate_dsa_private_key_and_parameters(key_size)


def _check_dsa_parameters(parameters):
    if (utils.bit_length(parameters.p),
        utils.bit_length(parameters.q)) not in (
            (1024, 160),
            (2048, 256),
            (3072, 256)):
        raise ValueError("p and q lengths must be "
                         "one of these pairs (1024, 160) or (2048, 256) "
                         "or (3072, 256).")

    if not (1 < parameters.g < parameters.p):
        raise ValueError("g, p don't satisfy 1 < g < p.")


def _check_dsa_private_numbers(numbers):
    parameters = numbers.public_numbers.parameter_numbers
    _check_dsa_parameters(parameters)
    if numbers.x <= 0 or numbers.x >= parameters.q:
        raise ValueError("x must be > 0 and < q.")

    if numbers.public_numbers.y != pow(parameters.g, numbers.x, parameters.p):
        raise ValueError("y must be equal to (g ** x % p).")


class DSAParameterNumbers(object):
    def __init__(self, p, q, g):
        if (
            not isinstance(p, six.integer_types) or
            not isinstance(q, six.integer_types) or
            not isinstance(g, six.integer_types)
        ):
            raise TypeError(
                "DSAParameterNumbers p, q, and g arguments must be integers."
            )

        self._p = p
        self._q = q
        self._g = g

    @property
    def p(self):
        return self._p

    @property
    def q(self):
        return self._q

    @property
    def g(self):
        return self._g

    def parameters(self, backend):
        return backend.load_dsa_parameter_numbers(self)


class DSAPublicNumbers(object):
    def __init__(self, y, parameter_numbers):
        if not isinstance(y, six.integer_types):
            raise TypeError("DSAPublicNumbers y argument must be an integer.")

        if not isinstance(parameter_numbers, DSAParameterNumbers):
            raise TypeError(
                "parameter_numbers must be a DSAParameterNumbers instance."
            )

        self._y = y
        self._parameter_numbers = parameter_numbers

    @property
    def y(self):
        return self._y

    @property
    def parameter_numbers(self):
        return self._parameter_numbers

    def public_key(self, backend):
        return backend.load_dsa_public_numbers(self)


class DSAPrivateNumbers(object):
    def __init__(self, x, public_numbers):
        if not isinstance(x, six.integer_types):
            raise TypeError("DSAPrivateNumbers x argument must be an integer.")

        if not isinstance(public_numbers, DSAPublicNumbers):
            raise TypeError(
                "public_numbers must be a DSAPublicNumbers instance."
            )
        self._public_numbers = public_numbers
        self._x = x

    @property
    def x(self):
        return self._x

    @property
    def public_numbers(self):
        return self._public_numbers

    def private_key(self, backend):
        return backend.load_dsa_private_numbers(self)
