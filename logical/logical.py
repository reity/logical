"""Logical operators as callable tuples.

Callable subclass of tuple for representing logical
operators/connectives based on their truth tables.
"""

from __future__ import annotations
import doctest
import itertools
import math

class logical(tuple):
    """
    The list of unary and binary logical operations
    represented as the output columns of truth tables
    where the input column pairs are sorted in
    ascending dictionary order:

    * (0, 0) is UNARY FALSE
    * (0, 1) is IDENTITY
    * (1, 0) is NOT
    * (1, 1) is UNARY TRUE

    * (0, 0, 0, 0) is BINARY FALSE
    * (0, 0, 0, 1) is AND
    * (0, 0, 1, 0) is NIMP (i.e., >)
    * (0, 0, 1, 1) is FST (first/left-hand input)
    * (0, 1, 0, 0) is NIF (i.e., <)
    * (0, 1, 0, 1) is SND (second/right-hand input)
    * (0, 1, 1, 0) is XOR (i.e., !=)
    * (0, 1, 1, 1) is OR
    * (1, 0, 0, 0) is NOR
    * (1, 0, 0, 1) is XNOR (i.e., ==)
    * (1, 0, 1, 0) is NSND (negation of second input)
    * (1, 0, 1, 1) is IF (i.e., >=)
    * (1, 1, 0, 0) is NFST (negation of first input)
    * (1, 1, 0, 1) is IMP (i.e., <=)
    * (1, 1, 1, 0) is NAND
    * (1, 1, 1, 1) is BINARY TRUE

    >>> logical((1, 0)) == logical((1, 0))
    True
    >>> logical((1, 0)) == logical((0, 1))
    False
    >>> logical((1, 0))[1]
    0
    """

    names = {
        (0, 0): 'uf',
        (0, 1): 'id',
        (1, 0): 'not',
        (1, 1): 'ut',
        (0, 0, 0, 0): 'bf',
        (0, 0, 0, 1): 'and',
        (0, 0, 1, 0): 'nimp',
        (0, 0, 1, 1): 'fst',
        (0, 1, 0, 0): 'nif',
        (0, 1, 0, 1): 'snd',
        (0, 1, 1, 0): 'xor',
        (0, 1, 1, 1): 'or',
        (1, 0, 0, 0): 'nor',
        (1, 0, 0, 1): 'xnor',
        (1, 0, 1, 0): 'nsnd',
        (1, 0, 1, 1): 'if',
        (1, 1, 0, 0): 'nfst',
        (1, 1, 0, 1): 'imp',
        (1, 1, 1, 0): 'nand',
        (1, 1, 1, 1): 'bt'
    }

    def __call__(self: logical, *arguments) -> int:
        """
        Apply the operator to an input tuple.

        >>> logical((1, 0))(1)
        0
        >>> logical((1, 0, 0, 1))(0, 0)
        1
        >>> logical((1, 0, 0, 1))(1, 1)
        1
        >>> logical((1, 0, 0, 1))(1, 0)
        0
        >>> logical((1, 0, 0, 1))(0, 1)
        0
        >>> logical((1, 0, 0, 1, 0, 1, 0, 1))(1, 1, 0)
        0
        """
        if len(arguments) == 1: # pylint: disable=R1705
            return self[[0, 1].index(arguments[0])]
        elif len(arguments) == 2:
            return self[[(0, 0), (0, 1), (1, 0), (1, 1)].index(tuple(arguments))]
        else:
            inputs = list(itertools.product(*[(0, 1)]*self.arity()))
            return self[inputs.index(tuple(arguments))]

    def name(self: logical) -> str:
        """
        Typical name for the operator.

        >>> logical((1, 0, 0, 1)).name()
        'xnor'
        >>> len([o.name for o in logical.unary])
        4
        >>> len([o.name for o in logical.binary])
        16
        """
        return dict(logical.names)[self]

    def arity(self: logical) -> int:
        """
        Arity of the operator.

        >>> logical((1, 0)).arity()
        1
        >>> logical((1, 0, 0, 1)).arity()
        2
        """
        return int(math.log2(len(self)))

# All unary and binary operators as named class constants.
logical.uf_ = logical((0, 0))
logical.id_ = logical((0, 1))
logical.not_ = logical((1, 0))
logical.ut_ = logical((1, 1))
logical.bf_ = logical((0, 0, 0, 0))
logical.and_ = logical((0, 0, 0, 1))
logical.nimp_ = logical((0, 0, 1, 0))
logical.fst_ = logical((0, 0, 1, 1))
logical.nif_ = logical((0, 1, 0, 0))
logical.snd_ = logical((0, 1, 0, 1))
logical.xor_ = logical((0, 1, 1, 0))
logical.or_ = logical((0, 1, 1, 1))
logical.nor_ = logical((1, 0, 0, 0))
logical.xnor_ = logical((1, 0, 0, 1))
logical.nsnd_ = logical((1, 0, 1, 0))
logical.if_ = logical((1, 0, 1, 1))
logical.nfst_ = logical((1, 1, 0, 0))
logical.imp_ = logical((1, 1, 0, 1))
logical.nand_ = logical((1, 1, 1, 0))
logical.bt_ = logical((1, 1, 1, 1))

# All unary and binary operators as top-level constants.
uf_ = logical.uf_
id_ = logical.id_
not_ = logical.not_
ut_ = logical.ut_
bf_ = logical.bf_
and_ = logical.and_
nimp_ = logical.nimp_
fst_ = logical.fst_
nif_ = logical.nif_
snd_ = logical.snd_
xor_ = logical.xor_
or_ = logical.or_
nor_ = logical.nor_
xnor_ = logical.xnor_
nsnd_ = logical.nsnd_
if_ = logical.if_
nfst_ = logical.nfst_
imp_ = logical.imp_
nand_ = logical.nand_
bt_ = logical.bt_

# Useful containers.
logical.unary = {uf_, id_, not_, ut_}
logical.binary = {
    bf_,
    and_, nimp_, fst_, nif_, snd_, xor_, or_,
    nor_, xnor_, nsnd_, if_, nfst_, imp_, nand_,
    bt_
}
logical.every = logical.unary | logical.binary

unary = logical.unary
binary = logical.binary
every = logical.every

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
