import numpy as np

# Store all user-input matrices
matrices = {}

# ==========================
# Automatic matrix label generation function (A, B, ..., Z, AA, AB, ...)
# ==========================

label_counter = 0   # Start counting from 0 -> A

def get_next_label():
    global label_counter
    label = number_to_label(label_counter)
    label_counter += 1
    return label

def number_to_label(n):
    """Convert number to Excel-style letter label"""
    s = ""
    n += 1  # Make 0 correspond to A
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

def input_matrix(name):
    """Input matrix and store"""
    print(f"\nEnter the number of rows and columns for matrix {name}:")
    rows = int(input("Rows: "))
    cols = int(input("Columns: "))

    data = []
    print(f"Enter each row of matrix {name} (numbers separated by spaces):")
    for i in range(rows):
        row = list(map(float, input(f"Row {i+1}: ").split()))
        while len(row) != cols:
            print("Column count mismatch, please re-enter!")
            row = list(map(float, input(f"Row {i+1}: ").split()))
        data.append(row)

    matrices[name] = np.array(data)
    print(f"\nMatrix {name} has been stored:\n{matrices[name]}\n")


def add_matrices(a, b):
    """Matrix addition"""
    if a not in matrices or b not in matrices:
        print("Cannot find the given matrix names!")
        return
    if matrices[a].shape != matrices[b].shape:
        print("Matrix dimensions are inconsistent, cannot add!")
        return
    print(f"\n{a} + {b} result:\n{matrices[a] + matrices[b]}\n")

def subtract_matrices(a, b):
    """Matrix subtraction a - b"""
    if a not in matrices or b not in matrices:
        print("Cannot find the given matrix names!")
        return
    if matrices[a].shape != matrices[b].shape:
        print("Matrix dimensions are inconsistent, cannot subtract!")
        return
    print(f"\n{a} - {b} result:\n{matrices[a] - matrices[b]}\n")


def multiply_matrices(a, b):
    """Matrix multiplication"""
    if a not in matrices or b not in matrices:
        print("Cannot find the given matrix names!")
        return
    if matrices[a].shape[1] != matrices[b].shape[0]:
        print("Matrix dimensions do not match, cannot multiply!")
        return
    print(f"\n{a} × {b} result:\n{matrices[a] @ matrices[b]}\n")


def transpose_matrix(a):
    """Matrix transpose"""
    if a not in matrices:
        print("Cannot find the matrix name!")
        return
    print(f"\nTranspose of matrix {a}:\n{matrices[a].T}\n")

def inverse_matrix(a):
    """Calculate the inverse of the matrix"""
    if a not in matrices:
        print("Cannot find the matrix name!")
        return

    mat = matrices[a]

    # Inverse is only defined for square matrices
    if mat.shape[0] != mat.shape[1]:
        print(f"Matrix {a} is not square, cannot compute inverse!")
        return

    # If determinant is 0, not invertible
    det = np.linalg.det(mat)
    if det == 0:
        print(f"Matrix {a} has determinant 0, not invertible!")
        return

    inv = np.linalg.inv(mat)
    print(f"\nInverse of matrix {a}:\n{inv}\n")

def determinant_matrix(a):
    """Calculate the determinant of the matrix"""
    if a not in matrices:
        print("Cannot find the matrix name!")
        return

    mat = matrices[a]

    # Determinant is only defined for square matrices
    if mat.shape[0] != mat.shape[1]:
        print(f"Matrix {a} is not square, cannot compute determinant!")
        return

    det = round(np.linalg.det(mat),1)
    print(f"\nDeterminant (det) of matrix {a}: {det}\n")

def rank_matrix(a):
    """Calculate the rank of the matrix"""
    if a not in matrices:
        print("Cannot find the matrix name!")
        return

    mat = matrices[a]

    r = np.linalg.matrix_rank(mat)
    print(f"\nRank of matrix {a}: {r}\n")

def eigen_matrix(a):
    """Calculate eigenvalues and eigenvectors of the matrix"""
    if a not in matrices:
        print("Cannot find the matrix name!")
        return

    mat = matrices[a]

    # Must be square to compute eigenvalues/eigenvectors
    if mat.shape[0] != mat.shape[1]:
        print(f"Matrix {a} is not square, cannot compute eigenvalues and eigenvectors!")
        return

    # Use numpy to compute eigenvalues and eigenvectors
    values, vectors = np.linalg.eig(mat)

    print(f"\nEigenvalues of matrix {a}:\n{values}\n")
    print(f"Eigenvectors of matrix {a} (by columns):\n{vectors}\n")

def lu_decomposition(matrix):
    """Perform LU decomposition on the matrix (Doolittle algorithm), return L, U"""

    import numpy as np
    A = np.array(matrix, dtype=float)
    n = A.shape[0]

    # Must be square
    if A.shape[0] != A.shape[1]:
        print("LU decomposition requires a square matrix!")
        return None, None

    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        # Compute row i of U
        for k in range(i, n):
            sum_u = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - sum_u

        # Compute column i of L
        for k in range(i, n):
            if i == k:
                L[i][i] = 1  # Diagonal of L is 1
            else:
                if U[i][i] == 0:
                    print("LU decomposition failed: zero pivot encountered (pivoting needed)")
                    return None, None
                sum_l = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (A[k][i] - sum_l) / U[i][i]

    return L, U

