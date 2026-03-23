#include "utils/utils.h"
#include <algorithm>

int median_of_three_animated(int l, int r, int *a) {
    int mid = l + (r - l) / 2;
    if (a[l] > a[mid]) std::swap(a[l], a[mid]);
    if (a[l] > a[r])   std::swap(a[l], a[r]);
    if (a[mid] > a[r]) std::swap(a[mid], a[r]);
    std::swap(a[mid], a[l]);
    return a[l];
}

void quicksort_animated(int l, int r, int *a, int total, std::ofstream& fout) {
    if (l >= r) return;
    int p = median_of_three_animated(l, r, a), k = l;
    for (int i = l; i <= r; i++) {
        if (a[i] < p) {
            k++;
            std::swap(a[i], a[k]);
            log_state(fout, a, total); 
        }
    }
    a[l] = a[k];
    a[k] = p;
    log_state(fout, a, total);
    quicksort_animated(l, k - 1, a, total, fout);
    quicksort_animated(k + 1, r, a, total, fout);
}

void quicksort_animated(int l, int r, int *a, std::ofstream& fout) {
    log_state(fout, a, r + 1);
    quicksort_animated(l, r, a, r + 1, fout);
}