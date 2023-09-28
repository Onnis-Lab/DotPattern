import numpy as np

def get_pattern(n):
    '''Generates a random matrix of n times n'''
    return np.random.choice([0, 1], size=(n, n))

def compare_patterns(A, B):
    '''Compares two matrices and returns the percentage of correctly matched figure'''
    if A.shape != B.shape:
        raise ValueError('Matrices must be of the same shape')

    return np.sum(A == B)/A.size


if __name__ == '__main__':
    A = get_pattern(10)
    B = get_pattern(10)

    print(A)
    print(B)
    print(compare_patterns(A, B))