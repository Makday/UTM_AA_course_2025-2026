#include <algorithm>
#include <vector>
#include <tuple>

class UnionFind {
    private:
        std::vector<int> parent;
        std::vector<int> rank;
        
    public:
        UnionFind(int n) : parent(n), rank(n, 0) {
            for (int i = 0; i < n; i++) {
                parent[i] = i;
            }
        }
        
        int find(int x) {
            if (parent[x] != x) {
                parent[x] = find(parent[x]);
            }
            return parent[x];
        }
        
        bool unite(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);
            
            if (rootX == rootY) return false;
            
            if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
            } else if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
            } else {
                parent[rootY] = rootX;
                rank[rootX]++;
            }
            return true;
        }
    };

struct Edge {
    int u, v, weight;
    
    Edge(int u, int v, int weight) : u(u), v(v), weight(weight) {}
    
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

void kruskal(const std::vector<std::vector<std::pair<int, int>>>& adj) {
    int n = adj.size();
    std::vector<Edge> edges;
    std::vector<Edge> mst;

    for (int u = 0; u < n; u++) {
        for (size_t i = 0; i < adj[u].size(); i++) {
            int v = adj[u][i].first;
            int weight = adj[u][i].second;
            if (u < v) {
                edges.push_back(Edge(u, v, weight));
            }
        }
    }

    std::sort(edges.begin(), edges.end());

    UnionFind uf(n);
    
    // Process edges in sorted order
    for (size_t i = 0; i < edges.size(); i++) {
        Edge e = edges[i];
        if (uf.unite(e.u, e.v)) {
            mst.push_back(e);
            if (mst.size() == n - 1) break;  // MST complete
        }
    }

    return;
}