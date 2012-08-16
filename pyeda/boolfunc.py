"""
Boolean Functions

Interface Classes:
    Variable
    Function
    VectorFunction

Huntington's Postulates
+---------------------------------+--------------+
| x + y = y + x                   | Commutative  |
| x * y = y * x                   | Commutative  |
+---------------------------------+--------------+
| x + (y * z) = (x + y) * (x + z) | Distributive |
| x * (y + z) = (x * y) + (x * z) | Distributive |
+---------------------------------+--------------+
| x + x' = 1                      | Complement   |
| x * x' = 0                      | Complement   |
+---------------------------------+--------------+

Properties of Boolean Algebraic Systems
+---------------------------+---------------+
| x + (y + z) = (x + y) + z | Associativity |
| x * (y * z) = (x * y) * z | Associativity |
+---------------------------+---------------+
| x + x = x                 | Idempotence   |
| x * x = x                 | Idempotence   |
+---------------------------+---------------+
| x + (x * y) = x           | Absorption    |
| x * (x + y) = x           | Absorption    |
+---------------------------+---------------+
| (x + y)' = x' * y'        | De Morgan     |
| (x * y)' = x' + y'        | De Morgan     |
+---------------------------+---------------+
| (x')' = x                 | Involution    |
+---------------------------+---------------+
"""

__copyright__ = "Copyright (c) 2012, Chris Drake"

from .common import bit_on

UNSIGNED, TWOS_COMPLEMENT = range(2)


class Variable:
    """Boolean variable base class"""

    def __init__(self, name, index=None):
        self._name = name
        self._index = index

    def __str__(self):
        if self._index is None:
            return self._name
        else:
            return "{0._name}[{0._index}]".format(self)

    @property
    def name(self):
        return self._name

    @property
    def index(self):
        return self._index


class Function:
    """
    Abstract base class that defines an interface for a scalar Boolean function
    of N variables.
    """
    @property
    def support(self):
        """Return the support set of a function.

        Let f(x1, x2, ..., xn) be a Boolean function of N variables. The set
        {x1, x2, ..., xn} is called the *support* of the function.
        """
        raise NotImplementedError()

    def __abs__(self):
        """Return the cardinality of the support set."""
        return len(self.support)

    # Overloaded operators
    def __neg__(self):
        return self.op_not()

    def __add__(self, other):
        return self.op_or(other)

    #def __radd__(self, other):
    #    return self.op_or(other)

    def __mul__(self, other):
        return self.op_and(other)

    #def __rmul__(self, other):
    #    return self.op_and(other)

    def __lshift__(self, other):
        """Return a << b, equivalent to b -> a."""
        return self.op_ge(other)

    #def __rlshift(self, other):
    #    return self.op_ge(other):

    def __rshift__(self, other):
        """Return a >> b, equivalent to a -> b."""
        return self.op_le(other)

    #def __rrshift__(self, other):
    #    return self.op_le(other)

    # Operators
    def op_not(self):
        """Return symbolic complement of a Boolean function.

        +---+----+
        | f | -f |
        +---+----+
        | 0 |  1 |
        | 1 |  0 |
        +---+----+

        Also known as: NOT
        """
        raise NotImplementedError()

    def op_or(self, *args):
        """Return symbolic disjunction of functions.

        +---+---+-------+
        | f | g | f + g |
        +---+---+-------+
        | 0 | 0 |   0   |
        | 0 | 1 |   1   |
        | 1 | 0 |   1   |
        | 1 | 1 |   1   |
        +---+---+-------+

        Also known as: sum, OR
        """
        raise NotImplementedError()

    def op_and(self, *args):
        """Return symbolic conjunction of functions.

        +---+---+-------+
        | f | g | f * g |
        +---+---+-------+
        | 0 | 0 |   0   |
        | 0 | 1 |   0   |
        | 1 | 0 |   0   |
        | 1 | 1 |   1   |
        +---+---+-------+

        Also known as: product, AND
        """
        raise NotImplementedError()

    def op_eq(self, *args):
        """Return symbolic "equal to" of functions.

        +---+---+-------+
        | f | g | f = g |
        +---+---+-------+
        | 0 | 0 |   1   |
        | 0 | 1 |   0   |
        | 1 | 0 |   0   |
        | 1 | 1 |   1   |
        +---+---+-------+

        Also known as: Exclusive NOR (XNOR), even parity
        """
        raise NotImplementedError()

    def op_ne(self, *args):
        """Return symbolic "not equal to" of functions.

        +---+---+--------+
        | f | g | f != g |
        +---+---+--------+
        | 0 | 0 |    0   |
        | 0 | 1 |    1   |
        | 1 | 0 |    1   |
        | 1 | 1 |    0   |
        +---+---+--------+

        Also known as: Exclusive OR (XOR), odd parity
        """
        raise NotImplementedError()

    def op_gt(self, other):
        """Return symbolic "greater than" of two functions.

        +---+---+-------+
        | f | g | f > g |
        +---+---+-------+
        | 0 | 0 |   0   |
        | 0 | 1 |   0   |
        | 1 | 0 |   1   |
        | 1 | 1 |   0   |
        +---+---+-------+
        """
        raise NotImplementedError()

    def op_lt(self, other):
        """Return symbolic "less than" of two functions.

        +---+---+-------+
        | f | g | f < g |
        +---+---+-------+
        | 0 | 0 |   0   |
        | 0 | 1 |   1   |
        | 1 | 0 |   0   |
        | 1 | 1 |   0   |
        +---+---+-------+
        """
        raise NotImplementedError()

    def op_ge(self, other):
        """Return symbolic "greater than or equal to" of two functions.

        +---+---+--------+
        | f | g | f >= g |
        +---+---+--------+
        | 0 | 0 |    1   |
        | 0 | 1 |    0   |
        | 1 | 0 |    1   |
        | 1 | 1 |    1   |
        +---+---+--------+
        """
        raise NotImplementedError()

    def op_le(self, other):
        """Return symbolic "less than or equal to" of two functions.

        +---+---+--------+
        | f | g | f <= g |
        +---+---+--------+
        | 0 | 0 |    1   |
        | 0 | 1 |    1   |
        | 1 | 0 |    0   |
        | 1 | 1 |    1   |
        +---+---+--------+

        Also known as: implies (f -> g)
        """
        raise NotImplementedError()

    def restrict(self, d):
        """
        Return the Boolean function that results after restricting a subset of
        its input variables to {0, 1}.

        g = f | xi=b
        """
        raise NotImplementedError()

    def compose(self, d):
        """
        Return the Boolean function that results after substituting a subset of
        its input variables for other Boolean functions.

        g = f1 | xi=f2
        """
        raise NotImplementedError()

    def iter_cofactors(self, vs=None):
        """Iterate through the cofactors of N variables."""
        vs = vs or list()
        for n in range(2 ** len(vs)):
            yield self.restrict({v: bit_on(n, i) for i, v in enumerate(vs)})

    def cofactors(self, vs=None):
        """Return a tuple of cofactors of N variables.

        The *cofactor* of f(x1, x2, ..., xi, ..., xn) with respect to
        variable xi is f[xi] = f(x1, x2, ..., 1, ..., xn)

        The *cofactor* of f(x1, x2, ..., xi, ..., xn) with respect to
        variable xi' is f[xi'] = f(x1, x2, ..., 0, ..., xn)
        """
        return tuple(cf for cf in self.iter_cofactors(vs))


