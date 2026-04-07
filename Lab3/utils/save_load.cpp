#include <fstream>
#include <vector>
#include <string>

void save_graph(std::ofstream& file, const std::vector<std::vector<int>>& adj) {
    int E = 0;
    for (auto& neighbors : adj) E += neighbors.size();
    E /= 2;

    file << "---\n";
    file << adj.size() << " " << E << "\n";
    for (int u = 0; u < (int)adj.size(); u++)
        for (int v : adj[u])
            if (u < v)
                file << u << " " << v << "\n";
}

std::vector<std::vector<std::vector<int>>> load_all_graphs(const std::string& filename) {
    std::ifstream file(filename);

    int count;
    file >> count;

    std::vector<std::vector<std::vector<int>>> graphs;
    graphs.reserve(count);

    std::string separator;
    while (getline(file, separator)) {
        if (separator != "---") continue;

        int V, E;
        file >> V >> E;

        std::vector<std::vector<int>> adj(V);
        int u, v;
        for (int i = 0; i < E; i++) {
            file >> u >> v;
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
        graphs.push_back(adj);
    }
    return graphs;
}