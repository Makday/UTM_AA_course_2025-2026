#include "utils/utils.h"
#include <algorithm>
#include <fstream>

void heapify_animated(int *a, int size, int i, int total, std::ofstream& fout){
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < size && a[l] > a[largest])
        largest = l;

    if (r < size && a[r] > a[largest])
        largest = r;

    if (largest != i) {
        std::swap(a[i], a[largest]);
        log_state(fout, a, total);
        heapify_animated(a, size, largest, total, fout);
    }
}

void heapsort_animated(int *a, int size, std::ofstream& fout){
    log_state(fout, a, size);

    for (int i = size / 2 - 1; i >= 0; i--)
        heapify_animated(a, size, i, size, fout);

    for (int i = size - 1; i >= 0; i--) {
        std::swap(a[0], a[i]);
        log_state(fout, a, size);
        heapify_animated(a, i, 0, size, fout);
    }
}