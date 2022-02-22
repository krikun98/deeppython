# Medium
import numbers

import numpy as np
from pathlib import Path


class Printer:
    def __str__(self):
        return str(self.value)


class Offloader:
    def offload(self, filename):
        with open(filename, "w") as file:
            file.write(str(self))


class Gettable:
    def get_value(self):
        return self.value


class Settable:
    def set_value(self, value):
        self.value = value


class NpMatrix(np.lib.mixins.NDArrayOperatorsMixin, Printer, Offloader, Gettable, Settable):
    def __init__(self, value):
        self.value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (NpMatrix,)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, NpMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, NpMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.value)



if __name__ == "__main__":
    Path("artifacts").mkdir(exist_ok=True)
    np.random.seed(0)
    a = NpMatrix([])
    a.set_value(np.random.randint(0, 10, (2, 2)))
    b = NpMatrix(np.random.randint(0, 10, (2, 2)))
    (a+b).offload("artifacts/npmatrixplus.txt")
    (a*b).offload("artifacts/npmatrixmul.txt")
    (a@b).offload("artifacts/npmatrixmatmul.txt")
