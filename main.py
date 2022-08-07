import math
import random

import genetic
from typing import List



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
            self.states.append(node.capacity)

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

    def request_max_available(self, usage, replica=1):
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

        self.accept(temp_state)
        return reserve_node


    def find_min(self, ls: list[int], cap):
        min = math.inf
        min_id = -1
        for i in range(len(ls)):
            if ls[i] < cap:  # node i is not good enough
                continue
            if ls[i] < min:
                min = ls[i]
                min_id = i
        return min_id


# graph of clusters
class Graph:
    def __init__(self, clusters: List[Cluster]):
        self.clusters = {}

        for cluster in clusters:
            self.clusters[cluster.name] = cluster

    def add_cluster(self, cluster: Cluster):
        self.clusters[cluster.name] = cluster

    def reserved_capacity(self, cluster_name, usage , replica):
        number_of_reserved_node = self.clusters[cluster_name].request_max_available(usage , replica)
        return number_of_reserved_node

class Task:
    def __init__(self, vertices: list[Vertex], replica , usage):
        self.vertices = vertices
        self.usage = usage
        self.replica = replica
        self.received_throughput = [0] * len(vertices)

    # def set_received_throughput(self, index, amount):
    #     self.received_throughput[index] = amount
    #

    def demand_throughput(self, cluster_name, usage, replica, target_graph: Graph) -> int:
        gained_nodes =  target_graph.reserved_capacity(cluster_name, usage, replica)
        return gained_nodes

    def get_resource(self):
        yield

    def finished(self):
        yield


def main():
    # print("hello")
    # graph = Graph()
    setup_problem_clusters()

    setup_problem_clusters()



def setup_problem_clusters():
    number_of_clusters = 15
    clusters = []
    random.seed(1500)
    nodes = []
    for i in range(1000):
        nodes.append(Node(random.randint(0, 10)))

    # iteration starts from 1 because source cluster is 0 and the other starts from 1
    for i in range(1, number_of_clusters + 1):
        cluster_nodes = random.randint(5, 15)
        clusters.append(Cluster(i, nodes[0: cluster_nodes]))
        nodes = nodes[cluster_nodes:]

    return Graph(clusters)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
