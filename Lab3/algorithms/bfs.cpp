#include <vector>
#include <queue>

void bfs_adj_matrix(const std::vector<std::vector<bool>>& matrix){
    int n = matrix.size();
    std::vector<bool> visited(n, 0);

    std::queue<int> qu;
    for (int src = 0; src < n; src++) {   // handle disconnected graphs
        if (visited[src]) continue;
        visited[src] = true;
        qu.push(src);
        while(!qu.empty()){
            int node = qu.front();
            qu.pop();
            for(int i = 0; i < n; i++){
                if(matrix[node][i] && !visited[i]){
                    visited[i] = 1;
                    qu.push(i);
                } 
            }
        }
    }
}

void bfs_adj_list(const std::vector<std::vector<int>>& graph) {
    int n = graph.size();
    std::vector<bool> visited(n, false);
    std::queue<int> q;

    for (int src = 0; src < n; src++) {
        if (visited[src]) continue;
        visited[src] = true;
        q.push(src);

        while (!q.empty()) {
            int node = q.front(); q.pop();

            for (int neighbor : graph[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
    }
}

void bfs_edge_list(int n, const std::vector<std::pair<int, int>>& edges) {
    std::vector<bool> visited(n, false);
    std::queue<int> q;

    for (int src = 0; src < n; src++) {
        if (visited[src]) continue;
        visited[src] = true;
        q.push(src);

        while (!q.empty()) {
            int node = q.front(); q.pop();

            for (const auto& edge : edges) {
                int u = edge.first;
                int v = edge.second;
                if (u == node && !visited[v]) {
                    visited[v] = true;
                    q.push(v);
                } else if (v == node && !visited[u]) {  // undirected
                    visited[u] = true;
                    q.push(u);
                }
            }
        }
    }
}