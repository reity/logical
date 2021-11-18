"""
Callable subclass of tuple for representing logical
operators/connectives based on their truth tables.

All four unary and all sixteen binary operators are
available as attributes of the :obj:`logical` class,
and also as constants. Likewise, the three sets of
operators :obj:`logical.unary`, :obj:`logical.binary`,
and :obj:`logical.every` are available both as
attributes of :obj:`logical` and as constants.
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

    * ``(0, 0)`` is **UNARY FALSE**
    * ``(0, 1)`` is **IDENTITY**
    * ``(1, 0)`` is **NOT**
    * ``(1, 1)`` is **UNARY TRUE**

    * ``(0, 0, 0, 0)`` is **BINARY FALSE**
    * ``(0, 0, 0, 1)`` is **AND**
    * ``(0, 0, 1, 0)`` is **NIMP** (*i.e.*, ``>``)
    * ``(0, 0, 1, 1)`` is **FST** (*i.e.*, first/left-hand input)
    * ``(0, 1, 0, 0)`` is **NIF** (*i.e.*, ``<``)
    * ``(0, 1, 0, 1)`` is **SND** (*i.e.*, second/right-hand input)
    * ``(0, 1, 1, 0)`` is **XOR** (*i.e.*, ``!=``)
    * ``(0, 1, 1, 1)`` is **OR**
    * ``(1, 0, 0, 0)`` is **NOR**
    * ``(1, 0, 0, 1)`` is **XNOR** (*i.e.*, ``==``)
    * ``(1, 0, 1, 0)`` is **NSND** (*i.e.*, negation of second input)
    * ``(1, 0, 1, 1)`` is **IF** (*i.e.*, ``>=``)
    * ``(1, 1, 0, 0)`` is **NFST** (*i.e.*, negation of first input)
    * ``(1, 1, 0, 1)`` is **IMP** (*i.e.*, ``<=``)
    * ``(1, 1, 1, 0)`` is **NAND**
    * ``(1, 1, 1, 1)`` is **BINARY TRUE**

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
    """Typical concise names for all unary and binary operators."""

    every = None
    """Set of all unary and binary operators."""

    unary = None
    """Set of all unary operators."""

    binary = None
    """Set of all binary operators."""

    def __call__(self: logical, *arguments) -> int:
        """
        Apply this operator to an input tuple.

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
        Return the typical concise name for this operator.

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
        Return the arity of this operator.

        >>> logical((1, 0)).arity()
        1
        >>> logical((1, 0, 0, 1)).arity()
        2
        """
        return int(math.log2(len(self)))

    uf_ = None
    """
    Unary **FALSE** (constant) operation.

    +-------+------------+
    | ``x`` | ``uf_(x)`` |
    +-------+------------+
    | ``0`` | ``0``      |
    +-------+------------+
    | ``1`` | ``0``      |
    +-------+------------+
    """

    id_ = None
    """
    Unary **IDENTITY** operation.

    +-------+------------+
    | ``x`` | ``id_(x)`` |
    +-------+------------+
    | ``0`` | ``0``      |
    +-------+------------+
    | ``1`` | ``1``      |
    +-------+------------+
    """

    not_ = None
    """
    Unary **NOT** operation (*i.e.*, negation).

    +-------+-------------+
    | ``x`` | ``not_(x)`` |
    +-------+-------------+
    | ``0`` | ``1``       |
    +-------+-------------+
    | ``1`` | ``0``       |
    +-------+-------------+
    """

    ut_ = None
    """
    Unary **TRUE** (constant) operation.

    +-------+------------+
    | ``x`` | ``ut_(x)`` |
    +-------+------------+
    | ``0`` | ``1``      |
    +-------+------------+
    | ``1`` | ``1``      |
    +-------+------------+
    """

    bf_ = None
    """
    Binary **FALSE** (constant) operation.

    +------------+---------------+
    | ``(x, y)`` | ``bf_(x, y)`` |
    +------------+---------------+
    | ``(0, 0)`` | ``0``         |
    +------------+---------------+
    | ``(0, 1)`` | ``0``         |
    +------------+---------------+
    | ``(1, 0)`` | ``0``         |
    +------------+---------------+
    | ``(1, 1)`` | ``0``         |
    +------------+---------------+
    """

    and_ = None
    """
    Binary **AND** operation (*i.e.*, conjunction).

    +------------+----------------+
    | ``(x, y)`` | ``and_(x, y)`` |
    +------------+----------------+
    | ``(0, 0)`` | ``0``          |
    +------------+----------------+
    | ``(0, 1)`` | ``0``          |
    +------------+----------------+
    | ``(1, 0)`` | ``0``          |
    +------------+----------------+
    | ``(1, 1)`` | ``1``          |
    +------------+----------------+
    """

    nimp_ = None
    """
    Binary **NIMP** operation (*i.e.*, ``>``).

    +------------+-----------------+
    | ``(x, y)`` | ``nimp_(x, y)`` |
    +------------+-----------------+
    | ``(0, 0)`` | ``0``           |
    +------------+-----------------+
    | ``(0, 1)`` | ``0``           |
    +------------+-----------------+
    | ``(1, 0)`` | ``1``           |
    +------------+-----------------+
    | ``(1, 1)`` | ``0``           |
    +------------+-----------------+
    """

    fst_ = None
    """
    Binary **FST** operation (*i.e.*, first/left-hand input).

    +------------+----------------+
    | ``(x, y)`` | ``fst_(x, y)`` |
    +------------+----------------+
    | ``(0, 0)`` | ``0``          |
    +------------+----------------+
    | ``(0, 1)`` | ``0``          |
    +------------+----------------+
    | ``(1, 0)`` | ``1``          |
    +------------+----------------+
    | ``(1, 1)`` | ``1``          |
    +------------+----------------+
    """

    nif_ = None
    """
    Binary **NIF** operation (*i.e.*, ``<``).

    +------------+----------------+
    | ``(x, y)`` | ``nif_(x, y)`` |
    +------------+----------------+
    | ``(0, 0)`` | ``0``          |
    +------------+----------------+
    | ``(0, 1)`` | ``1``          |
    +------------+----------------+
    | ``(1, 0)`` | ``0``          |
    +------------+----------------+
    | ``(1, 1)`` | ``0``          |
    +------------+----------------+
    """

    snd_ = None
    """
    Binary **SND** operation (*i.e.*, second/right-hand input).

    +------------+----------------+
    | ``(x, y)`` | ``snd_(x, y)`` |
    +------------+----------------+
    | ``(0, 0)`` | ``0``          |
    +------------+----------------+
    | ``(0, 1)`` | ``1``          |
    +------------+----------------+
    | ``(1, 0)`` | ``0``          |
    +------------+----------------+
    | ``(1, 1)`` | ``1``          |
    +------------+----------------+
    """

    xor_ = None
    """
    Binary **XOR** operation (*i.e.*, ``!=``).

    +------------+----------------+
    | ``(x, y)`` | ``xor_(x, y)`` |
    +------------+----------------+
    | ``(0, 0)`` | ``0``          |
    +------------+----------------+
    | ``(0, 1)`` | ``1``          |
    +------------+----------------+
    | ``(1, 0)`` | ``1``          |
    +------------+----------------+
    | ``(1, 1)`` | ``0``          |
    +------------+----------------+
    """

    or_ = None
    """
    Binary **OR** operation (*i.e.*, disjunction).

    +------------+---------------+
    | ``(x, y)`` | ``or_(x, y)`` |
    +------------+---------------+
    | ``(0, 0)`` | ``0``         |
    +------------+---------------+
    | ``(0, 1)`` | ``1``         |
    +------------+---------------+
    | ``(1, 0)`` | ``1``         |
    +------------+---------------+
    | ``(1, 1)`` | ``1``         |
    +------------+---------------+
    """

    nor_ = None
    """
    Binary **NOR** operation.

    +------------+----------------+
    | ``(x, y)`` | ``nor_(x, y)`` |
    +------------+----------------+
    | ``(0, 0)`` | ``1``          |
    +------------+----------------+
    | ``(0, 1)`` | ``0``          |
    +------------+----------------+
    | ``(1, 0)`` | ``0``          |
    +------------+----------------+
    | ``(1, 1)`` | ``0``          |
    +------------+----------------+
    """

    xnor_ = None
    """
    Binary **XNOR** operation (*i.e.*, ``==``).

    +------------+-----------------+
    | ``(x, y)`` | ``xnor_(x, y)`` |
    +------------+-----------------+
    | ``(0, 0)`` | ``1``           |
    +------------+-----------------+
    | ``(0, 1)`` | ``0``           |
    +------------+-----------------+
    | ``(1, 0)`` | ``0``           |
    +------------+-----------------+
    | ``(1, 1)`` | ``1``           |
    +------------+-----------------+
    """

    nsnd_ = None
    """
    Binary **NSND** operation (*i.e.*, negation of second/right-hand input).

    +------------+-----------------+
    | ``(x, y)`` | ``nsnd_(x, y)`` |
    +------------+-----------------+
    | ``(0, 0)`` | ``1``           |
    +------------+-----------------+
    | ``(0, 1)`` | ``0``           |
    +------------+-----------------+
    | ``(1, 0)`` | ``1``           |
    +------------+-----------------+
    | ``(1, 1)`` | ``0``           |
    +------------+-----------------+
    """

    if_ = None
    """
    Binary **IF** operation.

    +------------+---------------+
    | ``(x, y)`` | ``if_(x, y)`` |
    +------------+---------------+
    | ``(0, 0)`` | ``1``         |
    +------------+---------------+
    | ``(0, 1)`` | ``0``         |
    +------------+---------------+
    | ``(1, 0)`` | ``1``         |
    +------------+---------------+
    | ``(1, 1)`` | ``1``         |
    +------------+---------------+
    """

    nfst_ = None
    """
    Binary **NFST** operation (*i.e.*, negation of first/left-hand input).

    +------------+-----------------+
    | ``(x, y)`` | ``nfst_(x, y)`` |
    +------------+-----------------+
    | ``(0, 0)`` | ``1``           |
    +------------+-----------------+
    | ``(0, 1)`` | ``1``           |
    +------------+-----------------+
    | ``(1, 0)`` | ``0``           |
    +------------+-----------------+
    | ``(1, 1)`` | ``0``           |
    +------------+-----------------+
    """

    imp_ = None
    """
    Binary **IMP** operation (*i.e.*, implication or ``<=``).

    +------------+----------------+
    | ``(x, y)`` | ``imp_(x, y)`` |
    +------------+----------------+
    | ``(0, 0)`` | ``1``          |
    +------------+----------------+
    | ``(0, 1)`` | ``1``          |
    +------------+----------------+
    | ``(1, 0)`` | ``0``          |
    +------------+----------------+
    | ``(1, 1)`` | ``1``          |
    +------------+----------------+
    """

    nand_ = None
    """
    Binary **NAND** operation (*i.e.*, negation of conjunction).

    +------------+-----------------+
    | ``(x, y)`` | ``nand_(x, y)`` |
    +------------+-----------------+
    | ``(0, 0)`` | ``1``           |
    +------------+-----------------+
    | ``(0, 1)`` | ``1``           |
    +------------+-----------------+
    | ``(1, 0)`` | ``1``           |
    +------------+-----------------+
    | ``(1, 1)`` | ``0``           |
    +------------+-----------------+
    """

    bt_ = None
    """
    Binary **TRUE** (constant) operation.

    +------------+---------------+
    | ``(x, y)`` | ``bt_(x, y)`` |
    +------------+---------------+
    | ``(0, 0)`` | ``1``         |
    +------------+---------------+
    | ``(0, 1)`` | ``1``         |
    +------------+---------------+
    | ``(1, 0)`` | ``1``         |
    +------------+---------------+
    | ``(1, 1)`` | ``1``         |
    +------------+---------------+
    """

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
