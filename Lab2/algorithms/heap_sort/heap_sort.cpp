#include <algorithm>

void heapify(int *a, int size, int i){
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < size && a[l] > a[largest])
        largest = l;

    if (r < size && a[r] > a[largest])
        largest = r;

    if (largest != i){
        std::swap(a[i], a[largest]);
        heapify(a, size, largest);
    }
}

void heapsort(int *a, int size){
    for (int i = size / 2 - 1; i >= 0; i--)
        heapify(a, size, i);

    for (int i = size - 1; i >= 0; i--){
        std::swap(a[0], a[i]);
        heapify(a, i, 0);
    }
}