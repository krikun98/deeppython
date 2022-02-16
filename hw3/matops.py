import copy

import numpy as np


class Matrix(list):
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

    def __matmul__(self, other):
        if len(other) != len(self[0]):
            raise Exception("Incompatible vectors")
        return Matrix([[sum(self[i][k] * other[k][j] for k in range(len(other)))
                        for j in range(len(other[0]))] for i in range(len(self))])


if __name__ == "__main__":
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (2, 2)))
    b = Matrix(np.random.randint(0, 10, (2, 2)))
    with open("matrix+.txt", "w") as file:
        file.write(str(a+b))
    with open("matrix*.txt", "w") as file:
        file.write(str(a+b))
    with open("matrix@.txt", "w") as file:
        file.write(str(a+b))