#include <vector>
#include <tuple>
#include <limits>



std::vector<std::vector<int>> to_adj_matrix(const std::vector<std::vector<std::pair<int, int>>>& a) {
    int INF = std::numeric_limits<int>::max();
    int n = a.size();
    std::vector<std::vector<int>> matrix(n, std::vector<int>(n, INF));
    
    for (int i = 0; i < n; ++i) {
        matrix[i][i] = 0;
    }

    for (int u = 0; u < n; ++u) {
        for (const auto& edge : a[u]) {
            matrix[u][edge.first] = edge.second;  // Only u->v
        }
    }

    return matrix;
}

std::vector<std::tuple<int, int, int>> to_edge_list(const std::vector<std::vector<std::pair<int, int>>>& a) {
    std::vector<std::tuple<int, int, int>> edges;
    
    int n = a.size();
    
    for (int u = 0; u < n; ++u) {
        for (const auto& edge : a[u]) {
            edges.emplace_back(u, edge.first, edge.second);  // No u < v check
        }
    }
    
    return edges;
}