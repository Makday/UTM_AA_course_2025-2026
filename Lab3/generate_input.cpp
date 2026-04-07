#include <iostream>
#include <random>

#include "algorithms/dfs.cpp"
#include "utils/save_load.cpp"

using namespace std;

mt19937 rng(42);

vector<vector<int>> generate_graph(int n, double density) {
    vector<vector<int>> adj(n);
    uniform_real_distribution<double> prob(0.0, 1.0);

    for (int u = 0; u < n; u++)
        for (int v = u + 1; v < n; v++)
            if (prob(rng) < density) {
                adj[u].push_back(v);
                adj[v].push_back(u);
            }

    return adj;
}

int main() {
    vector<int> sizes = {100, 175, 310, 545, 955, 1680, 2950, 5180, 9100, 16000};
    int num_graphs = sizes.size();
    ofstream sparse_file("inputs/sparse_graphs.txt");
    ofstream dense_file("inputs/dense_graphs.txt");

    sparse_file << num_graphs << "\n";
    dense_file  << num_graphs << "\n";

    for (auto size : sizes) {
        double sparse_density = 8.0 / (size - 1);
        double dense_density  = 0.25;

        {
            auto g = generate_graph(size, sparse_density);
            save_graph(sparse_file, g);
        }

        {
            auto g = generate_graph(size, dense_density);
            save_graph(dense_file, g);
        }
        cout<<"Done with : "<< size<<endl;
    }
    return 0;
}