class VectorFunction:
    """
    Abstract base class that defines an interface for a vector Boolean function.
    """
    def __init__(self, *fs, **kwargs):
        self.fs = list(fs)
        self._start = kwargs.get("start", 0)
        self._bnr = kwargs.get("bnr", UNSIGNED)

    def __int__(self):
        return self.to_int()

    def __iter__(self):
        return iter(self.fs)

    def __len__(self):
        return len(self.fs)

    @property
    def start(self):
        """Return the start index."""
        return self._start

    def _get_bnr(self):
        """Return the binary number representation."""
        return self._bnr

    def _set_bnr(self, value):
        self._bnr = value

    bnr = property(fget=_get_bnr, fset=_set_bnr)

    @property
    def sl(self):
        return slice(self._start, len(self.fs) + self._start)

    # Operators
    def uor(self):
        raise NotImplementedError()

    def uand(self):
        raise NotImplementedError()

    def uxor(self):
        raise NotImplementedError()

    def __invert__(self):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()

    def __xor__(self, other):
        raise NotImplementedError()

    def to_uint(self):
        """Convert vector to an unsigned integer."""
        raise NotImplementedError()

    def to_int(self):
        """Convert vector to an integer."""
        raise NotImplementedError()

    def getifz(self, i):
        """Get item from zero-based index."""
        return self.__getitem__(i + self.start)

    def __getitem__(self, sl):
        if isinstance(sl, int):
            return self.fs[self._norm_idx(sl)]
        else:
            cls = self.__class__
            norm_sl = self._norm_slice(sl)
            return cls(*self.fs.__getitem__(norm_sl),
                       start=(norm_sl.start + self._start), bnr=self._bnr)

    def __setitem__(self, sl, f):
        if isinstance(sl, int):
            self.fs.__setitem__(sl, f)
        else:
            norm = self._norm_slice(sl)
            self.fs.__setitem__(norm, f)

    def _norm_idx(self, i):
        """Return an index normalized to vector start index."""
        if i >= 0:
            if i < self._start:
                raise IndexError("list index out of range")
            else:
                idx = i - self._start
        else:
            idx = i + self._start
        return idx

    def _norm_slice(self, sl):
        """Return a slice normalized to vector start index."""
        d = dict()
        for k in ("start", "stop"):
            idx = getattr(sl, k)
            if idx is not None:
                d[k] = (idx if idx >= 0 else self.sl.stop + idx)
            else:
                d[k] = getattr(self.sl, k)
        if d["start"] < self.sl.start or d["stop"] > self.sl.stop:
            raise IndexError("list index out of range")
        elif d["start"] >= d["stop"]:
            raise IndexError("zero-sized slice")
        return slice(d["start"] - self._start, d["stop"] - self._start)

    def append(self, f):
        """Append a function to the end of this vector."""
        self.fs.append(f)