def lu_matrix(name):
    """Perform LU decomposition on the specified matrix"""
    if name not in matrices:
        print("Cannot find the matrix name!")
        return

    L, U = lu_decomposition(matrices[name])

    if L is None:
        return

    print(f"\nLU decomposition result of matrix {name}:")
    print("L =\n", L)
    print("U =\n", U)
    print()

def qr_decomposition(A):
    """Perform QR decomposition on matrix A (classic Gram-Schmidt)"""

    A = np.array(A, dtype=float)
    m, n = A.shape

    Q = np.zeros((m, n))
    R = np.zeros((n, n))

    for k in range(n):
        # Copy column k
        u = A[:, k].copy()

        # Subtract projections from previous q's
        for j in range(k):
            R[j, k] = np.dot(Q[:, j], A[:, k])
            u = u - R[j, k] * Q[:, j]

        # Norm
        norm_u = np.linalg.norm(u)
        if norm_u == 0:
            print("QR decomposition failed: linearly dependent columns")
            return None, None

        R[k, k] = norm_u
        Q[:, k] = u / norm_u

    return Q, R

def qr_matrix(name):
    """Perform QR decomposition on the specified matrix"""
    if name not in matrices:
        print("Cannot find the matrix name!")
        return

    Q, R = qr_decomposition(matrices[name])
    if Q is None:
        return

    print(f"\nQR decomposition result of matrix {name}:")
    print("Q =\n", Q)
    print("R =\n", R)
    print()

# -------------------------
# Usage example (you can modify)
# -------------------------

print("Welcome to the simple matrix tool!")

while True:
    print("""
Functions:
1. Input matrix
2. Generate random matrix
3. Generate identity matrix
4. Generate zero matrix
5. Generate diagonal matrix
6. View all matrices
7. Matrix addition
8. Matrix subtraction
9. Matrix multiplication
10. Matrix transpose
11. Matrix inverse
12. Compute determinant
13. Compute matrix rank
14. Eigenvalues and eigenvectors
15. LU decomposition
16. QR decomposition
17. Exit
""")

    choice = input("Please select a function: ")

    if choice == "1":
        name = input("Please enter the matrix name (e.g., A, B1, M3): ")
        input_matrix(name)

    elif choice == '2':
        rows = int(input("Rows: "))
        cols = int(input("Columns: "))
        low = int(input("Random value lower bound: "))
        high = int(input("Random value upper bound: "))
    
        M = np.random.randint(low, high, (rows, cols))
        label = get_next_label()
        matrices[label]=M
        
    
        print(f"\nMatrix {label} has been generated:\n{M}\n")
    
    elif choice == '3':
        n = int(input("Matrix order n: "))
    
        M = np.eye(n)
    
        label = get_next_label()
        matrices[label] = M
    
        print(f"\nMatrix {label} has been generated:\n{M}\n")
    
    elif choice == '4':
        rows = int(input("Rows: "))
        cols = int(input("Columns: "))
    
        M = np.zeros((rows, cols))
        label = get_next_label()
        matrices[label] = M

    
        print(f"Zero matrix {label} =\n{M}")
    
    elif choice == '5':
        diag_elements = list(map(float, input("Enter diagonal elements (space-separated): ").split()))
    
        M = np.diag(diag_elements)
        label = get_next_label()
        matrices[label] = M

    
        print(f"Diagonal matrix {label} =\n{M}")

    elif choice == "6":
        print("\nCurrently stored matrices:")
        for key in matrices:
            print(f"{key} =\n{matrices[key]}\n")

    elif choice == "7":
        a = input("Enter the first matrix name for addition: ")
        b = input("Enter the second matrix name for addition: ")
        add_matrices(a, b)

    elif choice == "8":
        a = input("Enter the minuend matrix (left matrix) name: ")
        b = input("Enter the subtrahend matrix (right matrix) name: ")
        subtract_matrices(a, b)
        
    elif choice == "9":
        a = input("Enter the left matrix name: ")
        b = input("Enter the right matrix name: ")
        multiply_matrices(a, b)

    elif choice == "10":
        a = input("Enter the matrix name to transpose: ")
        transpose_matrix(a)

    elif choice == "11":
        a = input("Enter the matrix name to compute inverse: ")
        inverse_matrix(a)

    elif choice == "12":
        a = input("Enter the matrix name to compute determinant: ")
        determinant_matrix(a)

    elif choice == "13":
        a = input("Enter the matrix name to compute rank: ")
        rank_matrix(a)

    elif choice == "14":
        a = input("Enter the matrix name to compute eigenvalues and eigenvectors: ")
        eigen_matrix(a)
        
    elif choice == "15":
        a = input("Enter the matrix name for LU decomposition: ")
        lu_matrix(a)

    elif choice == "16":
        a = input("Enter the matrix name for QR decomposition: ")
        qr_matrix(a)

    elif choice == "17":
        print("Program exited.")
        break

    else:
        print("Invalid selection, please re-enter!")
