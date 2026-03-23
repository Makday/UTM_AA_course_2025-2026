#include "utils/utils.h"
#include <fstream>

void merge_animated(int l, int mid, int r, int a[], int temp[], int total, std::ofstream& fout) {
    int lsub = l, rsub = mid + 1, k = l;
    while (lsub <= mid && rsub <= r) {
        if (a[lsub] <= a[rsub]) {
            temp[k++] = a[lsub++];
        } else {
            temp[k++] = a[rsub++];
        }
    }
    while (lsub <= mid) temp[k++] = a[lsub++];
    while (rsub <= r)   temp[k++] = a[rsub++];

    for (int i = l; i <= r; i++) {
        a[i] = temp[i];
        log_state(fout, a, total);
    }
}

void mergesort_animated(int l, int r, int a[], int temp[], int total, std::ofstream& fout) {
    if (l >= r) return;
    int mid = (l + r) / 2;
    mergesort_animated(l, mid, a, temp, total, fout);
    mergesort_animated(mid + 1, r, a, temp, total, fout);
    merge_animated(l, mid, r, a, temp, total, fout);
}

void mergesort_animated(int l, int r, int a[], std::ofstream& fout) {
    int total = r + 1;
    int* temp = new int[total];
    log_state(fout, a, total);
    mergesort_animated(l, r, a, temp, total, fout);
    delete[] temp;
}