"""
Callable subclass of the built-in :obj:`tuple <tuple>` type for representing
logical operators and connectives based on their truth tables.

The two nullary, four unary, and sixteen binary operators are available as
attributes of the :obj:`logical` class, and also as constants. Likewise, the
four sets of operators :obj:`logical.nullary`, :obj:`logical.unary`,
:obj:`logical.binary`, and :obj:`logical.every` are available both as attributes
of :obj:`logical` and as exported top-level constants.
"""
from __future__ import annotations
from typing import Sequence, Union
import doctest
from collections.abc import Iterable
import itertools
import math

class logical(tuple):
    """
    Each instance of this class represents a boolean function of ``n`` inputs
    by specifying its output values across all possible inputs. In other words,
    an instance represents the *output column* of a truth table for a function
    (under the assumption that the input vectors to which each output value
    corresponds are sorted in ascending order). Each instance representing a
    function that accepts ``n`` inputs must have length ``2**n``.

    For example, consider the truth table below for a boolean function *f* that
    accepts two inputs:

    +-----+-----+----------------+
    | *x* | *y* | *f* (*x*, *y*) |
    +-----+-----+----------------+
    |  0  |  0  | 1              |
    +-----+-----+----------------+
    |  0  |  1  | 0              |
    +-----+-----+----------------+
    |  1  |  0  | 1              |
    +-----+-----+----------------+
    |  1  |  1  | 0              |
    +-----+-----+----------------+

    The entire function *f* can be represented using the right-most column.
    For the example function *f* defined by the table above, this can be done
    in the manner illustrated below.

    >>> f = logical((1, 0, 1, 0))
    >>> f(0, 1)
    0
    >>> f(1, 0)
    1

    Pre-defined instances are defined for all nullary, unary and binary functions,
    and are available as attributes of this class and as top-level constants:

    * ``(0,)`` = :obj:`logical.nf_` represents **NULLARY FALSE**
    * ``(1,)`` = :obj:`logical.nt_` represents **NULLARY TRUE**

    * ``(0, 0)`` = :obj:`logical.uf_` represents **UNARY FALSE**
    * ``(0, 1)`` = :obj:`logical.id_` represents **IDENTITY**
    * ``(1, 0)`` = :obj:`logical.not_` represents **NOT**
    * ``(1, 1)`` = :obj:`logical.ut_` represents **UNARY TRUE**

    * ``(0, 0, 0, 0)`` = :obj:`logical.bf_` represents **BINARY FALSE**
    * ``(0, 0, 0, 1)`` = :obj:`logical.and_` represents **AND**
    * ``(0, 0, 1, 0)`` = :obj:`logical.nimp_` represents **NIMP** (*i.e.*, ``>``)
    * ``(0, 0, 1, 1)`` = :obj:`logical.fst_` represents **FST** (*i.e.*, first/left-hand input)
    * ``(0, 1, 0, 0)`` = :obj:`logical.nif_` represents **NIF** (*i.e.*, ``<``)
    * ``(0, 1, 0, 1)`` = :obj:`logical.snd_` represents **SND** (*i.e.*, second/right-hand input)
    * ``(0, 1, 1, 0)`` = :obj:`logical.xor_` represents **XOR** (*i.e.*, ``!=``)
    * ``(0, 1, 1, 1)`` = :obj:`logical.or_` represents **OR**
    * ``(1, 0, 0, 0)`` = :obj:`logical.nor_` represents **NOR**
    * ``(1, 0, 0, 1)`` = :obj:`logical.xnor_` represents **XNOR** (*i.e.*, ``==``)
    * ``(1, 0, 1, 0)`` = :obj:`logical.nsnd_` represents **NSND** (*i.e.*, negation of second input)
    * ``(1, 0, 1, 1)`` = :obj:`logical.if_` represents **IF** (*i.e.*, ``>=``)
    * ``(1, 1, 0, 0)`` = :obj:`logical.nfst_` represents **NFST** (*i.e.*, negation of first input)
    * ``(1, 1, 0, 1)`` = :obj:`logical.imp_` represents **IMP** (*i.e.*, ``<=``)
    * ``(1, 1, 1, 0)`` = :obj:`logical.nand_` represents **NAND**
    * ``(1, 1, 1, 1)`` = :obj:`logical.bt_` represents **BINARY TRUE**

    >>> logical.xor_(1, 0)
    1
    >>> and_(1, 0)
    0

    Because this class is derived from the :obj:`tuple <tuple>` type, all
    methods and functions that operate on tuples also work with instances of
    this class.

    >>> logical((1, 0)) == logical((1, 0))
    True
    >>> logical((1, 0)) == logical((0, 1))
    False
    >>> logical((1, 0))[1]
    0
    """
    names: set = {
        (0,): 'nf',
        (1,): 'nt',
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
    """Typical concise names for all nullary, unary, and binary operators."""

    nullary: set = {} # Populated at top-level, after this class definition.
    """Set of all nullary operators."""

    unary: set = {} # Populated at top-level, after this class definition.
    """Set of all unary operators."""

    binary: set = {} # Populated at top-level, after this class definition.
    """Set of all binary operators."""

    every: set = {} # Populated at top-level, after this class definition.
    """Set of all nullary, unary, and binary operators."""

    def __call__(self: logical, *arguments: Union[Sequence[int], Sequence[Sequence[int]]]) -> int:
        """
        Apply the function represented by this instance to zero or more integer
        arguments (where the arguments collectively represent an individual input
        row within a truth table) or to a single iterable of integers (where the
        entries of the iterable represent an individual input row within a truth
        table).

        >>> logical((1,))()
        1
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
        >>> logical((1, 0, 0, 1, 0, 1, 0, 1))([1, 1, 0])
        0
        >>> logical((1, 0, 0, 1, 0, 1, 0, 1))((1, 1, 0))
        0
        >>> logical((1, 0, 0, 1, 0, 1, 0, 1))((1, 1, 0))
        0

        Any attempt to apply an instance to an invalid input raises an exception.

        >>> logical((1, 0))(2.3)
        Traceback (most recent call last):
          ...
        TypeError: expecting zero or more integers or a single iterable of integers
        >>> logical((1, 0))(['abc'])
        Traceback (most recent call last):
          ...
        TypeError: expecting zero or more integers or a single iterable of integers
        >>> logical((1, 0))(2)
        Traceback (most recent call last):
          ...
        ValueError: expecting an integer that is 0 or 1
        """
        if len(arguments) == 1 and isinstance(arguments[0], Iterable):
            arguments = arguments[0]

        if not all(isinstance(argument, int) for argument in arguments):
            raise TypeError(
                'expecting zero or more integers or a single iterable of integers'
            )

        if not all(argument in (0, 1) for argument in arguments):
            raise ValueError(
                'expecting an integer that is 0 or 1'
            )

        if len(arguments) == 0:
            return self[0]
        if len(arguments) == 1: # pylint: disable=R1705
            return self[[0, 1].index(arguments[0])]
        if len(arguments) == 2:
            return self[[(0, 0), (0, 1), (1, 0), (1, 1)].index(tuple(arguments))]

        inputs = list(itertools.product(*[(0, 1)]*self.arity()))
        return self[inputs.index(tuple(arguments))]

    def name(self: logical) -> str:
        """
        Return the typical concise name for this operator.

        >>> logical((0,)).name()
        'nf'
        >>> logical((1, 0, 0, 1)).name()
        'xnor'
        >>> len([o.name for o in logical.nullary])
        2
        >>> len([o.name for o in logical.unary])
        4
        >>> len([o.name for o in logical.binary])
        16
        """
        return dict(logical.names)[self]

    def arity(self: logical) -> int:
        """
        Return the arity of this operator.

        >>> logical((1,)).arity()
        0
        >>> logical((1, 0)).arity()
        1
        >>> logical((1, 0, 0, 1)).arity()
        2
        """
        return int(math.log2(len(self)))

    nf_: logical = None
    """
    Nullary **FALSE** (constant) operation.

    +-----------+
    | ``nf_()`` |
    +-----------+
    | ``0``     |
    +-----------+
    """

    nt_: logical = None
    """
    Nullary **TRUE** (constant) operation.

    +-----------+
    | ``nt_()`` |
    +-----------+
    | ``1``     |
    +-----------+
    """

    uf_: logical = None
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

    id_: logical = None
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

    not_: logical = None
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

    ut_: logical = None
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

    bf_: logical = None
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

    and_: logical = None
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

    nimp_: logical = None
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

    fst_: logical = None
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

    nif_: logical = None
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

    snd_: logical = None
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

    xor_: logical = None
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

    or_: logical = None
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

    nor_: logical = None
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

    xnor_: logical = None
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

    nsnd_: logical = None
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

    if_: logical = None
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

    nfst_: logical = None
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

    imp_: logical = None
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

    nand_: logical = None
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

    bt_: logical = None
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

# All nullary, unary, and binary operators as named class constants.
logical.nf_ = logical((0,))
logical.nt_ = logical((1,))
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

# All nullary, unary, and binary operators as top-level constants.
nf_: logical = logical.nf_
nt_: logical = logical.nt_
uf_: logical = logical.uf_
id_: logical = logical.id_
not_: logical = logical.not_
ut_: logical = logical.ut_
bf_: logical = logical.bf_
and_: logical = logical.and_
nimp_: logical = logical.nimp_
fst_: logical = logical.fst_
nif_: logical = logical.nif_
snd_: logical = logical.snd_
xor_: logical = logical.xor_
or_: logical = logical.or_
nor_: logical = logical.nor_
xnor_: logical = logical.xnor_
nsnd_: logical = logical.nsnd_
if_: logical = logical.if_
nfst_: logical = logical.nfst_
imp_: logical = logical.imp_
nand_: logical = logical.nand_
bt_: logical = logical.bt_

# Useful class constants: containers of all operators.
logical.nullary = {nf_, nt_}
logical.unary = {uf_, id_, not_, ut_}
logical.binary = {
    bf_,
    and_, nimp_, fst_, nif_, snd_, xor_, or_,
    nor_, xnor_, nsnd_, if_, nfst_, imp_, nand_,
    bt_
}
logical.every = logical.nullary | logical.unary | logical.binary

# Top-level constants corresponding to class constants for containers.
nullary: set = logical.nullary
unary: set = logical.unary
binary: set = logical.binary
every: set = logical.every

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
