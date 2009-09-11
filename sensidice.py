"""
sensidice - a module to aid in creating passphrases.

In stead of using the original Diceware method, one could use this module in
conjuction with lists of words of different parts of speech to convert random
numbers to structured sentences.

Copyright (c) 2009, Amir Yalon. All rights reserved.

"""


class DigitSeqCat:

    """Two sequences of digits concatenated dynamically.
    
    >>> dsq = DigitSeqCat('01234', '56789')
    >>> len(dsq)
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

    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def __len__(self):
        return len(self.seq1) + len(self.seq2)

    def __getitem__(self, key):
        len1 = len(self.seq1)
        if key < len1:
            return self.seq1[key]
        len2 = len(self.seq2)
        key -= len1
        if key < len2:
            return self.seq2[key]
        raise IndexError


class DigitSeqCartes:

    """Two sequences of digits cartesian-multiplied dynamically.
    
    >>> dsq = DigitSeqCartes('01234', 'abcdef')
    >>> len(dsq)
    30
    >>> dsq[0]
    ('0', 'a')
    >>> dsq[29]
    ('4', 'f')
    >>> dsq[31]
    ... #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    IndexError:
    
    """

    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def __len__(self):
        return len(self.seq1) * len(self.seq2)

    def __getitem__(self, key):
        len2 = len(self.seq2)
        return (self.seq1[key // len2], self.seq2[key % len2])


class Digital:

    """A digital place with its own base and list of digits.
    
    >>> d = Digital('0123456789')
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

    """

    def __init__(self, digits):
        self.digits = digits

    def __call__(self, number):
        res = []
        base = len(self.digits)
        while True:
            index = number % base
            try:
                res[0:0] = self.digits[index]
            except TypeError:
                res.insert(0, self.digits[index])
            if number < base:
                break
            number //= base
        return res

    def __add__(self, other):
        if not isinstance(other, Digital):
            return NotImplemented
        return Digital(DigitSeqCat(self.digits, other.digits))

    def __mul__(self, other):
        if not isinstance(other, Digital):
            return NotImplemented
        return Digital(DigitSeqCartes(self.digits, other.digits))

