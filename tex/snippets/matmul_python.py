for i in range(N):
  for j in range(N):
    for k in range(N):
      C[i, j] += A[i, k] * B[k, j]