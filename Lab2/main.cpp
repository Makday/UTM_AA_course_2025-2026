#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>
#include <random>
#include <cstdint>
#include <algorithm>
#include <functional>

#include "algorithms/merge_sort.h"
#include "algorithms/quick_sort.h"
#include "algorithms/heap_sort.h"

using namespace std;

vector<int> generate_random(int size, mt19937& rng){
    uniform_int_distribution<int32_t> dist(INT32_MIN, INT32_MAX);
    vector<int> arr(size);
    for(int i = 0; i < size; i++) arr[i] = dist(rng);
    return arr;
}

void write_output(const string& filename, const vector<vector<int>>& arrs){
    ofstream fout(filename);
    fout << arrs.size() << "\n";
    for(const auto& arr : arrs){
        fout << arr.size();
        for(int x : arr) fout << " " << x;
        fout << "\n";
    }
}

vector<vector<int>> read_input(string file_path){
    ifstream fin(file_path);
    int num;
    fin >> num;

    vector<vector<int>> arrs(num);
    for(int i = 0; i < num; i++){
        int size;
        fin >> size;
        vector<int> arr(size);
        for (int j = 0; j < size; j++) {
            fin >> arr[j];
        }
        arrs[i] = arr;
    }
    fin.close();
    return arrs;
}

double measure(function<void()> fn){
    auto start = chrono::high_resolution_clock::now();
    fn();
    auto end = chrono::high_resolution_clock::now();
    return chrono::duration<double, nano>(end - start).count();
}

void benchmark(ofstream& fout, const string& algo, const string& input_type, vector<vector<int>> arrs){
    for(auto arr : arrs){
        double t = 0;

        if(algo == "mergesort")
            t = measure([&](){ mergesort(0, arr.size()-1, arr.data()); });
        else if(algo == "quicksort")
            t = measure([&](){ quicksort(0, arr.size()-1, arr.data()); });
        else if(algo == "heapsort")
            t = measure([&](){ heapsort(arr.data(), arr.size()); });

        fout << algo << "," << input_type << "," << arr.size() << "," << t << "\n";
    }
}

int main(){
    mt19937 rng(42);

    vector<int> sizes(30);
    for(int i = 0; i < 30; i++)
        sizes[i] = (int)(100000 + (1000000 - 100000) * i / 29.0);

    vector<vector<int>> random_arrs, sorted_arrs, reverse_arrs;

    for(int size : sizes){
        // random
        vector<int> arr = generate_random(size, rng);
        random_arrs.push_back(arr);

        // sorted
        vector<int> sarr = generate_random(size, rng);
        sort(sarr.begin(), sarr.end());
        sorted_arrs.push_back(sarr);

        // reverse sorted
        vector<int> rarr = generate_random(size, rng);
        sort(rarr.begin(), rarr.end(), greater<int>());
        reverse_arrs.push_back(rarr);
    }

    write_output("inputs/random_input.txt", random_arrs);
    write_output("inputs/sorted_input.txt", sorted_arrs);
    write_output("inputs/reverse_sorted_input.txt", reverse_arrs);

    cout << "Generated " << sizes.size() << " arrays." << endl;
    cout << "Size range: " << sizes.front() << " to " << sizes.back() << endl;

    ofstream fout("outputs/benchmark.txt");
    fout << "algorithm,input_type,size,time_ns\n";

    vector<string> algos      = {"mergesort", "heapsort", "quicksort"} ;
    vector<string> input_types = {"random", "sorted", "reverse"};
    vector<vector<vector<int>>> inputs = {random_arrs, sorted_arrs, reverse_arrs};

    for(const string& algo : algos){
        for(int i = 0; i < input_types.size(); i++){
            benchmark(fout, algo, input_types[i], inputs[i]);
            fout.flush();
        }
        cout<<"Done benchmarking : "<<algo<<endl;
    }

    fout.close();
    return 0;
}

    // g++ main.cpp algorithms/merge_sort.cpp algorithms/quick_sort.cpp algorithms/heap_sort.cpp