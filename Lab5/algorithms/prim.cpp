#include <vector>
#include <queue>
#include <tuple>

std::vector<int> prim(const std::vector<std::vector<std::pair<int, int>>>& adj) {
    int n = adj.size();
    std::vector<bool> visited(n, false);
    std::vector<int> parent(n, -1);
    
    typedef std::tuple<int, int, int> Edge;
    std::priority_queue<Edge, std::vector<Edge>, std::greater<Edge> > pq;
    
    visited[0] = true;
    for (size_t i = 0; i < adj[0].size(); i++) {
        int neighbor = adj[0][i].first;
        int weight = adj[0][i].second;
        pq.push(std::make_tuple(weight, neighbor, 0));
    }
    
    while (!pq.empty()) {
        Edge top = pq.top();
        pq.pop();
        
        int weight = std::get<0>(top);
        int v = std::get<1>(top);
        int p = std::get<2>(top);
        
        if (visited[v]) continue;
        
        visited[v] = true;
        parent[v] = p;
        
        for (size_t i = 0; i < adj[v].size(); i++) {
            int neighbor = adj[v][i].first;
            int w = adj[v][i].second;
            if (!visited[neighbor]) {
                pq.push(std::make_tuple(w, neighbor, v));
            }
        }
    }
    
    return parent;
}