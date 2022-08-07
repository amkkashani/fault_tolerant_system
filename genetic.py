import random
import time
from typing import List

import main
from main import Task
from main import Graph
from main import Node
from main import Cluster
from main import *

Genome = List[Task]
Population = List[Genome]


def generate_genome(tasks: List[Task]):
    graph = main.setup_problem_clusters()
    random.seed(time.time())
    for task in tasks:
        task.received_throughput = [0] * len(task.vertices)
        start_nodes = set()

        for i, vertex in enumerate(task.vertices):
            if vertex.start in start_nodes:  # initial heuristic
                continue
            if vertex.end == -2:
                continue  # it is end node and no need to get resource

            start_nodes.add(vertex.start)
            random_replica = random.randint(1, task.replica + 1)
            accepted_replica = task.demand_throughput(vertex.end, task.usage, random_replica, graph)
            task.received_throughput[i] = accepted_replica



def generate_population(size: int, tasks: List[Task]):
    return [generate_genome(tasks) for _ in range(size)]


def fitness_function(genome: Genome) -> int:
    yield
