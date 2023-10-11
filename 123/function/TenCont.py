## Tensor Contraction for A_ijk * B_k
import numpy as np



def TenCont(A, B, dim):
    # Get matrix sizes
    sizeA = np.array(A.shape)
    sizeB = np.array(B.shape)

    # Check for errors in dimension assignment
    if len(dim) > 2:
        print('Wrong Assignment of Dimension in TenCont')
        return None

    # Size of the target column
    sizetar = np.max(sizeB)

    # Check for illegal operation
    if np.sum(sizeB) > sizetar + 1:
        print('Illegal Tensor Contraction')
        return None

    # Erasing the contribution of the target column
    sizeA = np.delete(sizeA, dim[0])

    # Reshaping matrix and contraction
    result = np.dot(A.reshape((-1, sizetar)), B)

    # Reshape to the original size
    result = result.reshape(tuple(sizeA))

    return result

'''
# Example usage
A = np.ones((1, 2 * 1 + 1, 3))
B = np.array(([1],
              [1],
              [1]))
print(A)
print(B)
dim = [2, 0]  # Example dimension

result = TenCont(A, B, dim)
print("Result shape:", result.shape)
print("Result:", result)
'''
