#include <fstream>
#include <chrono>
#include <vector>
#include <functional>
#include <iostream>
#include <iomanip>

#include "utils/save_load.cpp"
#include "utils/conv_graph.cpp"

#include "algorithms/dijkstra.cpp"
#include "algorithms/floydwarshall.cpp"

using namespace std;

double measure(function<void()> fn, int runs = 1){
    double total_time = 0.0;
    for (int i = 0; i < runs; i++)
    {
        auto start = chrono::high_resolution_clock::now();
        fn();
        auto end = chrono::high_resolution_clock::now();
        total_time += chrono::duration<double, milli>(end - start).count();
    }
    return total_time / runs;
}

void run_benchmark(const vector<vector<vector<pair<int, int>>>>& graphs, const string& density_label, ofstream& csv) { 
    for (const auto& adj_list : graphs) {
        int n = adj_list.size();

        long long E = 0;
        for (const auto& neighbors : adj_list) {
            E += neighbors.size();
        }

        auto adj_matrix = to_adj_matrix(adj_list);

        int runs = 1;
        if (n < 500) runs = 5;
        if (n < 200) runs = 10;

        cout << "[running] " << density_label << "  V=" << n << " E=" << E << " (runs=" << runs << ")" << flush;

        double t_dijkstra_array = measure([&](){ dijkstra_array_all_pairs(adj_list); }, runs);
        double t_dijkstra_heap  = measure([&](){ dijkstra_heap_all_pairs(adj_list); },  runs);
        double t_floyd_warshall = measure([&](){ floyd_warshall(adj_matrix); },         runs);

        csv << density_label   << ","
            << n               << ","
            << E               << ","
            << fixed << setprecision(3)
            << t_dijkstra_array << ","
            << t_dijkstra_heap  << ","
            << t_floyd_warshall << "\n";

        cout << " ✓" << endl;
    }
}

int main(){
    ofstream csv("outputs/results.csv");
    csv << "density,vertices,edges,"
        << "dijkstra_array_ms,dijkstra_heap_ms,floyd_warshall_ms\n";

    {
        cout << "Loading sparse graphs..." << endl;
        vector<vector<vector<pair<int, int>>>> sparse_graphs = load_all_graphs("inputs/sparse_graphs.txt");
        cout << "Loaded " << sparse_graphs.size() << " sparse graphs\n" << endl;
        run_benchmark(sparse_graphs, "sparse", csv);
    }

    cout << "\n[✓] Sparse graphs complete\n" << endl;

    {
        cout << "Loading dense graphs..." << endl;
        vector<vector<vector<pair<int, int>>>> dense_graphs = load_all_graphs("inputs/dense_graphs.txt");
        cout << "Loaded " << dense_graphs.size() << " dense graphs\n" << endl;
        run_benchmark(dense_graphs,  "dense",  csv);
    }

    cout << "\n[✓] Dense graphs complete\n" << endl;
    cout << "[✓] Results written to outputs/results.csv\n";
    
    return 0;
}