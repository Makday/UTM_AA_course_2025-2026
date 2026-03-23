#include "utils/utils.h"
#include <cstdint>

inline uint32_t to_radix_key(int32_t x) {
    return static_cast<uint32_t>(x) ^ 0x80000000u;
}

void countsort256_animated(int *a, int n, int *res, int shift, std::ofstream& fout) {
    int freq[256] = {};

    for (int i = 0; i < n; i++) {
        uint32_t key = to_radix_key(a[i]);
        int byte = (key >> shift) & 0xFF;
        freq[byte]++;
    }

    for (int i = 1; i < 256; i++)
        freq[i] += freq[i - 1];

    for (int i = 0; i < n; i++) res[i] = a[i];

    for (int i = n - 1; i >= 0; i--) {
        uint32_t key = to_radix_key(a[i]);
        int byte = (key >> shift) & 0xFF;
        res[freq[byte] - 1] = a[i];
        freq[byte]--;
        log_state(fout, res, n); 
    }
}

void radixsort256_animated(int *a, int n, std::ofstream& fout) {
    if (n < 2) return;

    int *temp = new int[n];

    log_state(fout, a, n);

    countsort256_animated(a, n, temp, 0, fout); 
    countsort256_animated(temp, n, a, 8, fout); 
    countsort256_animated(a, n, temp, 16, fout); 
    countsort256_animated(temp, n, a, 24, fout);  

    delete[] temp;
}