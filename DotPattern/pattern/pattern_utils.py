import numpy as np
import random

def get_pattern(size, n_dots):
	'''Generates a random matrix of n times n'''
	seed_pattern = np.zeros((size,size)) 
	grid_numbers = list(range(size**2))

	chosen_numbers = random.sample(grid_numbers, n_dots)
	for i in chosen_numbers:
		x, y = i // 10, i % 10
		seed_pattern[x, y] = 1
		  
	return seed_pattern

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