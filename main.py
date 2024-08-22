import random
import time
import heapq
from typing import List, Tuple

class InvalidArgumentException(Exception):
    pass

class LogicErrorException(Exception):
    pass

class Graph:
    def __init__(self, num_vertices: int):
        self.adjacency_list = [[] for _ in range(num_vertices)]
        self.vertices_data = [None] * num_vertices
        self.distances = []

    def end_vertices(self, e: int) -> List[int]:
        if e < 0 or e >= len(self.adjacency_list):
            raise InvalidArgumentException()
        return [neighbor[0] for neighbor in self.adjacency_list[e]]

    def opposite(self, v: int, e: int) -> int:
        if e < 0 or e >= len(self.adjacency_list) or v < 0 or v >= len(self.adjacency_list):
            raise InvalidArgumentException()
        for neighbor in self.adjacency_list[e]:
            if neighbor[0] == v:
                return neighbor[0]
        raise LogicErrorException()

    def are_adjacent(self, v: int, w: int) -> bool:
        return any(neighbor[0] == w for neighbor in self.adjacency_list[v])

    def replace(self, v: int, x: int):
        self.vertices_data[v] = x

    def replace_edge(self, e: int, x: int):
        if e < 0 or e >= len(self.adjacency_list):
            raise InvalidArgumentException()
        for neighbor in self.adjacency_list[e]:
            neighbor[1] = x

    def insert_vertex(self, o: int):
        self.adjacency_list.append([])
        self.vertices_data.append(o)

    def insert_edge(self, v: int, w: int, o: int):
        if v < 0 or v >= len(self.adjacency_list) or w < 0 or w >= len(self.adjacency_list):
            raise InvalidArgumentException()
        self.adjacency_list[v].append((w, o))
        self.adjacency_list[w].append((v, o))

    def remove_vertex(self, v: int):
        if v < 0 or v >= len(self.adjacency_list):
            raise InvalidArgumentException()
        del self.adjacency_list[v]
        del self.vertices_data[v]
        for neighbors in self.adjacency_list:
            neighbors[:] = [neighbor for neighbor in neighbors if neighbor[0] != v]

    def remove_edge(self, v: int, w: int):
        if v < 0 or v >= len(self.adjacency_list) or w < 0 or w >= len(self.adjacency_list):
            raise InvalidArgumentException()
        self.adjacency_list[v] = [neighbor for neighbor in self.adjacency_list[v] if neighbor[0] != w]
        self.adjacency_list[w] = [neighbor for neighbor in self.adjacency_list[w] if neighbor[0] != v]

    def incident_edges(self, v: int) -> List[int]:
        if v < 0 or v >= len(self.adjacency_list):
            raise InvalidArgumentException()
        return [neighbor[0] for neighbor in self.adjacency_list[v]]

    def get_vertices(self) -> List[int]:
        return list(range(len(self.vertices_data)))

    def get_edges(self) -> List[Tuple[int, int]]:
        edges = []
        for i, neighbors in enumerate(self.adjacency_list):
            for neighbor in neighbors:
                if i < neighbor[0]:
                    edges.append((i, neighbor[0]))
        return edges

    def initialize_single_source(self, source: int):
        self.distances = [{'distance': float('inf'), 'predecessor': -1} for _ in range(len(self.adjacency_list))]
        self.distances[source]['distance'] = 0

    def dijkstra(self, source: int):
        self.initialize_single_source(source)
        visited = [False] * len(self.adjacency_list)
        min_heap = [(0, source)]

        while min_heap:
            dist_u, u = heapq.heappop(min_heap)
            if visited[u]:
                continue
            visited[u] = True

            for v, weight in self.adjacency_list[u]:
                if not visited[v] and dist_u + weight < self.distances[v]['distance']:
                    self.distances[v]['distance'] = dist_u + weight
                    self.distances[v]['predecessor'] = u
                    heapq.heappush(min_heap, (self.distances[v]['distance'], v))

    def get_path(self, source: int, destination: int) -> List[int]:
        path = []
        v = destination
        while v != -1:
            path.append(v)
            v = self.distances[v]['predecessor']
        return path[::-1]

    def shortest_path_from_source(self, source: int):
        self.dijkstra(source)
        for i in range(len(self.adjacency_list)):
            if i != source:
                path = self.get_path(source, i)
                print(f"Vertex {i}: ", end="")
                if self.distances[i]['distance'] == float('inf'):
                    print("No path exists")
                else:
                    print(f"Path: {' -> '.join(map(str, path))}, Distance: {self.distances[i]['distance']}")

    def shortest_path(self, source: int, destination: int):
        self.dijkstra(source)
        print(f"Shortest path from vertex {source} to vertex {destination}: ", end="")
        path = self.get_path(source, destination)
        if self.distances[destination]['distance'] == float('inf'):
            print("No path exists")
        else:
            print(f"Path: {' -> '.join(map(str, path))}, Distance: {self.distances[destination]['distance']}")

def generate_random_instances(num_vertices: int, density: int) -> List[Graph]:
    if density > 100:
        density = 100
    instances = []

    for _ in range(100):
        graph = Graph(num_vertices)
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if random.randint(0, 99) < density:
                    weight = random.randint(1, 10)
                    graph.insert_edge(i, j, weight)
        instances.append(graph)
    return instances

def measure_shortest_path_from_source(instances: List[Graph]):
    for i, instance in enumerate(instances):
        start_time = time.time()
        source_vertex = 0
        instance.shortest_path_from_source(source_vertex)
        end_time = time.time()
        print(f"Time taken to find shortest path for instance {i + 1}: {(end_time - start_time) * 1000:.2f} ms")

def measure_shortest_path(instances: List[Graph], vertex1: int, vertex2: int):
    for i, instance in enumerate(instances):
        start_time = time.time()
        instance.shortest_path(vertex1, vertex2)
        end_time = time.time()
        print(f"Time taken to find shortest path between vertices {vertex1} and {vertex2} for instance {i + 1}: {(end_time - start_time) * 1000:.2f} ms")

def calculate_average_time(instances: List[Graph]):
    total_time = 0.0
    for i, instance in enumerate(instances):
        start_time = time.time()
        source_vertex = 0
        instance.shortest_path_from_source(source_vertex)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        total_time += elapsed_time
        print(f"Time taken to find shortest path for instance {i + 1}: {elapsed_time:.2f} ms")
    average_time = total_time / len(instances)
    print(f"\nAverage time taken to find shortest path for all instances: {average_time:.2f} ms")

def calculate_average_path_time(instances: List[Graph], vertex1: int, vertex2: int):
    total_time = 0.0
    for i, instance in enumerate(instances):
        start_time = time.time()
        instance.shortest_path(vertex1, vertex2)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        total_time += elapsed_time
    average_time = total_time / len(instances)
    print(f"Average time taken to find shortest path between vertices {vertex1} and {vertex2}: {average_time:.2f} ms")

if __name__ == "__main__":
    num_vertices = int(input("Enter number of vertices: "))
    density = int(input("Enter density (percentage): "))

    random_instances = generate_random_instances(num_vertices, density)
    calculate_average_time(random_instances)

    vertex1 = int(input("\nEnter two vertices to find the shortest path between them (vertex1): "))
    vertex2 = int(input("Enter two vertices to find the shortest path between them (vertex2): "))
    calculate_average_path_time(random_instances, vertex1, vertex2)
