import pytest
from pygraphblas import Matrix


def test_check_mult():
    row_inds = [0, 0, 1, 1]
    col_inds = [0, 1, 0, 1]

    matrix_1 = Matrix.from_lists(row_inds, col_inds, [1, 2, 0, 3])
    matrix_2 = Matrix.from_lists(row_inds, col_inds, [0, 1, 3, 5])

    matrix_res = matrix_1 @ matrix_2

    expected = Matrix.from_lists(row_inds, col_inds, [6, 11, 9, 15])

    assert expected.iseq(matrix_res), "Matrices not equal"
