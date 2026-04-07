#include <vector>
#include <utility>

void dfs_adj_matrix(const std::vector<std::vector<bool>>& matrix, std::vector<bool>& visited, int node){
    visited[node] = true;
    int n = visited.size();
    for(int i = 0; i < n; i++) {
        if(matrix[node][i] && !visited[i]) dfs_adj_matrix(matrix, visited, i);
    }
}

void dfs_adj_matrix(const std::vector<std::vector<bool>>& matrix){
    int v = matrix[0].size();
    std::vector<bool> visited(v, false);

    for (int i = 0; i < v; i++) {
        if (!visited[i]) {
            dfs_adj_matrix(matrix, visited, i);
        }
    }
}

void dfs_adj_list(const std::vector<std::vector<int>>& graph, std::vector<bool>& visited, int node) {
    visited[node] = true;

    for (int neighbor : graph[node]) {
        if (!visited[neighbor]) {
            dfs_adj_list(graph, visited, neighbor);
        }
    }
}

void dfs_adj_list(const std::vector<std::vector<int>>& graph) {
    int v = graph.size();
    std::vector<bool> visited(v, false);

    for (int i = 0; i < v; i++) {
        if (!visited[i]) {
            dfs_adj_list(graph, visited, i);
        }
    }
}

void dfs_edge_list(int n, const std::vector<std::pair<int, int>>& edges, std::vector<bool>& visited, int node) {
    visited[node] = true;

    for (const auto& edge : edges) {
        int u = edge.first;
        int v = edge.second;
        if (u == node && !visited[v])
            dfs_edge_list(n, edges, visited, v);
        else if (v == node && !visited[u])  // undirected — check both directions
            dfs_edge_list(n, edges, visited, u);
    }
}

void dfs_edge_list(int n, const std::vector<std::pair<int, int>>& edges) {
    std::vector<bool> visited(n, false);

    for (int i = 0; i < n; i++)
        if (!visited[i])
            dfs_edge_list(n, edges, visited, i);
}