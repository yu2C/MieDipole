import numpy as np

def TenCont(A, B, dim):
    # Get the shape of A and B
    sizeA = np.array(A.shape)
    sizeB = np.array(B.shape)

    # Check for dimension validity
    if len(dim) > 2:
        print("Wrong Assignment of Dimension in TenCont")
        return

    # Get the size of the target column
    sizetar = np.max(sizeB)

    # Alert of Illegal Operation
    if np.sum(sizeB) > sizetar + 1:
        print("Illegal Tensor Contraction")
        return

    # Remove the contracted dimension from sizeA
    sizeA_new = np.delete(sizeA, dim[0])

    # Reshape A for dot product
    A_reshaped = np.reshape(A, (np.prod(sizeA_new), sizetar))

    # Perform the dot product
    result_dot = np.dot(A_reshaped, B)

    # Reshape the result back to the original shape, minus the contracted dimension
    result = np.reshape(result_dot, sizeA_new)

    return result

# Testing
#A = np.random.rand(3, 4, 5)
#B = np.random.rand(5)
#dim = [2]

#result = TenCont(A, B, dim)
#print(result.shape)  # Should be (3, 4)
