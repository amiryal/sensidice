# Copyright 2009 Amir Yalon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
sensidice: a module to aid in creating sensible passphrases using dice.

In stead of using the original method (http://diceware.com/), one could use this
module in conjuction with a large parts-of-speech database to convert random
numbers to structured sentences.

"""


def flatprepend(mutable_sequence, item):
    
    """Prepend item to mutable_sequence while keeping it flat.

    If item is a list, then prepend each item from the list in stead of the list
    itself.

    """

    if isinstance(item, list):
        mutable_sequence[0:0] = item
    else:
        mutable_sequence.insert(0, item)
    return mutable_sequence


class Digital:

    """A digital place with its own base and list of digits.
    
    >>> d = Digital('0123456789')
    >>> d.base()
    10
    >>> d(0)
    ['0']
    >>> d(9)
    ['9']
    >>> d(10)
    ['1', '0']
    >>> d = Digital('01') + Digital('ab') * Digital('AB')
    >>> d(0)
    ['0']
    >>> d(1)
    ['1']
    >>> d(2)
    ['a', 'A']
    >>> d(5)
    ['b', 'B']
    >>> d(6)
    ['1', '0']
    >>> d = Digital((0, 1)) * Digital(('a', 'b')) * Digital(['A', 'B'])
    >>> d(0)
    [0, 'a', 'A']
    >>> d = Digital('01') + object()
    ... #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:
    >>> d = object() * Digital('01')
    ... #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:

    Regression testing against overflow:
    >>> import sys
    >>> d = Digital(xrange(sys.maxint)) + Digital(xrange(1))
    >>> d(0)
    [0]

    """

    def __init__(self, digits):
        self.digits = digits

    def base(self):
        return len(self.digits)

    def __getitem__(self, key):
        return self.digits[key]

    def __call__(self, number):
        res = []
        base = self.base()
        while True:
            flatprepend(res, self[number % base])
            if number < base:
                break
            number //= base
        return res

    def __add__(self, other):
        if not isinstance(other, Digital):
            return NotImplemented
        return DigitalCat(self, other)

    def __mul__(self, other):
        if not isinstance(other, Digital):
            return NotImplemented
        return DigitalCartes(self, other)


class DigitalCat(Digital):

    """A digital place where the list of digits is a dynamic concatenation.
    
    >>> dsq = DigitalCat(Digital('01234'), Digital('56789'))
    >>> dsq.base()
    10
    >>> dsq[0]
    '0'
    >>> dsq[9]
    '9'
    >>> dsq[10]
    Traceback (most recent call last):
        ...
    IndexError
    
    """

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def base(self):
        return self.first.base() + self.second.base()

    def __getitem__(self, key):
        firstlen = self.first.base()
        secondlen = self.second.base()
        if key < firstlen:
            return self.first[key]
        key -= firstlen
        if key < secondlen:
            return self.second[key]
        raise IndexError


class DigitalCartes(Digital):

    """A digital place with dynamic cartesian multiplication of digits.
    
    >>> dsq = DigitalCartes(Digital('01234'), Digital('abcdef'))
    >>> dsq.base()
    30
    >>> dsq[0]
    ['0', 'a']
    >>> dsq[29]
    ['4', 'f']
    >>> dsq[31]
    ... #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    IndexError:
    
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def base(self):
        return self.left.base() * self.right.base()

    def __getitem__(self, key):
        rightbase = self.right.base()
        res = []
        flatprepend(res, self.right[key % rightbase])
        flatprepend(res, self.left[key // rightbase])
        return res
