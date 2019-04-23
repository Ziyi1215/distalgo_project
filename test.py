class G:
    def __init__(self, weights, n):
        if len(weights) == n * n:
            self.weights = weights
            self.np = n
        else:
            print('Input weights error')

    def neighbor(self, p):
        neighbor_ids = []
        neighbor_weights = self.weights[p * self.np: (p + 1) * self.np]
        for i in range(self.np):
            if neighbor_weights[i] > 0:
                neighbor_ids.append(i)
        return neighbor_ids

    def distance(self, i, j):
        if self.weights[i * self.np + j] == -1:
            return float("inf")
        else:
            return self.weights[i * self.np + j]

if __name__ == "__main__":
    weights = [
        0, -1, 3,
        5, 0, 8,
        10, -1, 0,
    ]
    graph = G(weights, 3)
    print(graph.neighbor(0))
    print(graph.neighbor(1))
    print(graph.neighbor(2))
    print(graph.distance(0, 0))
    print(graph.distance(0, 1))
    print(graph.distance(0, 2))
