import math
import genetic
from typing import List

graph = None


# vertex in cluster graph
class Vertex:
    def __init__(self, start, end):
        self.start = start
        self.end = end


# node of cluster
class Node:
    def __init__(self, capacity):
        self.capacity = capacity


class Cluster:
    def __init__(self, name, nodes: list[Node]):
        self.name = name
        self.nodes = nodes
        self.states = []
        for node in nodes:
            self.state = node.capacity

    def request(self, usage, replica=1):
        temp_state = self.states.copy()
        reserve_node = 0
        for i in range(replica):
            id = self.find_min(temp_state, usage)
            if id == -1:
                # not found
                break
            else:
                temp_state[id] -= usage
                reserve_node += 1

        return reserve_node, temp_state

    def accept(self, temp_state):
        self.state = temp_state

    def find_min(self, ls: list[int], cap):
        min = math.inf
        min_id = -1
        for i in range(len(ls)):
            if self.ls[i] < cap:  # node i is not good enough
                continue
            if self.ls[i] < min:
                min = self.ls[i]
                min_id = i
        return min_id


class Task:
    def __init__(self, vertices: list[Vertex], replica):
        self.vertices = vertices
        self.replica = replica
        self.received_throughput = [0] * len(vertices)

    def set_received_througput(self, index, amount):
        self.received_throughput[index] = amount

    def get_resource(self):
        yield

    def finished(self):
        yield


# graph of clusters
class Graph:
    def __init__(self, clusters: List[Cluster]):
        self.clusters = {}

        for cluster in clusters:
            self.clusters[cluster.name] = cluster

    def add_cluster(self, cluster: Cluster):
        self.clusters[cluster.name] = cluster


def main():
    print("hello")
    graph = Graph()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
