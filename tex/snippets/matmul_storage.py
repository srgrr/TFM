@task(C = INOUT)
def multiply(A, B, C):
  '''Multiplies two blocks and acumulates the result in an INOUT
  matrix
  '''
  C += A.block * B.block

def dot(A, B, C, set_barrier = False):
  '''A COMPSs-PSCO blocked matmul algorithm
  A and B (blocks) are PSCOs, while C (blocks) are objects
  '''
  n, m = len(A), len(B[0])
  # as many rows as A, as many columns as B
  for i in range(n):
    for j in range(m):
      for k in range(n):
        multiply(A[i][j], B[i][j], C[i][j])
  if set_barrier:
    from pycompss.api.api import compss_barrier
    compss_barrier()   
