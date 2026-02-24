#include <cstdint>
#include <algorithm>

inline uint32_t to_radix_key(int32_t x) {
    return static_cast<uint32_t>(x) ^ 0x80000000u;
}

void countsort256(int *a, int n, int *res, int shift){
    int freq[256] = {};
    
    for(int i = 0; i < n; i++){
        uint32_t key = to_radix_key(a[i]);
        int byte = (key >> shift) & 0xFF;
        freq[byte]++;
    }

    for(int i = 1; i < 256; i++)
        freq[i] += freq[i-1];;
    
    for (int i = n - 1; i >= 0; i--) {
        uint32_t key = to_radix_key(a[i]);
        int byte = (key >> shift) & 0xFF;
        res[freq[byte] - 1] = a[i];
        freq[byte]--;
    }
}

void radixsort256(int *a, int n) {
    if (n < 2) return;
    int *temp = new int[n];
    countsort256(a, n, temp, 0);
    countsort256(temp, n, a, 8);
    countsort256(a, n, temp, 16);
    countsort256(temp, n, a, 24);

    delete[] temp;
}