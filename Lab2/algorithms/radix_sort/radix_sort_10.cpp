#include <cstdint>
#include <cstring>
#include <algorithm>

inline uint32_t to_radix_key(int32_t x) {
    return static_cast<uint32_t>(x) ^ 0x80000000u;
}

void countsort10(int *a, int n, int *res, int exp){
    int freq[10] = {};
    
    for(int i = 0; i < n; i++){
        uint32_t key = to_radix_key(a[i]);
        int digit = (key / exp) % 10;
        freq[digit]++;
    }

    for(int i = 1; i < 10; i++)
        freq[i] += freq[i-1];;
    
    for (int i = n - 1; i >= 0; i--) {
        uint32_t key = to_radix_key(a[i]);
        int digit = (key / exp) % 10;
        res[freq[digit] - 1] = a[i];
        freq[digit]--;
    }
}

void radixsort10(int *a, int n){
    if (n < 2) return;
    int max_abs = 0;
    for (int i = 0; i < n; i++) {
        if (abs(a[i]) > max_abs) max_abs = abs(a[i]);
    }
    
    int *temp = new int[n];
    for(int exp = 1; max_abs/exp > 0; exp*=10){
        countsort10(a, n, temp, exp);
        std::swap(a, temp);
    }
    
    if (a != temp) {
        for (int i = 0; i < n; i++) {
            a[i] = temp[i];
        }
    }
    
    delete[] temp;
}