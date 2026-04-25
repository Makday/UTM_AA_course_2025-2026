#include <fstream>
#include <chrono>
#include <vector>
#include <functional>
#include <iostream>
#include <iomanip>

#include "utils/save_load.cpp"
#include "utils/conv_graph.cpp"
#include "algorithms/dfs.cpp"
#include "algorithms/bfs.cpp"

using namespace std;

double measure(function<void()> fn, int runs = 10){
    double total_time = 0.0;
    for (int i = 0; i < runs; i++)
    {
        auto start = chrono::high_resolution_clock::now();
        fn();
        auto end = chrono::high_resolution_clock::now();
        total_time += chrono::duration<double, nano>(end - start).count();
    }
    return total_time / runs;;
}

void run_benchmark(const vector<vector<vector<int>>>& graphs, const string& density_label, ofstream& csv) { 
    for (const auto& adj_list : graphs) {
        int n = adj_list.size();

        // convert once per graph
        auto adj_matrix = to_adj_matrix(adj_list);
        auto edge_list  = to_edge_list(adj_list);

        int runs = max(1, 1000 / n);  // more runs for small graphs

        double t_dfs_list   = measure([&](){ dfs_adj_list(adj_list); },       runs);
        double t_dfs_matrix = measure([&](){ dfs_adj_matrix(adj_matrix); },   runs);
        double t_dfs_edge   = measure([&](){ dfs_edge_list(n, edge_list); },  runs);
        double t_bfs_list   = measure([&](){ bfs_adj_list(adj_list); },       runs);
        double t_bfs_matrix = measure([&](){ bfs_adj_matrix(adj_matrix); },   runs);
        double t_bfs_edge   = measure([&](){ bfs_edge_list(n, edge_list); },  runs);

        long long E = edge_list.size();

        csv << density_label   << ","
            << n               << ","
            << E               << ","
            << fixed << setprecision(2)
            << t_dfs_list      << ","
            << t_dfs_matrix    << ","
            << t_dfs_edge      << ","
            << t_bfs_list      << ","
            << t_bfs_matrix    << ","
            << t_bfs_edge      << "\n";

        cout << "[done] " << density_label << "  V=" << n << endl;
    }
}

int main(){
    ofstream csv("outputs/results.csv");
    csv << "density,vertices,edges,"
        << "dfs_adj_list_ns,dfs_adj_matrix_ns,dfs_edge_list_ns,"
        << "bfs_adj_list_ns,bfs_adj_matrix_ns,bfs_edge_list_ns\n";

    {
        vector<vector<vector<int>>> sparse_graphs   = load_all_graphs("inputs/sparse_graphs.txt");
        cout<<"Done with sparse graph loading"<<endl;
        run_benchmark(sparse_graphs, "sparse", csv);
    }

    cout<<"Done with sparse"<<endl;

    {
        vector<vector<vector<int>>> dense_graphs    = load_all_graphs("inputs/dense_graphs.txt");
        cout<<"Done with dense graph loading"<<endl;
        run_benchmark(dense_graphs,  "dense",  csv);
    }

    cout<<"Done with dense"<<endl;

    cout << "\n[✓] Results written to results.csv\n";
    return 0;
}