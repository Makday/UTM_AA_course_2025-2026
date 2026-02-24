#include "utils.h"
#include <algorithm>

int median_of_three(int l, int r, int *a){
    int mid = l + (r - l) / 2;
    if(a[l] > a[mid]) std::swap(a[l], a[mid]);
    if(a[l] > a[r])   std::swap(a[l], a[r]);
    if(a[mid] > a[r]) std::swap(a[mid], a[r]);
    std::swap(a[mid], a[l]);
    return a[l];
}

void quicksort(int l, int r, int *a){
    if(l >= r) return;
    int p = median_of_three(l, r, a), k = l;
    for(int i = l; i <= r; i++){
        if(a[i] < p){
            k++;
            std::swap(a[i], a[k]);
        }
    }
    a[l]=a[k];
    a[k]=p;
    quicksort(l, k - 1, a);
    quicksort(k + 1, r, a);
}