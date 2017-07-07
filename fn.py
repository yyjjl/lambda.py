#! /usr/bin/env python3

import operator
import functools


def dispatch1(op, v):
    f = v.lam
    return Lambda(lambda *vs: op(f(*vs)))


def dispatch2(op, v1, v2):
    f1 = v1.lam
    if isinstance(v2, Lambda):
        f2 = v2.lam
        return Lambda(lambda *vs: op(f1(*vs), f2(*vs)))
    return Lambda(lambda *vs: op(f1(*vs), v2))


def dispatch3(op, v1, v2, v3):
    f1 = v1.lam
    is_lam2 = isinstance(v2, Lambda)
    is_lam3 = isinstance(v3, Lambda)
    if is_lam2 and is_lam3:
        f2, f3 = v2.lam, v3.lam
        return Lambda(lambda *vs: op(f1(*vs), f2(*vs), f3(*vs)))
    elif is_lam2:
        f2 = v2.lam
        return Lambda(lambda *vs: op(f1(*vs), f2(*vs), v3))
    elif is_lam2:
        f3 = v3.lam
        return Lambda(lambda *vs: op(f1(*vs), v2, f3(*vs)))
    return Lambda(lambda *vs: op(f1(*vs), v2, v3))


class Lambda:
    def __init__(self, lam=None):
        self.lam = lam

    def __call__(self, *vs):
        f = self.lam
        return Lambda(lambda *nvs: f(*nvs)(*vs))

    def __getattr__(self, v):
        return dispatch2(getattr, self, v)

    def __getitem__(self, key):
        if isinstance(key, slice):
            key = dispatch3(slice, key.start, key.stop, key.step)
        return dispatch2(operator.getitem, self, key)

    def __next__(self):
        return dispatch1(next, self)

    def __iter__(self):
        return dispatch1(iter, self)

    def __reversed__(self):
        return dispatch1(reversed, self)

    def __lt__(self, v):
        return dispatch2(operator.lt, self, v)

    def __le__(self, v):
        return dispatch2(operator.le, self, v)

    def __eq__(self, v):
        return dispatch2(operator.eq, self, v)

    def __ne__(self, v):
        return dispatch2(operator.ne, self, v)

    def __ge__(self, v):
        return dispatch2(operator.ge, self, v)

    def __gt__(self, v):
        return dispatch2(operator.gt, self, v)

    def __add__(self, v):
        return dispatch2(operator.add, self, v)

    def __sub__(self, v):
        return dispatch2(operator.sub, self, v)

    def __mul__(self, v):
        return dispatch2(operator.mul, self, v)

    def __matmul__(self, v):
        return dispatch2(operator.matmul, self, v)

    def __truediv__(self, v):
        return dispatch2(operator.truediv, self, v)

    def __floordiv__(self, v):
        return dispatch2(operator.floordiv, self, v)

    def __mod__(self, v):
        return dispatch2(operator.mod, self, v)

    def __divmod__(self, v):
        return dispatch2(divmod, self, v)

    def __pow__(self, v1, v2):
        return dispatch3(pow, self, v1, v2)

    def __lshift__(self, v):
        return dispatch2(operator.lshift, self, v)

    def __rshift__(self, v):
        return dispatch2(operator.rshift, self, v)

    def __and__(self, v):
        return dispatch2(operator.and_, self, v)

    def __xor__(self, v):
        return dispatch2(operator.xor, self, v)

    def __or__(self, v):
        return dispatch2(operator.or_, self, v)

    def __radd__(self, v):
        return dispatch2(lambda x, y: y + x, self, v)

    def __rsub__(self, v):
        return dispatch2(lambda x, y: y - x, self, v)

    def __rmul__(self, v):
        return dispatch2(lambda x, y: y * x, self, v)

    def __rmatmul__(self, v):
        return dispatch2(lambda x, y: y @ x, self, v)

    def __rtruediv__(self, v):
        return dispatch2(lambda x, y: y / x, self, v)

    def __rfloordiv__(self, v):
        return dispatch2(lambda x, y: y // x, self, v)

    def __rmod__(self, v):
        return dispatch2(lambda x, y: y % x, self, v)

    def __rdivmod__(self, v):
        return dispatch2(lambda x, y: divmod(y, x), self, v)

    def __rpow__(self, v):
        return dispatch3(lambda x, y: y**x, self, v)

    def __rlshift__(self, v):
        return dispatch2(lambda x, y: y << x, self, v)

    def __rrshift__(self, v):
        return dispatch2(lambda x, y: y >> x, self, v)

    def __rand__(self, v):
        return dispatch2(lambda x, y: y & x, self, v)

    def __rxor__(self, v):
        return dispatch2(lambda x, y: y ^ x, self, v)

    def __ror__(self, v):
        return dispatch2(lambda x, y: y | x, self, v)

    def __neg__(self):
        return dispatch1(operator.neg, self)

    def __pos__(self):
        return dispatch1(operator.pos, self)

    def __abs__(self):
        return dispatch1(abs, self)

    def __invert__(self):
        return dispatch1(operator.invert, self)

    def __contains__(self, v):
        return dispatch2(operator.contains, self, v)


_1 = Lambda(lambda *x: x[0])
_2 = Lambda(lambda *x: x[1])
_3 = Lambda(lambda *x: x[2])
_4 = Lambda(lambda *x: x[3])
_5 = Lambda(lambda *x: x[4])
_6 = Lambda(lambda *x: x[5])
_7 = Lambda(lambda *x: x[6])
_8 = Lambda(lambda *x: x[7])
_9 = Lambda(lambda *x: x[8])


def L(lam):
    return lambda *vs: lam.lam(*vs)


def andmap(f, vs):
    if len(vs) == 0:
        return True
    return f(vs[0]) and andmap(f, vs[1:])


def ormap(f, vs):
    if len(vs) == 0:
        return False
    return f(vs[0]) or ormap(f, vs[1:])


def wrap(f):
    def hasLambda(vs):
        return ormap(lambda x: isinstance(x, Lambda), vs)

    @functools.wraps(f)
    def wrapped(*vs, **ks):
        if hasLambda(vs) or hasLambda(ks):
            def inner(*vs_):
                def call(ls):
                    for v in ls:
                        if isinstance(v, Lambda):
                            v = v.lam(*vs_)
                        yield v
                vs2 = list(call(vs))
                ks2 = dict(zip(ks.keys(), call(ks.values())))
                return f(*vs2, **ks2)
            return Lambda(inner)
        return f(*vs, **ks)
    return wrapped
