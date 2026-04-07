#include <vector>

std::vector<std::vector<bool>> to_adj_matrix(const std::vector<std::vector<int>>& a) {
    int n = a.size();
    std::vector<std::vector<bool>> matrix(n, std::vector<bool>(n, 0));

    for (int u = 0; u < n; ++u) {
        for (int v : a[u]) {
            matrix[u][v] = true;
            matrix[v][u] = true;
        }
    }

    return matrix;
}

std::vector<std::pair<int, int>> to_edge_list(const std::vector<std::vector<int>>& a) {
    std::vector<std::pair<int, int>> edges;
    
    int n = a.size();
    
    for (int u = 0; u < n; ++u) {
        for (int v : a[u]) {
            if (u < v) {
                edges.emplace_back(u, v);
            }
        }
    }
    
    return edges;
}