#include <vector>
#include <limits>

// Standard Floyd-Warshall - O(V³)
// Returns all-pairs shortest path distances
std::vector<std::vector<int>> floyd_warshall(const std::vector<std::vector<int>>& graph) {
    int INF = std::numeric_limits<int>::max();
    int n = graph.size();
    std::vector<std::vector<int>> dist = graph;  // Copy input matrix
    
    // Triple nested loop: try each vertex as intermediate
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                // Avoid overflow when dist[i][k] or dist[k][j] is INF
                if (dist[i][k] != INF && dist[k][j] != INF) {
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }
    }
    
    return dist;
}