import numpy as np
import random

def get_pattern(size, n_dots):
	'''Generates a random matrix of n times n'''
	seed_pattern = np.zeros((size,size), dtype=int) 
	grid_numbers = list(range(size**2))

	chosen_numbers = random.sample(grid_numbers, n_dots)
	for i in chosen_numbers:
		x, y = i // size, i % size
		seed_pattern[x, y] = 1
		  
	return seed_pattern

def compare_patterns(A, B):
	A = np.array(A)
	B = np.array(B).reshape(A.shape)
	'''Compares two matrices and returns the percentage of correctly matched figure'''
	if A.shape != B.shape:
		raise ValueError('Matrices must be of the same shape')

	n_dots = np.sum(A) 
	n_correct = 0
	for i in range(A.shape[0]):
		for j in range(A.shape[1]):
			if A[i,j]:
				if A[i, j] == B[i, j]:
					n_correct += 1

	return n_correct


if __name__ == '__main__':
	A = get_pattern(10, 12)
	B = get_pattern(10, 12)

	print(A)
	print(B)
	print(compare_patterns(A, B))