#include "utils.h"

void log_state(std::ofstream& fout, int* a, int n) {
    for (int i = 0; i < n; i++) {
        fout << a[i];
        if (i < n - 1) fout << " ";
    }
    fout << "\n";
}