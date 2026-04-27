#include <vector>
#include <queue>
#include <limits>

constexpr int INF = std::numeric_limits<int>::max();

// Single-source Array-based Dijkstra - O(V²)
std::vector<int> dijkstra_array(const std::vector<std::vector<std::pair<int, int>>>& adj, int source) {
    int n = adj.size();
    std::vector<int> dist(n, INF);
    std::vector<bool> visited(n, false);
    
    dist[source] = 0;
    
    for (int i = 0; i < n; ++i) {
        int u = -1;
        for (int v = 0; v < n; ++v) {
            if (!visited[v] && (u == -1 || dist[v] < dist[u])) {
                u = v;
            }
        }
        
        if (dist[u] == INF) break;
        
        visited[u] = true;
        
        for (const auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;
            
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
            }
        }
    }
    
    return dist;
}

// Single-source Priority queue Dijkstra - O((V + E) log V)
std::vector<int> dijkstra_heap(const std::vector<std::vector<std::pair<int, int>>>& adj, int source) {
    int n = adj.size();
    std::vector<int> dist(n, INF);
    
    std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<std::pair<int, int>>> pq;
    
    dist[source] = 0;
    pq.push({0, source});
    
    while (!pq.empty()) {
        auto top = pq.top();
        pq.pop();
        
        int d = top.first;
        int u = top.second;
        
        if (d > dist[u]) continue;
        
        for (const auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;
            
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}

// ALL-PAIRS Array-based Dijkstra - O(V³)
// Runs Dijkstra from every vertex
std::vector<std::vector<int>> dijkstra_array_all_pairs(const std::vector<std::vector<std::pair<int, int>>>& adj) {
    int n = adj.size();
    std::vector<std::vector<int>> all_dist(n);
    
    // Run Dijkstra from each vertex
    for (int source = 0; source < n; ++source) {
        all_dist[source] = dijkstra_array(adj, source);
    }
    
    return all_dist;
}

// ALL-PAIRS Priority queue Dijkstra - O(V * (V + E) log V) = O(V² log V) for sparse
// Runs Dijkstra from every vertex
std::vector<std::vector<int>> dijkstra_heap_all_pairs(const std::vector<std::vector<std::pair<int, int>>>& adj) {
    int n = adj.size();
    std::vector<std::vector<int>> all_dist(n);
    
    // Run Dijkstra from each vertex
    for (int source = 0; source < n; ++source) {
        all_dist[source] = dijkstra_heap(adj, source);
    }
    
    return all_dist;
}