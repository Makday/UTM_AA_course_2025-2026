void merge(int l, int mid, int r, int a[], int temp[]){
    int lsub = l, rsub = mid + 1, k = l;
    while (lsub <= mid && rsub <= r){
        if (a[lsub] <= a[rsub]){
            temp[k] = a[lsub];
            lsub++;
            k++;
        } else {
            temp[k] = a[rsub];
            rsub++;
            k++;
        }
    }

    while (lsub <= mid){
        temp[k] = a[lsub];
        lsub++;
        k++;
    }

    while (rsub <= r){
        temp[k] = a[rsub];
        rsub++;
        k++;
    }

    for (int i = l; i <= r; i++){
        a[i] = temp[i];
    }
}

void mergesort(int l, int r, int a[], int temp[]){
    if (l >= r) return;
    int mid = (l + r) / 2;
    mergesort(l, mid, a, temp);
    mergesort(mid + 1, r, a, temp);

    merge(l, mid, r, a, temp);
}

void mergesort(int l, int r, int a[]){
    int* temp = new int[r + 1];
    mergesort(l, r, a, temp);
    delete[] temp;
}