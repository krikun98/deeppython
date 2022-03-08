# Easy
import copy
import numpy as np
from pathlib import Path
from functools import lru_cache


class Hashable:
    def __hash__(self):
        return int(np.sum(self))  # looks self-explanatory

    def __eq__(self, other):
        return self == other

    def dummy(self):
        return


class Matrix(list, Hashable):
    __hash__ = Hashable.__hash__

    def __add__(self, other):
        if len(other) != len(self) or len(other[0]) != len(self[0]):
            raise Exception("Incompatible vectors")
        new_mat = copy.deepcopy(self)
        for i in range(len(self)):
            for j in range(len(self[0])):
                new_mat[i][j] += other[i][j]
        return new_mat

    def __mul__(self, other):
        if len(other) != len(self) or len(other[0]) != len(self[0]):
            raise Exception("Incompatible vectors")
        new_mat = copy.deepcopy(self)
        for i in range(len(self)):
            for j in range(len(self[0])):
                new_mat[i][j] *= other[i][j]
        return new_mat

    @lru_cache
    def __matmul__(self, other):
        if len(other) != len(self[0]):
            raise Exception("Incompatible vectors")
        return Matrix([[sum(self[i][k] * other[k][j] for k in range(len(other)))

                        for j in range(len(other[0]))] for i in range(len(self))])

    def ncmatmul(self, other):
        if len(other) != len(self[0]):
            raise Exception("Incompatible vectors")
        return Matrix([[sum(self[i][k] * other[k][j] for k in range(len(other)))
                        for j in range(len(other[0]))] for i in range(len(self))])


def find_collisions():
    a = Matrix(np.random.randint(0, 10, (2, 2)))
    b = Matrix(np.random.randint(0, 10, (2, 2)))
    c = copy.deepcopy(a)
    d = copy.deepcopy(b)
    c[0][1] -= 1
    c[0][0] += 1
    Path("artifacts/hard").mkdir(exist_ok=True)
    with open("artifacts/hard/A.txt", "w") as file:
        file.write(str(a))
    with open("artifacts/hard/B.txt", "w") as file:
        file.write(str(b))
    with open("artifacts/hard/C.txt", "w") as file:
        file.write(str(c))
    with open("artifacts/hard/D.txt", "w") as file:
        file.write(str(d))
    with open("artifacts/hard/AB.txt", "w") as file:
        file.write(str(a@b))
    with open("artifacts/hard/CD.txt", "w") as file:
        file.write(str(c.ncmatmul(d)))


if __name__ == "__main__":
    Path("artifacts/easy").mkdir(exist_ok=True)
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (2, 2)))
    b = Matrix(np.random.randint(0, 10, (2, 2)))
    with open("artifacts/easy/matrixplus.txt", "w") as file:
        file.write(str(a + b))
    with open("artifacts/easy/matrixmul.txt", "w") as file:  # the OS didn't like matrix* as a path.
        file.write(str(a * b))
    with open("artifacts/easy/matrixmatmul.txt", "w") as file:
        file.write(str(a @ b))
    find_collisions()
