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

    def reserved_capacity(self, cluster_name, usage, replica):
        number_of_reserved_node = self.clusters[cluster_name].request_max_available(usage, replica)
        return number_of_reserved_node


class Task:
    def __init__(self, vertices: list[Vertex], replica, usage):
        self.vertices = vertices
        self.usage = usage
        self.replica = replica
        self.received_throughput = [0] * len(vertices)

    # def set_received_throughput(self, index, amount):
    #     self.received_throughput[index] = amount
    #

    def demand_throughput(self, cluster_name, usage, replica, target_graph: Graph) -> int:
        gained_nodes = target_graph.reserved_capacity(cluster_name, usage, replica)
        return gained_nodes

    def get_resource(self):
        yield

    def finished(self):
        yield

    def ford_fulkerson(self):
        task_graph = {}

        for i, vertex in enumerate(self.vertices):
            if vertex.start in task_graph:
                task_graph[vertex.start].append((vertex.end, self.received_throughput[i]))
            else:
                task_graph[vertex.start] = [(vertex.end, self.received_throughput[i])]


        flow = 0
        while True:
            queue = []

            # initial node for search
            initial_nodes = task_graph["0"]
            for tuple in initial_nodes:
                way= [Vertex("0" , tuple[0])]
                queue.append(way)

            found = False
            while len(queue) != 0:

                found = False
                way = queue.pop(0)
                last_vertex = way[-1]

                # check loop
                way_vertecies = set()
                loop = False
                for ver in way:
                    if ver.end in way_vertecies:
                        loop = True
                        break
                    way_vertecies.add(ver.start)
                if loop:
                    continue

                # it means that we find the sink
                if last_vertex.end == '-2':
                    flow += 1
                    found = True
                    for v in way:
                        same_start_nodes = task_graph[v.start]
                        # for i in range(len(same_start_nodes)):
                        for i, _ in enumerate(same_start_nodes):
                            neighbor = same_start_nodes[i]
                            if neighbor[0] == v.end:
                                same_start_nodes.remove(neighbor)
                                if neighbor[1] - 1 > 0:
                                    same_start_nodes.insert(0, (v.end, neighbor[1] - 1))

                                task_graph[v.start] = same_start_nodes

                                # setup reverse vertex after add new way
                                if v.end in task_graph.keys():
                                    isExist = False
                                    current_list_of_tuples = task_graph[v.end]
                                    # if len(current_list_of_tuples) == 2:
                                    #     current_list_of_tuples = [current_list_of_tuples]
                                    for t in current_list_of_tuples:
                                        if t[0] == v.start:
                                            isExist = True
                                            current_list_of_tuples.remove(t)
                                            current_list_of_tuples.append((v.start, t[1] + 1))
                                            task_graph[v.end] = current_list_of_tuples

                                    if len(current_list_of_tuples) == 0:
                                        isExist = True
                                        current_list_of_tuples = [(v.start, 1)]
                                        task_graph[v.end] = current_list_of_tuples

                                    if not isExist:
                                        current_list_of_tuples.append((v.start, 1))
                                        task_graph[v.end] = current_list_of_tuples
                                else:
                                    task_graph[v.end] = [(v.start, 1)]
                    break

                else:
                    if last_vertex.end not in task_graph.keys():
                        # can not continue this way any more
                        continue
                    next_steps = task_graph[last_vertex.end]

                    if len(next_steps) == 0:
                        continue

                    for neighbor in next_steps:
                        # val is tuple that first element is the end node id and second element is
                        # throughput
                        new_way = way.copy()
                        new_way.append(Vertex(last_vertex.end, neighbor[0]))
                        queue.append(new_way)

                if found:
                    break
            if not found:
                break

        return flow


def main():
    # print("hello")
    # graph = Graph()
    setup_graph_and_clusters()

    setup_graph_and_clusters()

    # test
    task = Task(
        [Vertex("0", 'a'), Vertex("0", 'd'), Vertex('a', 'b'), Vertex('d', 'c'), Vertex('b', '-2'), Vertex('d', 'b'),
         Vertex('c', '-2')], 0, 0)

    task.received_throughput = [8, 3, 9, 4, 2, 7, 5]

    print(task.ford_fulkerson())


def setup_graph_and_clusters():
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
