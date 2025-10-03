from Solver import Solver # Import the Solver class from Solver, be sure to reference the correct path 


def main():
    '''Main function to read input, create model, and solve the problem.
    Currently a placeholder implementation based on the SC-QBF problem.'''

    ### ------------
    ### Input Reading
    ### ------------

    # Read the number of variables (n)
    n = int(input())

    # Read the number of elements in each set (but not used afterwards)
    _ = list(map(int, input().split()))

    # Initialize list to hold the sets
    sets = []

    # Read n sets of integers, one per line, and convert to 0-based indices
    for _ in range(n):
        sets.append(set(x - 1 for x in map(int, input().split())))


    # Initialize and read the upper triangular matrix
    upper_A = []
    for i in range(n):
        row = list(map(float, input().split()))
        upper_A.append(row)

    # Convert upper triangular to full n x n matrix (symmetric, fill lower triangle)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(len(upper_A[i])):
            A[i][j] = upper_A[i][j]
            if i != j:
                A[j][i] = upper_A[i][j]

    ### ------------
    ### Problem Solving
    ### ------------

    # Model creation
    solver = Solver(
        n=n,
        sets=sets,
        A=A
        # Pass the other class attributes (if any) here as needed
    )


    solution = solver.solve()


    print(f"\nFinal {solution}", flush=True)


if __name__=='__main__':
    main()
