#pragma omp parallel for shared(a,b,c) private(i, j, k)
for (i = 0; i < size; ++i) {
    for (j = 0; j < size; ++j) {
        for (k = 0; k < size; ++k) {
            c[i][j] += a[i][k] * b[k][j];
        }
    }
}