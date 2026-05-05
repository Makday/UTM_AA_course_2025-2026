#include <fstream>
#include <vector>
#include <string>

void save_graph(std::ofstream& file, const std::vector<std::vector<std::pair<int, int>>>& adj) {
    int E = 0;
    for (auto& neighbors : adj) E += neighbors.size();
    file << "---\n";
    file << adj.size() << " " << E << "\n";
    for (int u = 0; u < (int)adj.size(); u++)
        for (const auto& edge : adj[u])
            file << u << " " << edge.first << " " << edge.second << "\n";
}

std::vector<std::vector<std::vector<std::pair<int, int>>>> load_all_graphs(const std::string& filename) {
    std::ifstream file(filename);

    int count;
    file >> count;

    std::vector<std::vector<std::vector<std::pair<int, int>>>> graphs;
    graphs.reserve(count);

    std::string separator;
    while (getline(file, separator)) {
        if (separator != "---") continue;

        int V, E;
        file >> V >> E;

        std::vector<std::vector<std::pair<int, int>>> adj(V);
        int u, v, weight;
        for (int i = 0; i < E; i++) {
            file >> u >> v >> weight;
            adj[u].push_back({v, weight});
        }
        graphs.push_back(adj);
    }
    return graphs;
}