#include <iostream>
#include <fstream>
#include <vector>
#include <string>

#include "algorithms/quick_sort/quick_sort_anim.h"
#include "algorithms/merge_sort/merge_sort_anim.h"
#include "algorithms/heap_sort/heap_sort_anim.h"
#include "algorithms/radix_sort/radix_sort_anim.h"

using namespace std;

int main() {
    cout << "Enter number of elements: ";
    int n;
    cin >> n;

    vector<int> input(n);
    cout << "Enter " << n << " integers: ";
    for (int i = 0; i < n; i++)
        cin >> input[i];

    ofstream fout("outputs/animations.txt");
    if (!fout.is_open()) {
        cerr << "Error: could not open outputs/animations.txt\n";
        return 1;
    }


    auto reset = [&](std::vector<int>& arr) {
        arr = input;
    };

    vector<int> arr(n);

    // --- QuickSort ---
    fout << "QUICKSORT " << n << "\n";
    reset(arr);
    quicksort_animated(0, n - 1, arr.data(), fout);
    fout << "\n";

    // --- MergeSort ---
    fout << "MERGESORT " << n << "\n";
    reset(arr);
    mergesort_animated(0, n - 1, arr.data(), fout);
    fout << "\n";

    // --- HeapSort ---
    fout << "HEAPSORT " << n << "\n";
    reset(arr);
    heapsort_animated(arr.data(), n, fout);
    fout << "\n";

    // --- RadixSort ---
    fout << "RADIXSORT " << n << "\n";
    reset(arr);
    radixsort256_animated(arr.data(), n, fout);
    fout << "\n";

    fout.close();
    std::cout << "Done. Results saved to outputs/animations.txt\n";

    return 0;
}

//g++ -o generate_animated generate_animated.cpp algorithms/quick_sort/quick_sort_anim.cpp algorithms/merge_sort/merge_sort_anim.cpp algorithms/heap_sort/heap_sort_anim.cpp algorithms/radix_sort/radix_sort_anim.cpp utils/utils.cpp -I.